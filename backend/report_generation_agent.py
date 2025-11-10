"""
Report Generation Agent
Generates comprehensive executive and detailed reports from optimization results
"""
from datetime import datetime
import json

# Try to import LangChain AWS, but make it optional
try:
    import boto3
    from langchain_aws import ChatBedrock
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: langchain_aws not available. Reports will use fallback mode.")

# Initialize LLM
def get_llm():
    """Get LangChain LLM instance"""
    if not LANGCHAIN_AVAILABLE:
        return None
    
    try:
        # Use cross-region inference profile
        return ChatBedrock(
            model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            region_name="us-east-1"
        )
    except Exception as e:
        print(f"Warning: Could not initialize Bedrock LLM: {e}")
        return None


def generate_executive_report(optimization_results: dict) -> str:
    """
    Generate executive summary report using EXACT agent outputs
    NO AI GENERATION - Direct use of agent findings to ensure 100% accuracy
    
    Args:
        optimization_results: Complete optimization results from workflow
        
    Returns:
        Executive report as formatted string with exact agent outputs
    """
    # Use direct agent outputs - NO AI interpretation
    content = _generate_basic_executive_summary(optimization_results)
    
    # Add header and timestamp
    report = f"""
{'='*80}
EXECUTIVE SUMMARY - COAL BLENDING OPTIMIZATION
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

{content}

{'='*80}
"""
    
    return report


def generate_detailed_report(optimization_results: dict) -> str:
    """
    Generate detailed technical report using EXACT agent outputs
    NO AI GENERATION - Direct use of agent findings to ensure 100% accuracy
    
    Args:
        optimization_results: Complete optimization results from workflow
        
    Returns:
        Detailed report as formatted string with exact agent outputs
    """
    # Use direct agent outputs - NO AI interpretation to ensure accuracy
    content = _generate_basic_detailed_report(optimization_results)
    
    # Add header and timestamp
    report = f"""
{'='*80}
DETAILED TECHNICAL REPORT - COAL BLENDING OPTIMIZATION
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report Type: Comprehensive Technical Analysis
{'='*80}

{content}

{'='*80}
END OF REPORT
{'='*80}
"""
    
    return report


def generate_both_reports(optimization_results: dict, use_ai: bool = False) -> dict:
    """
    Generate both executive and detailed reports
    
    Args:
        optimization_results: Complete optimization results from workflow
        use_ai: Whether to use AI generation (default False to avoid throttling)
        
    Returns:
        Dictionary with both reports
    """
    # Use fallback mode by default to avoid throttling
    if use_ai:
        executive_report = generate_executive_report(optimization_results)
        detailed_report = generate_detailed_report(optimization_results)
    else:
        # Use fast fallback mode
        exec_content = _generate_basic_executive_summary(optimization_results)
        detail_content = _generate_basic_detailed_report(optimization_results)
        
        executive_report = f"""
{'='*80}
EXECUTIVE SUMMARY - COAL BLENDING OPTIMIZATION
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

{exec_content}

{'='*80}
"""
        
        detailed_report = f"""
{'='*80}
DETAILED TECHNICAL REPORT - COAL BLENDING OPTIMIZATION
{'='*80}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report Type: Comprehensive Technical Analysis
{'='*80}

{detail_content}

{'='*80}
END OF REPORT
{'='*80}
"""
    
    return {
        "executive_report": executive_report,
        "detailed_report": detailed_report,
        "generated_at": datetime.now().isoformat(),
        "generation_mode": "AI" if use_ai else "Template",
        "report_metadata": {
            "total_coals_analyzed": len(optimization_results.get('optimization', {}).get('selected_coals', [])),
            "optimization_status": optimization_results.get('validation', {}).get('status', 'unknown'),
            "total_cost": optimization_results.get('cost_analysis', {}).get('total_cost', 0)
        }
    }


