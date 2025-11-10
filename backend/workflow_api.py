"""
API-compatible version of the coal blending workflow
Removes Streamlit dependencies for use in FastAPI backend
"""

import numpy as np
from scipy.optimize import minimize
from typing import Dict, Optional, List
import json
from datetime import datetime

def validate_input_parameters_api(state: Dict) -> Dict:
    """Agent 1: Validate Input Parameters (API version - no Streamlit)"""
    
    coal_quality_params = state.get("coal_quality_params", {})
    target_specs = state.get("target_specifications", {})
    cost_params = state.get("cost_params", {})
    availability_constraints = state.get("availability_constraints", {})
    
    validation_result = {
        "status": "valid",
        "coal_count": len(coal_quality_params),
        "checks_passed": [],
        "warnings": [],
        "insights": [],
        "timestamp": datetime.now().isoformat()
    }
    
    # Check coal count
    if len(coal_quality_params) < 2:
        validation_result["warnings"].append("⚠️ Less than 2 coal sources provided")
        validation_result["status"] = "warning"
    else:
        validation_result["checks_passed"].append(f"✅ {len(coal_quality_params)} coal sources provided")
    
    # Check availability
    total_available = sum(availability_constraints.values())
    total_required = state.get("operational_constraints", {}).get("total_required", 0)
    
    if total_available >= total_required:
        validation_result["checks_passed"].append(f"✅ Total available ({int(total_available):,} tons) >= Required ({int(total_required):,} tons)")
        surplus = total_available - total_required
        validation_result["insights"].append(f"💡 Surplus capacity: {int(surplus):,} tons ({(surplus/total_required*100):.1f}%)")
    else:
        validation_result["warnings"].append(f"⚠️ Total available ({int(total_available):,}) < Required ({int(total_required):,})")
        validation_result["status"] = "warning"
    
    # Check target specifications
    required_targets = ["gcv_min", "ash_max", "sulfur_max", "moisture_max"]
    for target in required_targets:
        if target in target_specs:
            validation_result["checks_passed"].append(f"✅ {target.replace('_', ' ').title()}: {target_specs[target]}")
    
    # Analyze coal quality ranges
    if coal_quality_params:
        gcv_values = [params["gcv"] for params in coal_quality_params.values()]
        ash_values = [params["ash"] for params in coal_quality_params.values()]
        
        validation_result["insights"].append(f"📊 GCV Range: {min(gcv_values):.0f} - {max(gcv_values):.0f} kcal/kg")
        validation_result["insights"].append(f"📊 Ash Range: {min(ash_values):.1f}% - {max(ash_values):.1f}%")
    
    # Cost analysis
    if cost_params:
        costs = list(cost_params.values())
        avg_cost = sum(costs) / len(costs)
        validation_result["insights"].append(f"💰 Average coal cost: ${avg_cost:.2f}/ton")
    
    state["validation_result"] = validation_result
    state["agent_messages"] = state.get("agent_messages", []) + ["✅ Validation Agent completed"]
    
    return state


