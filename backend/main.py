"""
FastAPI Backend for Coal Blending Optimization System
Integrates with Strands AI Framework and Amazon Bedrock Claude 4 Sonnet
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
from datetime import datetime
import json
import uuid

# Import workflows
from agentic_workflow_parallel import run_workflow_parallel as run_workflow_traditional
from agentic_workflow_llm_parallel import run_llm_workflow_parallel  # Default: LLM-powered PARALLEL

app = FastAPI(title="Coal Blending Optimizer API")

# Store workflow status in memory (use Redis/DB for production)
workflow_status = {}

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://main.d3ozheb5d4fqf2.amplifyapp.com",
        "https://*.amplifyapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CoalSource(BaseModel):
    name: str
    ash: float
    sulfur: float
    moisture: float
    gcv: float
    cost: float
    available: float

class TargetSpecs(BaseModel):
    ash_max: float
    sulfur_max: float
    moisture_max: float
    gcv_min: float

class OptimizationRequest(BaseModel):
    coal_sources: List[CoalSource]
    target_specs: TargetSpecs
    total_required: float
    target_boiler_efficiency: Optional[float] = 85.0  # Default to 85% if not provided

class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict] = None

class AgenticChatRequest(BaseModel):
    message: str
    app_context: Optional[Dict] = None

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    print("Coal Blending Optimizer API started")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Coal Blending Optimizer API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

async def run_workflow_with_status(workflow_id: str, initial_state: Dict):
    """Run workflow and update status"""
    
    # Agent progress mapping (7 agents - MAXIMUM PARALLEL execution)
    # Sequential: Validation (15%) -> Optimization (30%)
    # Parallel: Quality, Cost, Boiler, Performance, Knowledge ALL run together (30% -> 100%)
    agent_progress_map = {
        "Validation Agent": 15,
        "Optimization Agent": 30,
        # All 5 agents run in parallel (all update to 100%)
        "Quality Prediction Agent": 100,
        "Cost Analysis Agent": 100,
        "Boiler Efficiency Agent": 100,
        "Performance Comparison Agent": 100,
        "Knowledge Graph Agent": 100
    }
    
    def status_callback(agent_name: str, status: str):
        """Callback to update workflow status"""
        workflow_status[workflow_id]["current_agent"] = agent_name
        workflow_status[workflow_id]["agent_status"] = status
        
        # Update progress based on agent
        if agent_name in agent_progress_map:
            workflow_status[workflow_id]["progress"] = agent_progress_map[agent_name]
    
    try:
        workflow_status[workflow_id]["status"] = "running"
        workflow_status[workflow_id]["current_agent"] = "Initializing"
        workflow_status[workflow_id]["progress"] = 0
        
        # Run LLM-powered PARALLEL workflow (default)
        print(f"🚀 Running LLM-Powered PARALLEL Workflow (Default)")
        final_state = await asyncio.to_thread(
            run_llm_workflow_parallel, 
            initial_state,
            status_callback
        )
        
        # Update status to completed
        workflow_status[workflow_id]["status"] = "completed"
        workflow_status[workflow_id]["progress"] = 100
        workflow_status[workflow_id]["current_agent"] = "Completed"
        workflow_status[workflow_id]["results"] = final_state
        workflow_status[workflow_id]["completed_at"] = datetime.now().isoformat()
        
        # Save to DynamoDB for persistent context
        try:
            from dynamodb_service import DynamoDBService
            db = DynamoDBService()
            db.initialize_table()
            
            optimization_data = {
                'scenario_id': 'default',
                'status': 'completed',
                'coal_sources': initial_state.get('coal_sources', []),
                'target_specs': initial_state.get('target_specifications', {}),
                'operational_constraints': initial_state.get('operational_constraints', {}),
                'optimization_results': final_state.get('optimized_blend_strategy', {}),
                'quality_predictions': final_state.get('quality_predictions', {}),
                'cost_analysis': final_state.get('cost_analysis', {}),
                'boiler_efficiency': final_state.get('boiler_efficiency_analysis', {}),
                'performance_comparison': final_state.get('performance_comparison', {}),
                'knowledge_graph': final_state.get('knowledge_graph', {}),
                'workflow_metadata': {
                    'workflow_id': workflow_id,
                    'completed_at': datetime.now().isoformat()
                },
                'agent_messages': final_state.get('agent_messages', [])
            }
            
            db.save_optimization(workflow_id, optimization_data)
            print(f"✅ Optimization {workflow_id} saved to DynamoDB")
        except Exception as db_error:
            print(f"⚠️ Failed to save to DynamoDB: {db_error}")
            # Don't fail the workflow if DB save fails
        
    except Exception as e:
        workflow_status[workflow_id]["status"] = "failed"
        workflow_status[workflow_id]["error"] = str(e)
        import traceback
        workflow_status[workflow_id]["traceback"] = traceback.format_exc()

@app.post("/api/optimize")
async def optimize_blend(request: OptimizationRequest):
    """
    Run the complete agentic optimization workflow with Strands and Bedrock
    Returns immediately with workflow_id for status polling
    """
    try:
        # Generate workflow ID
        workflow_id = str(uuid.uuid4())
        
        # Convert request to workflow format
        coal_data = [coal.model_dump() for coal in request.coal_sources]
        target_data = request.target_specs.model_dump()
        
        # Prepare state for workflow (simple workflow format)
        initial_state = {
            "coal_quality_params": {
                coal['name']: {
                    'gcv': coal['gcv'],
                    'ash': coal['ash'],
                    'sulfur': coal['sulfur'],
                    'moisture': coal['moisture']
                }
                for coal in coal_data
            },
            "cost_params": {
                coal['name']: coal['cost']
                for coal in coal_data
            },
            "availability_constraints": {
                coal['name']: coal['available']
                for coal in coal_data
            },
            "operational_constraints": {
                "total_required": request.total_required,
                "min_blend_percentage": 5.0,
                "max_blend_percentage": 60.0,
                "target_boiler_efficiency": request.target_boiler_efficiency or 85.0
            },
            "target_specifications": {
                "gcv_min": target_data['gcv_min'],
                "ash_max": target_data['ash_max'],
                "sulfur_max": target_data['sulfur_max'],
                "moisture_max": target_data['moisture_max']
            },
            "coal_sources": coal_data,
            "agent_messages": []
        }
        
        # Initialize workflow status
        workflow_status[workflow_id] = {
            "workflow_id": workflow_id,
            "status": "initializing",
            "progress": 0,
            "current_agent": None,
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "results": None,
            "error": None
        }
        
        # Start workflow in background
        print(f"🚀 Starting workflow {workflow_id} with {len(coal_data)} coals...")
        asyncio.create_task(run_workflow_with_status(workflow_id, initial_state))
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "message": "Workflow started. Use /api/workflow-status/{workflow_id} to check progress.",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        import traceback
        error_detail = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/api/workflow-status/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """
    Get the current status of a workflow
    """
    if workflow_id not in workflow_status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    status = workflow_status[workflow_id]
    
    # If completed, format and return full results
    if status["status"] == "completed" and status["results"]:
        final_state = status["results"]
        boiler_data = final_state.get("boiler_efficiency_analysis")
        
        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "progress": 100,
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "validation": final_state.get("validation_result"),
            "optimization": final_state.get("optimized_blend_strategy"),
            "cost_analysis": final_state.get("cost_analysis"),
            "quality_prediction": final_state.get("quality_predictions"),
            "boiler_efficiency_analysis": boiler_data,
            "report": final_state.get("comprehensive_report"),
            "performance_comparison": final_state.get("performance_comparison"),
            "knowledge_graph": final_state.get("knowledge_graph"),
            "agent_messages": final_state.get("agent_messages", []),
            "executive_report": final_state.get("executive_report"),
            "detailed_report": final_state.get("detailed_report"),
            "report_metadata": final_state.get("report_metadata"),
            "orchestration_metadata": final_state.get("orchestration_metadata"),
            "completed_at": status["completed_at"]
        }
    
    # Return current status
    return {
        "workflow_id": workflow_id,
        "status": status["status"],
        "progress": status["progress"],
        "current_agent": status["current_agent"],
        "started_at": status["started_at"],
        "error": status.get("error"),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/validate")
async def validate_inputs(request: OptimizationRequest):
    """
    Validate coal sources and target specifications
    """
    try:
        coal_data = [coal.model_dump() for coal in request.coal_sources]
        target_data = request.target_specs.model_dump()
        
        validation_result = {
            "valid": True,
            "coal_count": len(coal_data),
            "total_available": sum(coal['available'] for coal in coal_data),
            "required": request.total_required,
            "feasible": sum(coal['available'] for coal in coal_data) >= request.total_required,
            "warnings": []
        }
        
        if not validation_result["feasible"]:
            validation_result["warnings"].append(
                f"Total available ({validation_result['total_available']}) < Required ({request.total_required})"
            )
        
        return {
            "success": True,
            "validation": validation_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_interaction(message: ChatMessage):
    """
    Handle natural language chat interactions with enhanced agentic backend
    Supports tool-calling for analysis, reports, emails, and knowledge queries
    Enhanced with DynamoDB context retrieval
    """
    try:
        # Try enhanced chat with tools first
        try:
            from agentic_chat_with_tools_enhanced import chat_with_tools
            
            # Get optimization results from context if available
            optimization_results = message.context.get('optimization_results') if message.context else None
            
            # Debug logging
            print(f"💬 Chat received context: has_context={message.context is not None}")
            if message.context:
                print(f"   Context keys: {list(message.context.keys())}")
                print(f"   Has optimization_results: {optimization_results is not None}")
                if optimization_results:
                    print(f"   Optimization keys: {list(optimization_results.keys())}")
            
            # If no optimization results in context, try to get latest from DynamoDB
            if not optimization_results:
                try:
                    from dynamodb_service import DynamoDBService
                    db = DynamoDBService()
                    db.initialize_table()
                    
                    latest_opt = db.get_latest_optimization()
                    if latest_opt:
                        # Reconstruct optimization results format
                        optimization_results = {
                            'optimized_blend_strategy': latest_opt.get('optimization_results', {}),
                            'quality_predictions': latest_opt.get('quality_predictions', {}),
                            'cost_analysis': latest_opt.get('cost_analysis', {}),
                            'boiler_efficiency_analysis': latest_opt.get('boiler_efficiency', {}),
                            'performance_comparison': latest_opt.get('performance_comparison', {}),
                            'knowledge_graph': latest_opt.get('knowledge_graph', {}),
                            'agent_messages': latest_opt.get('agent_messages', []),
                            'workflow_id': latest_opt.get('id'),
                            'created_at': latest_opt.get('created_at')
                        }
                        print(f"✅ Retrieved optimization context from DynamoDB: {latest_opt.get('id')}")
                except Exception as db_error:
                    print(f"⚠️ Could not retrieve from DynamoDB: {db_error}")
                    # Continue without DB context
            
            response = await asyncio.to_thread(
                chat_with_tools,
                message.message,
                optimization_results
            )
            
            # Add success flag and timestamp
            response['success'] = True
            response['timestamp'] = datetime.now().isoformat()
            response['context_source'] = 'database' if optimization_results and not message.context.get('optimization_results') else 'session'
            
            return response
            
        except ImportError:
            # Fallback to original chat agent
            from chat_agent import process_chat_message
            
            response = await asyncio.to_thread(
                process_chat_message,
                message.message,
                message.context
            )
            
            return response
        
    except Exception as e:
        import traceback
        return {
            "success": False,
            "response": f"I apologize, but I encountered an error. Please try again. Error: {str(e)}",
            "tools_used": [],
            "actions_taken": [],
            "suggestions": [],
            "error": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/optimization-history")
async def get_optimization_history(scenario_id: str = 'default', limit: int = 10):
    """
    Get optimization history from DynamoDB
    """
    try:
        from dynamodb_service import DynamoDBService
        db = DynamoDBService()
        db.initialize_table()
        
        history = db.get_optimization_history(scenario_id, limit)
        
        return {
            "success": True,
            "count": len(history),
            "history": history,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.get("/api/optimization/{workflow_id}")
async def get_optimization_by_id(workflow_id: str):
    """
    Get specific optimization by workflow ID from DynamoDB
    """
    try:
        from dynamodb_service import DynamoDBService
        db = DynamoDBService()
        db.initialize_table()
        
        optimization = db.get_optimization(workflow_id)
        
        if not optimization:
            raise HTTPException(status_code=404, detail="Optimization not found")
        
        return {
            "success": True,
            "optimization": optimization,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.get("/api/sample-data")
async def get_sample_data():
    """
    Return sample coal data for testing
    """
    return {
        "coal_sources": [
            {
                "name": "Indonesian Sub-Bituminous A",
                "gcv": 5850,
                "ash": 8.2,
                "sulfur": 0.38,
                "moisture": 6.8,
                "cost": 82.0,
                "available": 50000
            },
            {
                "name": "Australian Premium Thermal",
                "gcv": 6550,
                "ash": 9.5,
                "sulfur": 0.58,
                "moisture": 5.2,
                "cost": 118.0,
                "available": 35000
            },
            {
                "name": "South African Grade A",
                "gcv": 6180,
                "ash": 11.8,
                "sulfur": 0.75,
                "moisture": 7.2,
                "cost": 93.0,
                "available": 42000
            },
            {
                "name": "Colombian Export Quality",
                "gcv": 6320,
                "ash": 8.8,
                "sulfur": 0.68,
                "moisture": 4.8,
                "cost": 108.0,
                "available": 38000
            }
        ],
        "target_specs": {
            "gcv_min": 5800,
            "ash_max": 15.0,
            "sulfur_max": 1.0,
            "moisture_max": 7.5
        },
        "total_required": 10000
    }

@app.get("/api/test-scenarios")
async def get_test_scenarios():
    """
    Return all available test scenarios with 5 coal types each
    """
    from realistic_sample_data import get_all_test_scenarios
    return get_all_test_scenarios()

@app.get("/api/test-scenario/{scenario_id}")
async def get_test_scenario(scenario_id: str):
    """
    Return specific test scenario data (5 coal types each)
    """
    from realistic_sample_data import get_test_scenario
    
    scenario_data = get_test_scenario(scenario_id)
    if not scenario_data:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found")
    
    return scenario_data

@app.post("/api/chat/enhanced")
async def enhanced_chat(request: dict):
    """
    Enhanced multi-agentic chat endpoint
    """
    from enhanced_chat_agent import process_enhanced_chat
    
    message = request.get("message", "")
    context = request.get("context")
    
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    try:
        response = process_enhanced_chat(message, context)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# REPORT GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/generate-reports")
async def generate_reports(optimization_results: Dict, use_ai: bool = False):
    """
    Generate both executive and detailed reports from optimization results
    
    Request body should contain the complete optimization results
    Query param use_ai=true to enable AI generation (may be slow/throttled)
    """
    try:
        from report_generation_agent import generate_both_reports
        
        # Generate reports (use template mode by default to avoid throttling)
        reports = await asyncio.to_thread(generate_both_reports, optimization_results, use_ai)
        
        return {
            "success": True,
            "reports": reports,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.post("/api/generate-executive-report")
async def generate_executive_report_endpoint(optimization_results: Dict):
    """
    Generate executive summary report only
    """
    try:
        from report_generation_agent import generate_executive_report
        
        report = await asyncio.to_thread(generate_executive_report, optimization_results)
        
        return {
            "success": True,
            "report": report,
            "report_type": "executive",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.post("/api/generate-detailed-report")
async def generate_detailed_report_endpoint(optimization_results: Dict):
    """
    Generate detailed technical report only
    """
    try:
        from report_generation_agent import generate_detailed_report
        
        report = await asyncio.to_thread(generate_detailed_report, optimization_results)
        
        return {
            "success": True,
            "report": report,
            "report_type": "detailed",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.post("/api/save-reports")
async def save_reports_endpoint(request: Dict):
    """
    Generate and save reports to files
    
    Request body:
    {
        "optimization_results": {...},
        "filename_prefix": "optional_prefix"
    }
    """
    try:
        from report_generation_agent import generate_both_reports, save_reports_to_file
        
        optimization_results = request.get("optimization_results")
        filename_prefix = request.get("filename_prefix", "coal_blend_report")
        
        # Generate reports
        reports = await asyncio.to_thread(generate_both_reports, optimization_results)
        
        # Save to files
        file_info = await asyncio.to_thread(save_reports_to_file, reports, filename_prefix)
        
        return {
            "success": True,
            "files": file_info,
            "message": "Reports generated and saved successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

# ============================================================================
# EMAIL NOTIFICATION ENDPOINTS
# ============================================================================

@app.post("/api/send-email-notification")
async def send_email_notification_endpoint(optimization_results: Dict):
    """
    Send email notification with optimization summary
    Uses Claude Haiku 3.5 and Amazon SES
    
    Request body should contain the complete optimization results
    """
    try:
        from email_notification_agent import send_optimization_email
        
        result = await asyncio.to_thread(send_optimization_email, optimization_results)
        
        return result
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.get("/api/test-email")
async def test_email_endpoint():
    """
    Test email configuration and SES connectivity
    """
    try:
        from email_notification_agent import test_email_connection
        
        result = await asyncio.to_thread(test_email_connection)
        
        return result
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.post("/api/optimize-traditional")
async def optimize_blend_traditional(request: OptimizationRequest):
    """
    Run Traditional computational optimization workflow (fallback)
    Uses scipy/numpy for fast computational optimization
    Returns same data structure as LLM workflow for UI compatibility
    """
    try:
        # Generate workflow ID
        workflow_id = str(uuid.uuid4())
        
        # Convert request to workflow format
        coal_data = [coal.model_dump() for coal in request.coal_sources]
        target_data = request.target_specs.model_dump()
        
        # Prepare state for LLM workflow (same format as existing workflow)
        initial_state = {
            "coal_quality_params": {
                coal['name']: {
                    'gcv': coal['gcv'],
                    'ash': coal['ash'],
                    'sulfur': coal['sulfur'],
                    'moisture': coal['moisture']
                }
                for coal in coal_data
            },
            "cost_params": {
                coal['name']: coal['cost']
                for coal in coal_data
            },
            "availability_constraints": {
                coal['name']: coal['available']
                for coal in coal_data
            },
            "operational_constraints": {
                "total_required": request.total_required,
                "min_blend_percentage": 5.0,
                "max_blend_percentage": 60.0,
                "target_boiler_efficiency": request.target_boiler_efficiency or 85.0
            },
            "target_specifications": {
                "gcv_min": target_data['gcv_min'],
                "ash_max": target_data['ash_max'],
                "sulfur_max": target_data['sulfur_max'],
                "moisture_max": target_data['moisture_max']
            },
            "coal_sources": coal_data,
            "agent_messages": []
        }
        
        # Run traditional computational workflow (fallback)
        print(f"🔢 Starting Traditional workflow with {len(coal_data)} coals...")
        from agentic_workflow_parallel import MasterOrchestrator
        orchestrator = MasterOrchestrator(workflow_id=workflow_id, status_callback=lambda x, y: None)
        final_state = await asyncio.to_thread(
            lambda: asyncio.run(orchestrator.orchestrate_workflow(initial_state))
        )
        
        # Format response - SAME STRUCTURE as regular workflow for UI compatibility
        boiler_data = final_state.get("boiler_efficiency_analysis")
        
        return {
            "success": True,
            "workflow_type": "Traditional Computational",
            "timestamp": datetime.now().isoformat(),
            # Core results
            "validation": final_state.get("validation_result"),
            "optimization": final_state.get("optimized_blend_strategy"),
            "cost_analysis": final_state.get("cost_analysis"),
            "quality_prediction": final_state.get("quality_predictions"),
            # Specialized agents
            "boiler_efficiency_analysis": boiler_data,
            "performance_comparison": final_state.get("performance_comparison"),
            "knowledge_graph": final_state.get("knowledge_graph"),
            "report": final_state.get("comprehensive_report"),
            "executive_report": final_state.get("executive_report"),
            "detailed_report": final_state.get("detailed_report"),
            "report_metadata": final_state.get("report_metadata"),
            # Metadata
            "agent_messages": final_state.get("agent_messages", []),
            "orchestration_metadata": final_state.get("orchestration_metadata")
        }
        
    except Exception as e:
        import traceback
        error_detail = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        raise HTTPException(status_code=500, detail=error_detail)


@app.get("/api/llm-scenarios")
async def get_llm_scenarios():
    """
    Get list of LLM test scenarios with 5 coal types
    """
    try:
        from llm_test_scenarios import list_scenarios
        scenarios = list_scenarios()
        return {
            "success": True,
            "scenarios": scenarios,
            "count": len(scenarios)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/llm-scenario/{scenario_id}")
async def get_llm_scenario(scenario_id: str):
    """
    Get a specific LLM test scenario
    """
    try:
        from llm_test_scenarios import get_scenario
        scenario = get_scenario(scenario_id)
        
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        return {
            "success": True,
            "scenario": scenario
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ON-DEMAND REPORT AND EMAIL ENDPOINTS (Workflow-based)
# ============================================================================

@app.post("/api/workflow/{workflow_id}/generate-report")
async def generate_report_for_workflow(workflow_id: str):
    """
    Generate report for a completed workflow (on-demand)
    """
    if workflow_id not in workflow_status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    status = workflow_status[workflow_id]
    
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="Workflow not completed yet")
    
    try:
        # First, generate comprehensive report using LLM agent if not already done
        from agentic_workflow_llm_first import generate_comprehensive_report_llm
        from report_generation_agent import generate_both_reports
        
        # Run comprehensive report agent if not already in results
        if "comprehensive_report" not in status["results"] or not status["results"]["comprehensive_report"]:
            print("🤖 Running Comprehensive Report Agent on-demand...")
            updated_state = await asyncio.to_thread(
                generate_comprehensive_report_llm,
                status["results"]
            )
            status["results"].update(updated_state)
            workflow_status[workflow_id]["results"] = status["results"]
        
        # Generate PDF reports from workflow results
        reports = await asyncio.to_thread(generate_both_reports, status["results"])
        
        # Update workflow status with reports
        workflow_status[workflow_id]["reports"] = reports
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "reports": reports,
            "comprehensive_report": status["results"].get("comprehensive_report"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


@app.post("/api/workflow/{workflow_id}/send-email")
async def send_email_for_workflow(workflow_id: str, request: Optional[Dict] = None):
    """
    Send email notification for a completed workflow (on-demand)
    
    Optional request body:
    {
        "recipient_email": "user@example.com",
        "include_report": true
    }
    """
    if workflow_id not in workflow_status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    status = workflow_status[workflow_id]
    
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="Workflow not completed yet")
    
    try:
        from email_notification_agent import send_optimization_email
        
        # Prepare email data
        email_data = status["results"].copy()
        
        # Add optional parameters from request
        if request:
            if "recipient_email" in request:
                email_data["recipient_email"] = request["recipient_email"]
            if "include_report" in request:
                email_data["include_report"] = request["include_report"]
        
        # Send email
        result = await asyncio.to_thread(send_optimization_email, email_data)
        
        # Update workflow status with email result
        workflow_status[workflow_id]["email_sent"] = result
        
        return {
            "success": result.get("success", False),
            "workflow_id": workflow_id,
            "message": result.get("message", "Email sent"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "workflow_id": workflow_id,
            "error": str(e),
            "message": "Email service not configured or failed",
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