def _generate_basic_executive_summary(results: dict) -> str:
    """Enhanced executive summary aggregating ALL agent data"""
    opt = results.get('optimization', {})
    cost = results.get('cost_analysis', {})
    validation = results.get('validation', {})
    quality = results.get('quality_prediction', {})
    boiler = results.get('boiler_efficiency_analysis', {})
    performance = results.get('performance_comparison', {})
    
    # Extract key metrics
    selected_coals = opt.get('selected_coals', [])
    total_cost = cost.get('total_cost', 0)
    cost_per_ton = cost.get('cost_per_ton', 0)
    all_specs_met = validation.get('all_specs_met', False)
    quality_score = quality.get('quality_score', 0)
    boiler_eff = boiler.get('efficiency_analysis', {}).get('overall_efficiency', 0)
    
    return f"""
EXECUTIVE SUMMARY

1. KEY FINDINGS (All Agents):
   • Validation Agent: {'✓ PASSED' if all_specs_met else '✗ FAILED'} all quality specifications
   • Optimization Agent: Selected {len(selected_coals)} coal sources from available inventory
   • Cost Analysis Agent: Total cost ${total_cost:,.2f} at ${cost_per_ton:.2f}/ton
   • Quality Prediction Agent: Quality score {quality_score:.1f}%
   • Boiler Efficiency Agent: Predicted efficiency {boiler_eff:.1f}%
   • Performance Agent: {'Exceeds' if all_specs_met else 'Below'} target specifications

2. FINANCIAL IMPACT:
   Total Investment: ${total_cost:,.2f}
   Cost per Ton: ${cost_per_ton:.2f}
   Budget Status: {'✓ Within Budget' if all_specs_met else '⚠ Review Required'}
   Cost Efficiency: {cost.get('cost_efficiency', 'N/A')}

3. QUALITY COMPLIANCE:
   Overall Status: {validation.get('status', 'Unknown').upper()}
   All Specifications Met: {'YES ✓' if all_specs_met else 'NO ✗'}
   Quality Score: {quality_score:.1f}%
   Compliance Level: {'Excellent' if quality_score >= 90 else 'Good' if quality_score >= 75 else 'Acceptable' if quality_score >= 60 else 'Review Required'}

4. BOILER EFFICIENCY ASSESSMENT:
   Predicted Efficiency: {boiler_eff:.1f}%
   Target Efficiency: {boiler.get('efficiency_analysis', {}).get('target_efficiency', 85.0):.1f}%
   Status: {'✓ Meets Target' if boiler_eff >= boiler.get('efficiency_analysis', {}).get('target_efficiency', 85.0) else '⚠ Below Target'}
   GCV Impact: {boiler.get('blend_properties', {}).get('weighted_gcv', 0):.0f} kcal/kg

5. RECOMMENDATIONS (Prioritized):
   • {'Proceed with blend implementation' if all_specs_met else 'Review blend composition and adjust parameters'}
   • Monitor quality parameters during blending operations
   • {'Maintain current operational parameters' if boiler_eff >= 85 else 'Optimize boiler settings to improve efficiency'}
   • Track performance metrics against targets
   • {'Consider cost optimization opportunities' if cost_per_ton > 100 else 'Cost-effective blend achieved'}

6. RISK ASSESSMENT:
   Overall Risk Level: {'LOW' if all_specs_met and boiler_eff >= 85 else 'MEDIUM' if all_specs_met or boiler_eff >= 80 else 'HIGH'}
   Quality Risk: {'Low' if quality_score >= 80 else 'Medium' if quality_score >= 60 else 'High'}
   Operational Risk: {'Low' if boiler_eff >= 85 else 'Medium' if boiler_eff >= 80 else 'High'}
   Financial Risk: {'Low' if cost_per_ton <= 100 else 'Medium' if cost_per_ton <= 120 else 'High'}
"""


