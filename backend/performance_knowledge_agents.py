"""
Additional Agents for Performance Comparison and Knowledge Graph Visualization
Agent 6: Performance Comparison Agent - Target vs Achieved with bar graphs
Agent 7: Knowledge Graph Agent - Parameter relationships visualization
"""

from typing import Dict, List, Any
from datetime import datetime
import json


class PerformanceComparisonAgent:
    """Agent 6: Performance Comparison Analysis with Visualizations"""
    
    name = "Performance Comparison Agent"
    description = "Analyzes target vs achieved metrics with visual comparisons"
    
    def run(self, state) -> Dict[str, Any]:
        """Execute performance comparison analysis"""
        print(f"🎯 {self.name}: Analyzing performance metrics...")
        
        optimization_result = state.data.get("optimized_blend_strategy", {})
        target_specs = state.data.get("target_specifications", {})
        operational = state.data.get("operational_constraints", {})
        
        if not optimization_result.get("success"):
            return {"error": "Optimization failed"}
        
        achieved_params = optimization_result.get("achieved_parameters", {})
        total_cost = optimization_result.get("total_cost", 0)
        
        # Calculate target cost (if we used cheapest coal only)
        cost_params = state.data.get("cost_params", {})
        min_cost = min(cost_params.values()) if cost_params else 0
        target_cost = min_cost * operational.get("total_required", 0)
        
        # GCV Comparison
        target_gcv = target_specs.get("gcv_min", 0)
        achieved_gcv = achieved_params.get("gcv", 0)
        gcv_change = ((achieved_gcv - target_gcv) / target_gcv * 100) if target_gcv > 0 else 0
        
        # Cost Comparison
        cost_change = ((total_cost - target_cost) / target_cost * 100) if target_cost > 0 else 0
        
        # Ash Comparison (lower is better)
        target_ash = target_specs.get("ash_max", 0)
        achieved_ash = achieved_params.get("ash", 0)
        ash_improvement = ((target_ash - achieved_ash) / target_ash * 100) if target_ash > 0 else 0
        
        # Sulfur Comparison (lower is better)
        target_sulfur = target_specs.get("sulfur_max", 0)
        achieved_sulfur = achieved_params.get("sulfur", 0)
        sulfur_improvement = ((target_sulfur - achieved_sulfur) / target_sulfur * 100) if target_sulfur > 0 else 0
        
        # Moisture Comparison (lower is better)
        target_moisture = target_specs.get("moisture_max", 0)
        achieved_moisture = achieved_params.get("moisture", 0)
        moisture_improvement = ((target_moisture - achieved_moisture) / target_moisture * 100) if target_moisture > 0 else 0
        
        performance_data = {
            "gcv_comparison": {
                "target": float(target_gcv),
                "achieved": float(achieved_gcv),
                "change_percent": float(gcv_change),
                "status": "exceeded" if gcv_change > 0 else "met" if gcv_change == 0 else "below"
            },
            "cost_comparison": {
                "target": float(target_cost),
                "achieved": float(total_cost),
                "change_percent": float(cost_change),
                "status": "higher" if cost_change > 0 else "lower" if cost_change < 0 else "equal"
            },
            "ash_comparison": {
                "target": float(target_ash),
                "achieved": float(achieved_ash),
                "improvement_percent": float(ash_improvement),
                "status": "better" if ash_improvement > 0 else "met" if ash_improvement == 0 else "worse"
            },
            "sulfur_comparison": {
                "target": float(target_sulfur),
                "achieved": float(achieved_sulfur),
                "improvement_percent": float(sulfur_improvement),
                "status": "better" if sulfur_improvement > 0 else "met" if sulfur_improvement == 0 else "worse"
            },
            "moisture_comparison": {
                "target": float(target_moisture),
                "achieved": float(achieved_moisture),
                "improvement_percent": float(moisture_improvement),
                "status": "better" if moisture_improvement > 0 else "met" if moisture_improvement == 0 else "worse"
            },
            "overall_performance": {
                "quality_score": float((gcv_change + ash_improvement + sulfur_improvement + moisture_improvement) / 4),
                "cost_efficiency": float(100 - abs(cost_change)) if abs(cost_change) < 100 else 0
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate insights
        insights = []
        
        if gcv_change > 5:
            insights.append(f"✅ GCV exceeded target by {gcv_change:.1f}% - excellent energy content")
        elif gcv_change > 0:
            insights.append(f"✅ GCV met target with {gcv_change:.1f}% margin")
        else:
            insights.append(f"⚠️ GCV below target by {abs(gcv_change):.1f}%")
        
        if cost_change < 10:
            insights.append(f"💰 Cost optimized within {cost_change:.1f}% of minimum possible")
        elif cost_change < 20:
            insights.append(f"💰 Cost is {cost_change:.1f}% higher than minimum (quality trade-off)")
        else:
            insights.append(f"⚠️ Cost is {cost_change:.1f}% higher than minimum")
        
        if ash_improvement > 10:
            insights.append(f"🌟 Ash content {ash_improvement:.1f}% better than target")
        
        if sulfur_improvement > 10:
            insights.append(f"🌟 Sulfur content {sulfur_improvement:.1f}% better than target")
        
        performance_data["insights"] = insights
        
        print(f"✅ {self.name}: Performance analysis complete")
        return performance_data


class KnowledgeGraphAgent:
    """Agent 7: Knowledge Graph Visualization of Parameter Relationships"""
    
    name = "Knowledge Graph Agent"
    description = "Creates knowledge graph showing relationships between parameters"
    
    def run(self, state) -> Dict[str, Any]:
        """Execute knowledge graph generation"""
        print(f"🕸️ {self.name}: Building knowledge graph...")
        
        try:
            coal_quality_params = state.data.get("coal_quality_params", {})
            cost_params = state.data.get("cost_params", {})
            optimization_result = state.data.get("optimized_blend_strategy", {})
            target_specs = state.data.get("target_specifications", {})
            operational = state.data.get("operational_constraints", {})
            
            if not optimization_result.get("success"):
                return {
                    "error": "Optimization failed",
                    "nodes": [],
                    "edges": [],
                    "metadata": {"total_nodes": 0, "total_edges": 0},
                    "insights": ["Optimization did not succeed"]
                }
            
            blend_composition = optimization_result.get("blend_composition", [])
            achieved_params = optimization_result.get("achieved_parameters", {})
            
            # Build knowledge graph structure
            nodes = []
            edges = []
            
            # Central node: Optimized Blend
            nodes.append({
                "id": "optimized_blend",
                "label": "Optimized Blend",
                "type": "result",
                "properties": {
                    "gcv": float(achieved_params.get("gcv", 0)),
                    "ash": float(achieved_params.get("ash", 0)),
                    "sulfur": float(achieved_params.get("sulfur", 0)),
                    "moisture": float(achieved_params.get("moisture", 0)),
                    "cost_per_ton": float(achieved_params.get("cost_per_ton", 0)),
                    "total_cost": float(optimization_result.get("total_cost", 0))
                }
            })
            
            # Coal source nodes with ALL properties
            for blend in blend_composition:
                coal_name = blend["coal_name"]
                coal_id = f"coal_{coal_name.replace(' ', '_').lower()}"
                coal_props = coal_quality_params.get(coal_name, {})
                
                nodes.append({
                    "id": coal_id,
                    "label": coal_name,
                    "type": "coal_source",
                    "properties": {
                        "percentage": float(blend["percentage"]),
                        "quantity_tons": float(blend["quantity"]),
                        "gcv": float(coal_props.get("gcv", 0)),
                        "ash": float(coal_props.get("ash", 0)),
                        "sulfur": float(coal_props.get("sulfur", 0)),
                        "moisture": float(coal_props.get("moisture", 0)),
                        "cost_per_ton": float(cost_params.get(coal_name, 0)),
                        "total_cost": float(blend["quantity"] * cost_params.get(coal_name, 0))
                    }
                })
                
                # Edge from coal to blend
                edges.append({
                    "source": coal_id,
                    "target": "optimized_blend",
                    "relationship": "contributes_to",
                    "weight": float(blend["percentage"] / 100),
                    "label": f"{blend['percentage']:.1f}%"
                })
            
            # Parameter nodes - simplified
            parameter_nodes = [
            {
                "id": "param_gcv",
                "label": "GCV (Energy)",
                "type": "parameter",
                "properties": {
                    "target": float(target_specs.get("gcv_min", 0)),
                    "achieved": float(achieved_params.get("gcv", 0)),
                    "unit": "kcal/kg"
                }
            },
            {
                "id": "param_ash",
                "label": "Ash Content",
                "type": "parameter",
                "properties": {
                    "target": float(target_specs.get("ash_max", 0)),
                    "achieved": float(achieved_params.get("ash", 0)),
                    "unit": "%"
                }
            },
            {
                "id": "param_sulfur",
                "label": "Sulfur Content",
                "type": "parameter",
                "properties": {
                    "target": float(target_specs.get("sulfur_max", 0)),
                    "achieved": float(achieved_params.get("sulfur", 0)),
                    "unit": "%"
                }
            },
            {
                "id": "param_moisture",
                "label": "Moisture Content",
                "type": "parameter",
                "properties": {
                    "target": float(target_specs.get("moisture_max", 0)),
                    "achieved": float(achieved_params.get("moisture", 0)),
                    "unit": "%"
                }
            },
            {
                "id": "param_cost",
                "label": "Total Cost",
                "type": "parameter",
                "properties": {
                    "achieved": float(optimization_result.get("total_cost", 0)),
                    "unit": "USD"
                }
            }
            ]
        
            nodes.extend(parameter_nodes)
        
            # Edges from blend to parameters
            for param in parameter_nodes:
            edges.append({
                "source": "optimized_blend",
                "target": param["id"],
                "relationship": "achieves",
                "label": "results in"
            })
        
            # Constraint nodes - simplified
            constraint_nodes = [
            {
                "id": "constraint_quality",
                "label": "Quality Targets",
                "type": "constraint",
                "properties": {
                    "gcv_min": float(target_specs.get("gcv_min", 0)),
                    "ash_max": float(target_specs.get("ash_max", 0)),
                    "sulfur_max": float(target_specs.get("sulfur_max", 0)),
                    "moisture_max": float(target_specs.get("moisture_max", 0))
                }
            },
            {
                "id": "objective_cost",
                "label": "Cost Minimization",
                "type": "objective",
                "properties": {
                    "objective": "minimize",
                    "achieved": float(optimization_result.get("total_cost", 0))
                }
            }
            ]
        
            nodes.extend(constraint_nodes)
        
            # Edges from constraints to blend
            edges.append({
            "source": "constraint_quality",
            "target": "optimized_blend",
            "relationship": "constrains",
            "label": "quality targets"
            })
        
            edges.append({
            "source": "objective_cost",
            "target": "optimized_blend",
            "relationship": "optimizes",
            "label": "minimize cost"
            })
        
            # Generate Gremlin visualization code
            gremlin_code = self._generate_gremlin_code(nodes, edges)
        
            # Generate Cypher visualization code (Neo4j)
            cypher_code = self._generate_cypher_code(nodes, edges)
        
            # Generate D3.js compatible format
            d3_format = self._generate_d3_format(nodes, edges)
        
            knowledge_graph = {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "coal_sources": len(blend_composition),
                "parameters": len(parameter_nodes),
                "constraints": len(constraint_nodes)
            },
            "insights": [
                f"Knowledge graph contains {len(nodes)} nodes and {len(edges)} relationships",
                f"Blend uses {len(blend_composition)} coal sources with complex interdependencies",
                f"Each parameter is influenced by multiple coal sources and constraints",
                "Cost optimization balances quality targets with availability limits"
            ],
            "visualization": {
                "gremlin": gremlin_code,
                "cypher": cypher_code,
                "d3_format": d3_format
            },
            "timestamp": datetime.now().isoformat()
            }
        
            print(f"✅ {self.name}: Knowledge graph generated with {len(nodes)} nodes and {len(edges)} edges")
            return knowledge_graph
            
            except Exception as e:
            print(f"❌ {self.name}: Error generating knowledge graph: {e}")
            import traceback
            traceback.print_exc()
            return {
                "error": str(e),
                "nodes": [],
                "edges": [],
                "metadata": {"total_nodes": 0, "total_edges": 0},
                "insights": [f"Knowledge graph generation failed: {str(e)}"],
                "visualization": {
                    "d3_format": {"nodes": [], "links": []},
                    "gremlin": "",
                    "cypher": ""
                }
            }
    
    def _generate_gremlin_code(self, nodes: List[Dict], edges: List[Dict]) -> str:
        """Generate Gremlin graph traversal code for visualization"""
        gremlin_lines = [
            "// Gremlin Graph Traversal Code for Coal Blending Knowledge Graph",
            "// Compatible with Apache TinkerPop, AWS Neptune, Azure Cosmos DB",
            "",
            "// Clear existing graph (optional)",
            "g.V().drop().iterate()",
            "",
            "// Create vertices (nodes)"
        ]
        
        for node in nodes:
            props = []
            if "properties" in node:
                for key, value in node["properties"].items():
                    if isinstance(value, (int, float)):
                        props.append(f"property('{key}', {value})")
                    else:
                        props.append(f"property('{key}', '{value}')")
            
            props_str = ", " + ", ".join(props) if props else ""
            gremlin_lines.append(
                f"g.addV('{node['type']}').property('id', '{node['id']}').property('label', '{node['label']}'){props_str}.next()"
            )
        
        gremlin_lines.extend([
            "",
            "// Create edges (relationships)"
        ])
        
        for edge in edges:
            weight = edge.get('weight', 1.0)
            label = edge.get('label', edge['relationship'])
            gremlin_lines.append(
                f"g.V().has('id', '{edge['source']}').addE('{edge['relationship']}').to(g.V().has('id', '{edge['target']}')).property('weight', {weight}).property('label', '{label}').next()"
            )
        
        gremlin_lines.extend([
            "",
            "// Query examples:",
            "// Find all coal sources contributing to the blend",
            "g.V().hasLabel('coal_source').values('label')",
            "",
            "// Find parameters affected by the optimized blend",
            "g.V().has('id', 'optimized_blend').out('determines').values('label')",
            "",
            "// Find contribution percentages",
            "g.V().hasLabel('coal_source').outE('contributes_to').values('weight')",
            "",
            "// Find all constraints",
            "g.V().hasLabel('constraint').values('label')"
        ])
        
        return "\n".join(gremlin_lines)
    
    def _generate_cypher_code(self, nodes: List[Dict], edges: List[Dict]) -> str:
        """Generate Cypher query code for Neo4j visualization"""
        cypher_lines = [
            "// Cypher Query Code for Coal Blending Knowledge Graph",
            "// Compatible with Neo4j Graph Database",
            "",
            "// Clear existing graph (optional)",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// Create nodes"
        ]
        
        for node in nodes:
            props = [f"id: '{node['id']}'", f"label: '{node['label']}'", f"type: '{node['type']}'"]
            if "properties" in node:
                for key, value in node["properties"].items():
                    if isinstance(value, (int, float)):
                        props.append(f"{key}: {value}")
                    else:
                        props.append(f"{key}: '{value}'")
            
            props_str = ", ".join(props)
            cypher_lines.append(f"CREATE (:{node['type']} {{{props_str}}})")
        
        cypher_lines.extend([
            "",
            "// Create relationships"
        ])
        
        for edge in edges:
            weight = edge.get('weight', 1.0)
            label = edge.get('label', edge['relationship'])
            cypher_lines.append(
                f"MATCH (a {{id: '{edge['source']}'}}), (b {{id: '{edge['target']}'}}) "
                f"CREATE (a)-[:{edge['relationship'].upper()} {{weight: {weight}, label: '{label}'}}]->(b)"
            )
        
        cypher_lines.extend([
            "",
            "// Query examples:",
            "// Find all coal sources",
            "MATCH (n:coal_source) RETURN n.label;",
            "",
            "// Find blend composition with percentages",
            "MATCH (c:coal_source)-[r:CONTRIBUTES_TO]->(b:result) RETURN c.label, r.weight;",
            "",
            "// Find parameter relationships",
            "MATCH (b:result)-[r:DETERMINES]->(p:parameter) RETURN p.label, p.achieved;"
        ])
        
        return "\n".join(cypher_lines)
    
    def _generate_d3_format(self, nodes: List[Dict], edges: List[Dict]) -> Dict:
        """Generate D3.js force-directed graph format"""
        d3_nodes = []
        for i, node in enumerate(nodes):
            d3_node = {
                "id": node["id"],
                "name": node["label"],
                "type": node["type"],
                "group": self._get_node_group(node["type"])
            }
            if "properties" in node:
                d3_node["properties"] = node["properties"]
            d3_nodes.append(d3_node)
        
        d3_links = []
        for edge in edges:
            d3_links.append({
                "source": edge["source"],
                "target": edge["target"],
                "type": edge["relationship"],
                "value": edge.get("weight", 1.0),
                "label": edge.get("label", "")
            })
        
        return {
            "nodes": d3_nodes,
            "links": d3_links
        }
    
    def _get_node_group(self, node_type: str) -> int:
        """Assign group number for D3.js coloring"""
        groups = {
            "result": 1,
            "coal_source": 2,
            "parameter": 3,
            "constraint": 4,
            "objective": 5
        }
        return groups.get(node_type, 0)