def generate_optimized_blend_strategy_api(state: Dict) -> Dict:
    """Agent 2: Generate Optimized Blend Strategy (API version)"""
    
    coal_quality_params = state["coal_quality_params"]
    cost_params = state["cost_params"]
    availability_constraints = state["availability_constraints"]
    target_specs = state["target_specifications"]
    operational_constraints = state["operational_constraints"]
    
    coal_names = list(coal_quality_params.keys())
    n_coals = len(coal_names)
    
    # Objective function: minimize cost
    def objective(x):
        total_cost = sum(x[i] * cost_params[coal_names[i]] for i in range(n_coals))
        return total_cost
    
    # Constraints
    constraints = []
    
    # Total quantity constraint
    total_required = operational_constraints["total_required"]
    constraints.append({
        'type': 'eq',
        'fun': lambda x: sum(x) - total_required
    })
    
    # GCV constraint
    if "gcv_min" in target_specs:
        def gcv_constraint(x):
            weighted_gcv = sum(x[i] * coal_quality_params[coal_names[i]]["gcv"] for i in range(n_coals))
            return weighted_gcv - target_specs["gcv_min"] * sum(x)
        constraints.append({'type': 'ineq', 'fun': gcv_constraint})
    
    # Ash constraint
    if "ash_max" in target_specs:
        def ash_constraint(x):
            weighted_ash = sum(x[i] * coal_quality_params[coal_names[i]]["ash"] for i in range(n_coals))
            return target_specs["ash_max"] * sum(x) - weighted_ash
        constraints.append({'type': 'ineq', 'fun': ash_constraint})
    
    # Sulfur constraint
    if "sulfur_max" in target_specs:
        def sulfur_constraint(x):
            weighted_sulfur = sum(x[i] * coal_quality_params[coal_names[i]]["sulfur"] for i in range(n_coals))
            return target_specs["sulfur_max"] * sum(x) - weighted_sulfur
        constraints.append({'type': 'ineq', 'fun': sulfur_constraint})
    
    # Moisture constraint
    if "moisture_max" in target_specs:
        def moisture_constraint(x):
            weighted_moisture = sum(x[i] * coal_quality_params[coal_names[i]]["moisture"] for i in range(n_coals))
            return target_specs["moisture_max"] * sum(x) - weighted_moisture
        constraints.append({'type': 'ineq', 'fun': moisture_constraint})
    
    # Bounds
    bounds = []
    for coal_name in coal_names:
        max_available = availability_constraints.get(coal_name, total_required)
        bounds.append((0, max_available))
    
    # Initial guess
    x0 = np.array([total_required / n_coals] * n_coals)
    
    # Optimize
    result = minimize(
        objective,
        x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'maxiter': 1000}
    )
    
    # Calculate achieved parameters
    if result.success:
        blend_quantities = result.x
        total_quantity = sum(blend_quantities)
        
        # Convert all numpy types to Python native types
        achieved_params = {
            "gcv": float(sum(blend_quantities[i] * coal_quality_params[coal_names[i]]["gcv"] for i in range(n_coals)) / total_quantity),
            "ash": float(sum(blend_quantities[i] * coal_quality_params[coal_names[i]]["ash"] for i in range(n_coals)) / total_quantity),
            "sulfur": float(sum(blend_quantities[i] * coal_quality_params[coal_names[i]]["sulfur"] for i in range(n_coals)) / total_quantity),
            "moisture": float(sum(blend_quantities[i] * coal_quality_params[coal_names[i]]["moisture"] for i in range(n_coals)) / total_quantity),
        }
        
        blend_composition = [
            {
                "coal_name": coal_names[i],
                "quantity": float(blend_quantities[i]),
                "percentage": float(blend_quantities[i] / total_quantity * 100)
            }
            for i in range(n_coals)
            if blend_quantities[i] > 0.1
        ]
        
        optimization_result = {
            "success": True,
            "total_cost": float(result.fun),
            "blend_composition": blend_composition,
            "achieved_parameters": achieved_params,
            "optimization_message": str(result.message)
        }
    else:
        optimization_result = {
            "success": False,
            "error": result.message,
            "blend_composition": [],
            "achieved_parameters": {}
        }
    
    # Add optimization insights
    if optimization_result.get("success"):
        optimization_result["insights"] = []
        
        # Blend diversity
        active_coals = len([b for b in blend_composition if b["percentage"] > 5])
        optimization_result["insights"].append(f"🎯 Using {active_coals} coal sources in blend")
        
        # Dominant coal
        if blend_composition:
            dominant = max(blend_composition, key=lambda x: x["percentage"])
            optimization_result["insights"].append(f"📊 Dominant coal: {dominant['coal_name']} ({dominant['percentage']:.1f}%)")
        
        # Parameter compliance
        achieved = optimization_result["achieved_parameters"]
        compliance_count = 0
        if achieved.get("gcv", 0) >= target_specs.get("gcv_min", 0):
            compliance_count += 1
        if achieved.get("ash", 100) <= target_specs.get("ash_max", 100):
            compliance_count += 1
        if achieved.get("sulfur", 100) <= target_specs.get("sulfur_max", 100):
            compliance_count += 1
        if achieved.get("moisture", 100) <= target_specs.get("moisture_max", 100):
            compliance_count += 1
        
        optimization_result["insights"].append(f"✅ {compliance_count}/4 parameters meet targets")
    
    state["optimized_blend_strategy"] = optimization_result
    state["agent_messages"] = state.get("agent_messages", []) + ["⚙️ Optimization Agent completed"]
    
    return state


def perform_cost_analysis_api(state: Dict) -> Dict:
    """Agent 3: Perform Cost Analysis (API version)"""
    
    optimization_result = state.get("optimized_blend_strategy", {})
    
    if not optimization_result.get("success"):
        state["cost_analysis"] = {"error": "Optimization failed"}
        return state
    
    blend_composition = optimization_result["blend_composition"]
    cost_params = state["cost_params"]
    
    cost_breakdown = []
    total_cost = 0
    
    for blend in blend_composition:
        coal_name = blend["coal_name"]
        quantity = blend["quantity"]
        unit_cost = cost_params[coal_name]
        coal_cost = quantity * unit_cost
        
        cost_breakdown.append({
            "coal": coal_name,
            "quantity": float(quantity),
            "unit_cost": float(unit_cost),
            "total_cost": float(coal_cost),
            "percentage": float((coal_cost / optimization_result["total_cost"] * 100) if optimization_result["total_cost"] > 0 else 0)
        })
        total_cost += coal_cost
    
    cost_analysis = {
        "total_cost": float(total_cost),
        "cost_breakdown": cost_breakdown,
        "cost_per_ton": float(total_cost / state["operational_constraints"]["total_required"]),
        "currency": "USD"
    }
    
    # Add cost insights
    cost_analysis["insights"] = []
    
    if cost_breakdown:
        # Most expensive coal
        most_expensive = max(cost_breakdown, key=lambda x: x["total_cost"])
        cost_analysis["insights"].append(f"💰 Highest cost component: {most_expensive['coal']} (${most_expensive['total_cost']:,.0f})")
        
        # Cost efficiency
        total_quantity = state["operational_constraints"]["total_required"]
        cost_analysis["insights"].append(f"📊 Blending efficiency: ${cost_analysis['cost_per_ton']:.2f}/ton")
        
        # Cost distribution
        if len(cost_breakdown) > 1:
            cost_variance = max(c["percentage"] for c in cost_breakdown) - min(c["percentage"] for c in cost_breakdown)
            cost_analysis["insights"].append(f"📈 Cost distribution variance: {cost_variance:.1f}%")
    
    state["cost_analysis"] = cost_analysis
    state["agent_messages"] = state.get("agent_messages", []) + ["💰 Cost Analysis Agent completed"]
    
    return state