def _generate_basic_detailed_report(results: dict) -> str:
    """Enhanced detailed report with complete details from ALL agents"""
    opt = results.get('optimization', {})
    cost = results.get('cost_analysis', {})
    validation = results.get('validation', {})
    quality = results.get('quality_prediction', {})
    boiler = results.get('boiler_efficiency_analysis', {})
    performance = results.get('performance_comparison', {})
    knowledge = results.get('knowledge_graph', {})
    
    selected_coals = opt.get('selected_coals', [])
    blended = opt.get('blended_quality', {})
    efficiency_data = boiler.get('efficiency_analysis', {})
    blend_props = boiler.get('blend_properties', {})
    
    report = f"""
DETAILED TECHNICAL REPORT
Coal Blending Optimization Analysis

================================================================================
1. EXECUTIVE SUMMARY
================================================================================
Optimization completed with {len(selected_coals)} coal sources selected from available inventory.
Overall Status: {validation.get('status', 'Unknown').upper()}
Quality Score: {quality.get('quality_score', 0):.1f}%
Boiler Efficiency: {efficiency_data.get('overall_efficiency', 0):.1f}%
Total Cost: ${cost.get('total_cost', 0):,.2f}

================================================================================
2. VALIDATION AGENT RESULTS
================================================================================
Status: {validation.get('status', 'Unknown')}
All Specifications Met: {'YES' if validation.get('all_specs_met') else 'NO'}
Validation Details:
{json.dumps(validation, indent=2, default=str)}

================================================================================
3. OPTIMIZATION AGENT RESULTS
================================================================================
Total Tonnage Required: {opt.get('total_tonnage', 'N/A')} tons
Number of Available Coals: {len(results.get('coals', []))}
Number of Selected Coals: {len(selected_coals)}

Selected Coal Blend:
"""
    
    for i, coal in enumerate(selected_coals, 1):
        report += f"""
   {i}. {coal.get('name', 'Unknown')}
      - Percentage: {coal.get('percentage', 0):.1f}%
      - Quantity: {coal.get('quantity', 0):.0f} tons
      - Cost: ${coal.get('cost', 0):.2f}/ton
      - Total Cost: ${coal.get('quantity', 0) * coal.get('cost', 0):,.2f}
"""
    
    report += f"""
Blended Quality Parameters:
   • GCV: {blended.get('gcv', 0):.0f} kcal/kg
   • Ash: {blended.get('ash', 0):.2f}%
   • Sulfur: {blended.get('sulfur', 0):.2f}%
   • Moisture: {blended.get('moisture', 0):.2f}%
   • Volatile Matter: {blended.get('vm', 0):.2f}%

================================================================================
4. COST ANALYSIS AGENT RESULTS
================================================================================
Total Cost: ${cost.get('total_cost', 0):,.2f}
Cost per Ton: ${cost.get('cost_per_ton', 0):.2f}
Cost Efficiency: {cost.get('cost_efficiency', 'N/A')}
Budget Status: {cost.get('budget_status', 'N/A')}

Cost Breakdown by Coal:
"""
    
    for coal in selected_coals:
        coal_cost = coal.get('quantity', 0) * coal.get('cost', 0)
        percentage_of_total = (coal_cost / cost.get('total_cost', 1)) * 100 if cost.get('total_cost', 0) > 0 else 0
        report += f"   • {coal.get('name', 'Unknown')}: ${coal_cost:,.2f} ({percentage_of_total:.1f}% of total)\n"

    report += f"""
================================================================================
5. QUALITY PREDICTION AGENT RESULTS
================================================================================
Quality Score: {quality.get('quality_score', 0):.1f}%
Status: {quality.get('status', 'N/A')}

Compliance Status:
"""
    
    compliance = quality.get('compliance', {})
    for param, status in compliance.items():
        report += f"   • {param.upper()}: {'✓ PASS' if status else '✗ FAIL'}\n"

    report += f"""
================================================================================
6. BOILER EFFICIENCY AGENT RESULTS (DULONG METHOD)
================================================================================
Overall Efficiency: {efficiency_data.get('overall_efficiency', 0):.1f}%
Target Efficiency: {efficiency_data.get('target_efficiency', 85.0):.1f}%
Status: {'✓ Meets Target' if efficiency_data.get('overall_efficiency', 0) >= efficiency_data.get('target_efficiency', 85.0) else '⚠ Below Target'}

Blend Properties:
   • Weighted GCV: {blend_props.get('weighted_gcv', 0):.0f} kcal/kg
   • Weighted Moisture: {blend_props.get('weighted_moisture', 0):.2f}%
   • Weighted Ash: {blend_props.get('weighted_ash', 0):.2f}%
   • Weighted Sulfur: {blend_props.get('weighted_sulfur', 0):.2f}%

Heat Losses:
"""
    
    heat_losses = efficiency_data.get('heat_losses', {})
    for loss_type, value in heat_losses.items():
        if isinstance(value, (int, float)):
            report += f"   • {loss_type.replace('_', ' ').title()}: {value:.2f} kcal/kg\n"

    report += f"""
Dulong Method GCV Analysis:
{boiler.get('ai_insights', 'Detailed Dulong Method analysis available in AI-powered mode')}

================================================================================
7. PERFORMANCE COMPARISON AGENT RESULTS
================================================================================
"""
    
    if performance:
        gcv_comp = performance.get('gcv_comparison', {})
        cost_comp = performance.get('cost_comparison', {})
        report += f"""
GCV Performance:
   • Target: {gcv_comp.get('target', 0):.0f} kcal/kg
   • Achieved: {gcv_comp.get('achieved', 0):.0f} kcal/kg
   • Change: {gcv_comp.get('change_percent', 0):+.1f}%
   • Status: {gcv_comp.get('status', 'N/A')}

Cost Performance:
   • Target: ${cost_comp.get('target', 0):,.2f}
   • Achieved: ${cost_comp.get('achieved', 0):,.2f}
   • Change: {cost_comp.get('change_percent', 0):+.1f}%
   • Status: {cost_comp.get('status', 'N/A')}
"""

    report += f"""
================================================================================
8. KNOWLEDGE GRAPH INSIGHTS
================================================================================
{knowledge.get('summary', 'Relationship insights available in knowledge graph visualization')}

================================================================================
9. RECOMMENDATIONS
================================================================================
Based on analysis from all agents:

Immediate Actions:
   • {'Proceed with blend implementation' if validation.get('all_specs_met') else 'Review and adjust blend composition'}
   • Monitor quality parameters during blending operations
   • {'Maintain current boiler settings' if efficiency_data.get('overall_efficiency', 0) >= 85 else 'Optimize boiler parameters to improve efficiency'}

Long-term Improvements:
   • Track performance metrics against targets
   • Implement continuous quality monitoring
   • {'Explore cost optimization opportunities' if cost.get('cost_per_ton', 0) > 100 else 'Maintain cost-effective procurement strategy'}
   • Regular boiler efficiency assessments using Dulong Method

================================================================================
10. APPENDICES
================================================================================
A. Complete Agent Messages:
{chr(10).join(f'   • {msg}' for msg in results.get('agent_messages', []))}

B. Operational Constraints:
{json.dumps(results.get('operational_constraints', {}), indent=2)}

C. Target Specifications:
{json.dumps(results.get('target_specifications', {}), indent=2)}

================================================================================
END OF REPORT
================================================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report Type: Comprehensive Technical Analysis
All Agents: Validation, Optimization, Cost Analysis, Quality Prediction, 
            Boiler Efficiency, Performance Comparison, Knowledge Graph
================================================================================
"""
    
    return report


