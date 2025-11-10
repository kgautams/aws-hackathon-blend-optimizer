"""
Clean Knowledge Graph Agent - Complete Rewrite
Generates a knowledge graph showing relationships between coal sources, blend, and parameters
"""

from typing import Dict, List, Any
from datetime import datetime


class KnowledgeGraphAgent:
    """Agent 7: Knowledge Graph Visualization of Parameter Relationships"""
    
    name = "Knowledge Graph Agent"
    description = "Creates knowledge graph showing relationships between parameters"
    
    def run(self, state) -> Dict[str, Any]:
        """Execute knowledge graph generation"""
        print(f"🕸️ {self.name}: Building knowledge graph...")
        
        try:
            # Extract data from state
            coal_quality_params = state.data.get("coal_quality_params", {})
            cost_params = state.data.get("cost_params", {})
            optimization_result = state.data.get("optimized_blend_strategy", {})
            target_specs = state.data.get("target_specifications", {})
            operational = state.data.get("operational_constraints", {})
            
            # Check if optimization succeeded
            if not optimization_result or not optimization_result.get("success"):
                print(f"⚠️ {self.name}: Optimization did not succeed, returning empty graph")
                return self._empty_graph("Optimization did not succeed")
            
            blend_composition = optimization_result.get("blend_composition", [])
            achieved_params = optimization_result.get("achieved_parameters", {})
            
            if not blend_composition:
                print(f"⚠️ {self.name}: No blend composition found")
                return self._empty_graph("No blend composition available")
            
            # Build graph
            nodes = []
            edges = []
            
            # 1. Central Blend Node
            nodes.append({
                "id": "blend",
                "label": "Optimized Blend",
                "type": "result",
                "properties": {
                    "gcv": round(achieved_params.get("gcv", 0), 2),
                    "ash": round(achieved_params.get("ash", 0), 2),
                    "sulfur": round(achieved_params.get("sulfur", 0), 2),
                    "moisture": round(achieved_params.get("moisture", 0), 2),
                    "cost_per_ton": round(achieved_params.get("cost_per_ton", 0), 2),
                    "total_cost": round(optimization_result.get("total_cost", 0), 2)
                }
            })
            
            # 2. Coal Source Nodes
            for blend in blend_composition:
                coal_name = blend.get("coal_name", "Unknown")
                coal_id = f"coal_{coal_name.replace(' ', '_').lower()}"
                coal_props = coal_quality_params.get(coal_name, {})
                coal_cost = cost_params.get(coal_name, 0)
                
                nodes.append({
                    "id": coal_id,
                    "label": coal_name,
                    "type": "coal_source",
                    "properties": {
                        "percentage": round(blend.get("percentage", 0), 2),
                        "quantity_tons": round(blend.get("quantity", 0), 2),
                        "gcv": round(coal_props.get("gcv", 0), 2),
                        "ash": round(coal_props.get("ash", 0), 2),
                        "sulfur": round(coal_props.get("sulfur", 0), 2),
                        "moisture": round(coal_props.get("moisture", 0), 2),
                        "cost_per_ton": round(coal_cost, 2)
                    }
                })
                
                # Edge: Coal → Blend
                edges.append({
                    "source": coal_id,
                    "target": "blend",
                    "relationship": "contributes_to",
                    "label": f"{blend.get('percentage', 0):.1f}%"
                })
            
            # 3. Parameter Nodes
            parameters = [
                ("gcv", "GCV (Energy)", "kcal/kg", target_specs.get("gcv_min", 0)),
                ("ash", "Ash Content", "%", target_specs.get("ash_max", 0)),
                ("sulfur", "Sulfur Content", "%", target_specs.get("sulfur_max", 0)),
                ("moisture", "Moisture Content", "%", target_specs.get("moisture_max", 0)),
                ("cost", "Total Cost", "USD", None)
            ]
            
            for param_id, param_label, unit, target in parameters:
                achieved = achieved_params.get(param_id, 0)
                if param_id == "cost":
                    achieved = optimization_result.get("total_cost", 0)
                
                node_props = {
                    "achieved": round(achieved, 2),
                    "unit": unit
                }
                if target is not None:
                    node_props["target"] = round(target, 2)
                
                nodes.append({
                    "id": f"param_{param_id}",
                    "label": param_label,
                    "type": "parameter",
                    "properties": node_props
                })
                
                # Edge: Blend → Parameter
                edges.append({
                    "source": "blend",
                    "target": f"param_{param_id}",
                    "relationship": "achieves",
                    "label": f"{achieved:.1f}"
                })
            
            # 4. Constraint Nodes
            nodes.append({
                "id": "constraints",
                "label": "Quality Constraints",
                "type": "constraint",
                "properties": {
                    "gcv_min": round(target_specs.get("gcv_min", 0), 2),
                    "ash_max": round(target_specs.get("ash_max", 0), 2),
                    "sulfur_max": round(target_specs.get("sulfur_max", 0), 2),
                    "moisture_max": round(target_specs.get("moisture_max", 0), 2)
                }
            })
            
            nodes.append({
                "id": "objective",
                "label": "Cost Minimization",
                "type": "objective",
                "properties": {
                    "goal": "minimize",
                    "achieved": round(optimization_result.get("total_cost", 0), 2)
                }
            })
            
            # Edges: Constraints → Blend
            edges.append({
                "source": "constraints",
                "target": "blend",
                "relationship": "constrains",
                "label": "quality limits"
            })
            
            edges.append({
                "source": "objective",
                "target": "blend",
                "relationship": "optimizes",
                "label": "minimize cost"
            })
            
            # Generate insights
            insights = [
                f"Blend uses {len(blend_composition)} coal sources",
                f"Achieved GCV: {achieved_params.get('gcv', 0):.1f} kcal/kg",
                f"Total cost: ${optimization_result.get('total_cost', 0):,.2f}",
                f"All quality constraints satisfied" if optimization_result.get("success") else "Some constraints not met"
            ]
            
            # Build final result
            result = {
                "nodes": nodes,
                "edges": edges,
                "metadata": {
                    "total_nodes": len(nodes),
                    "total_edges": len(edges),
                    "coal_sources": len(blend_composition),
                    "parameters": len(parameters),
                    "constraints": 2
                },
                "insights": insights,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ {self.name}: Generated graph with {len(nodes)} nodes and {len(edges)} edges")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error - {str(e)}")
            import traceback
            traceback.print_exc()
            return self._empty_graph(f"Error: {str(e)}")
    
    def _empty_graph(self, reason: str) -> Dict[str, Any]:
        """Return an empty graph structure"""
        return {
            "nodes": [],
            "edges": [],
            "metadata": {
                "total_nodes": 0,
                "total_edges": 0,
                "coal_sources": 0,
                "parameters": 0,
                "constraints": 0
            },
            "insights": [reason],
            "timestamp": datetime.now().isoformat()
        }