def generate_quality_predictions_api(state: Dict) -> Dict:
    """Agent 4: Generate Quality Predictions (API version)"""
    
    optimization_result = state.get("optimized_blend_strategy", {})
    
    if not optimization_result.get("success"):
        state["quality_predictions"] = {"error": "Optimization failed"}
        return state
    
    achieved = optimization_result["achieved_parameters"]
    targets = state["target_specifications"]
    
    # Convert numpy booleans to Python booleans
    quality_predictions = {
        "achieved_parameters": achieved,
        "target_specifications": targets,
        "compliance": {
            "gcv": bool(achieved.get("gcv", 0) >= targets.get("gcv_min", 0)),
            "ash": bool(achieved.get("ash", 100) <= targets.get("ash_max", 100)),
            "sulfur": bool(achieved.get("sulfur", 100) <= targets.get("sulfur_max", 100)),
            "moisture": bool(achieved.get("moisture", 100) <= targets.get("moisture_max", 100))
        },
        "quality_score": 0
    }
    
    # Calculate quality score
    compliant_count = sum(1 for v in quality_predictions["compliance"].values() if v)
    quality_predictions["quality_score"] = float((compliant_count / len(quality_predictions["compliance"])) * 100)
    
    # Add quality insights
    quality_predictions["insights"] = []
    
    # Overall assessment
    if quality_predictions["quality_score"] >= 75:
        quality_predictions["insights"].append("🌟 Excellent quality compliance")
    elif quality_predictions["quality_score"] >= 50:
        quality_predictions["insights"].append("✅ Good quality compliance")
    else:
        quality_predictions["insights"].append("⚠️ Quality targets partially met")
    
    # Parameter-specific insights
    for param, compliant in quality_predictions["compliance"].items():
        if not compliant:
            quality_predictions["insights"].append(f"⚠️ {param.upper()} does not meet target specification")
    
    # Quality score interpretation
    quality_predictions["insights"].append(f"📊 Overall compliance: {quality_predictions['quality_score']:.0f}% of targets met")
    
    state["quality_predictions"] = quality_predictions
    state["agent_messages"] = state.get("agent_messages", []) + ["🎯 Quality Prediction Agent completed"]
    
    return state


def generate_comprehensive_report_api(state: Dict) -> Dict:
    """Agent 5: Generate Comprehensive Report (API version)"""
    
    report_sections = []
    
    # Executive Summary
    optimization_result = state.get("optimized_blend_strategy", {})
    cost_analysis = state.get("cost_analysis", {})
    quality_predictions = state.get("quality_predictions", {})
    
    if optimization_result.get("success"):
        report_sections.append({
            "title": "Executive Summary",
            "content": f"Optimization successful. Total cost: ${cost_analysis.get('total_cost', 0):,.2f}. Quality score: {quality_predictions.get('quality_score', 0):.1f}%"
        })
        
        # Blend Composition
        blend_composition = optimization_result.get("blend_composition", [])
        report_sections.append({
            "title": "Blend Composition",
            "content": blend_composition
        })
        
        # Cost Analysis
        report_sections.append({
            "title": "Cost Analysis",
            "content": cost_analysis
        })
        
        # Quality Assessment
        report_sections.append({
            "title": "Quality Assessment",
            "content": quality_predictions
        })
    else:
        report_sections.append({
            "title": "Error",
            "content": "Optimization failed"
        })
    
    # Add executive summary
    report = {
        "sections": report_sections,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_agents": 5,
            "agents_completed": len(state.get("agent_messages", [])),
            "optimization_success": optimization_result.get("success", False),
            "quality_score": quality_predictions.get("quality_score", 0),
            "total_cost": cost_analysis.get("total_cost", 0)
        }
    }
    
    state["comprehensive_report"] = report
    state["agent_messages"] = state.get("agent_messages", []) + ["📄 Report Generation Agent completed"]
    
    return state


def run_workflow_api(initial_state: Dict) -> Dict:
    """Run the complete workflow without Streamlit"""
    
    # Run agents sequentially
    state = initial_state.copy()
    
    # Agent 1: Validation
    state = validate_input_parameters_api(state)
    
    # Agent 2: Optimization
    state = generate_optimized_blend_strategy_api(state)
    
    # Agent 3: Cost Analysis
    state = perform_cost_analysis_api(state)
    
    # Agent 4: Quality Predictions
    state = generate_quality_predictions_api(state)
    
    # Agent 5: Report Generation
    state = generate_comprehensive_report_api(state)
    
    return state