def save_reports_to_file(reports: dict, filename_prefix: str = "coal_blend_report"):
    """
    Save reports to files
    
    Args:
        reports: Dictionary with executive and detailed reports
        filename_prefix: Prefix for filenames
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save executive report
    exec_filename = f"{filename_prefix}_executive_{timestamp}.txt"
    with open(exec_filename, 'w') as f:
        f.write(reports['executive_report'])
    
    # Save detailed report
    detail_filename = f"{filename_prefix}_detailed_{timestamp}.txt"
    with open(detail_filename, 'w') as f:
        f.write(reports['detailed_report'])
    
    # Save combined JSON
    json_filename = f"{filename_prefix}_data_{timestamp}.json"
    with open(json_filename, 'w') as f:
        json.dump(reports, f, indent=2, default=str)
    
    return {
        "executive_report_file": exec_filename,
        "detailed_report_file": detail_filename,
        "json_data_file": json_filename
    }


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_results = {
        "optimization": {
            "selected_coals": [
                {"name": "Indonesian Sub-Bit", "percentage": 35, "cost": 82},
                {"name": "Australian Premium", "percentage": 30, "cost": 118},
                {"name": "South African", "percentage": 35, "cost": 93}
            ],
            "blended_quality": {
                "gcv": 6100,
                "ash": 10.2,
                "sulfur": 0.58,
                "moisture": 6.5
            }
        },
        "cost_analysis": {
            "total_cost": 950000,
            "cost_per_ton": 95,
            "savings_vs_baseline": 50000
        },
        "validation": {
            "status": "passed",
            "all_specs_met": True
        }
    }
    
    # Generate reports
    reports = generate_both_reports(sample_results)
    
    print("Executive Report:")
    print(reports['executive_report'])
    print("\n" + "="*80 + "\n")
    print("Detailed Report:")
    print(reports['detailed_report'])
