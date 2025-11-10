"""
Parallel Agentic Workflow with Master Orchestrator
Optimizes execution by running independent agents in parallel
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict
from datetime import datetime

# Import all agent functions from the simple workflow
from agentic_workflow_simple import (
    validate_input_parameters,
    generate_optimized_blend_strategy,
    perform_cost_analysis,
    generate_quality_predictions,
    analyze_boiler_efficiency,
    generate_comprehensive_report,
    generate_performance_comparison,
    generate_knowledge_graph,
    generate_final_reports
)


class MasterOrchestrator:
    """
    Master Orchestrator Agent
    Manages workflow execution, coordinates agents, and optimizes parallel execution
    """
    
    def __init__(self, workflow_id=None, status_callback=None):
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.workflow_start_time = None
        self.agent_timings = {}
        self.workflow_id = workflow_id
        self.status_callback = status_callback
    
    def log_agent_start(self, agent_name: str):
        """Log when an agent starts"""
        self.agent_timings[agent_name] = {
            'start': datetime.now(),
            'status': 'running'
        }
        print(f"🎯 Master Orchestrator: Starting {agent_name}")
        
        # Update status via callback if provided
        if self.status_callback:
            self.status_callback(agent_name, 'running')
    
    def log_agent_complete(self, agent_name: str):
        """Log when an agent completes"""
        if agent_name in self.agent_timings:
            self.agent_timings[agent_name]['end'] = datetime.now()
            self.agent_timings[agent_name]['status'] = 'completed'
            duration = (self.agent_timings[agent_name]['end'] - 
                       self.agent_timings[agent_name]['start']).total_seconds()
            self.agent_timings[agent_name]['duration'] = duration
            print(f"✅ Master Orchestrator: {agent_name} completed in {duration:.2f}s")
            
            # Update status via callback if provided
            if self.status_callback:
                self.status_callback(agent_name, 'completed')
    
    def log_agent_error(self, agent_name: str, error: str):
        """Log when an agent errors"""
        if agent_name in self.agent_timings:
            self.agent_timings[agent_name]['end'] = datetime.now()
            self.agent_timings[agent_name]['status'] = 'error'
            self.agent_timings[agent_name]['error'] = str(error)
            print(f"❌ Master Orchestrator: {agent_name} failed - {error}")
    
    async def run_agent_async(self, agent_func, state: Dict, agent_name: str) -> Dict:
        """Run an agent asynchronously"""
        self.log_agent_start(agent_name)
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(self.executor, agent_func, state)
            self.log_agent_complete(agent_name)
            return result
        except Exception as e:
            self.log_agent_error(agent_name, str(e))
            return state
    
    async def run_parallel_agents(self, state: Dict, agents: list) -> Dict:
        """
        Run multiple agents in parallel
        Each agent gets a copy of the state and returns updated state
        Results are merged back into the main state
        """
        print(f"🚀 Master Orchestrator: Running {len(agents)} agents in parallel...")
        
        # Create tasks for all agents
        tasks = []
        for agent_func, agent_name in agents:
            task = self.run_agent_async(agent_func, state.copy(), agent_name)
            tasks.append((task, agent_name))
        
        # Wait for all agents to complete
        results = await asyncio.gather(*[task for task, _ in tasks], return_exceptions=True)
        
        # Merge results back into state
        for (_, agent_name), result in zip(tasks, results):
            if isinstance(result, Exception):
                print(f"❌ Master Orchestrator: {agent_name} raised exception: {result}")
            elif isinstance(result, dict):
                # Merge the agent's results into main state
                state.update(result)
        
        return state
    
    async def orchestrate_workflow(self, initial_state: Dict) -> Dict:
        """
        Orchestrate the complete workflow with parallel execution
        
        Workflow Stages:
        1. Sequential: Validation → Optimization (dependencies)
        2. Parallel: Cost Analysis, Quality Prediction, Boiler Efficiency, 
                    Performance Comparison, Knowledge Graph (independent)
        3. Sequential: Comprehensive Report (needs all data)
        4. Sequential: Final Reports (needs comprehensive report)
        """
        self.workflow_start_time = datetime.now()
        print("="*80)
        print("🎭 MASTER ORCHESTRATOR: Starting Parallel Agentic Workflow")
        print("="*80)
        
        state = initial_state.copy()
        
        # STAGE 1: Sequential - Validation and Optimization (have dependencies)
        print("\n📋 STAGE 1: Sequential Execution (Validation → Optimization)")
        print("-"*80)
        
        state = await self.run_agent_async(
            validate_input_parameters, 
            state, 
            "Validation Agent"
        )
        
        state = await self.run_agent_async(
            generate_optimized_blend_strategy, 
            state, 
            "Optimization Agent"
        )
        
        # STAGE 2: Parallel - Analysis Agents (all independent after optimization)
        print("\n⚡ STAGE 2: Parallel Execution (5 Analysis Agents)")
        print("-"*80)
        
        parallel_agents = [
            (perform_cost_analysis, "Cost Analysis Agent"),
            (generate_quality_predictions, "Quality Prediction Agent"),
            (analyze_boiler_efficiency, "Boiler Efficiency Agent"),
            (generate_performance_comparison, "Performance Comparison Agent"),
            (generate_knowledge_graph, "Knowledge Graph Agent")
        ]
        
        state = await self.run_parallel_agents(state, parallel_agents)
        
        # STAGE 3: Sequential - Comprehensive Report (needs all analysis data)
        print("\n📊 STAGE 3: Sequential Execution (Comprehensive Report)")
        print("-"*80)
        
        state = await self.run_agent_async(
            generate_comprehensive_report, 
            state, 
            "Comprehensive Report Agent"
        )
        
        # STAGE 4: Sequential - Final Reports (needs comprehensive report)
        print("\n📄 STAGE 4: Sequential Execution (Final Reports)")
        print("-"*80)
        
        state = await self.run_agent_async(
            generate_final_reports, 
            state, 
            "Report Generation Agent"
        )
        
        # STAGE 5: Email Notification (optional, non-blocking)
        print("\n📧 STAGE 5: Email Notification")
        print("-"*80)
        
        try:
            from email_notification_agent import send_optimization_email
            email_result = send_optimization_email(state)
            state["email_notification"] = email_result
            if email_result.get('success'):
                print(f"✅ Email sent successfully: {email_result.get('message')}")
            else:
                print(f"⚠️ Email notification failed: {email_result.get('error')}")
        except Exception as e:
            print(f"⚠️ Email notification skipped: {str(e)}")
            state["email_notification"] = {
                'success': False,
                'error': str(e),
                'skipped': True
            }
        
        # Calculate total workflow time
        workflow_end_time = datetime.now()
        total_duration = (workflow_end_time - self.workflow_start_time).total_seconds()
        
        # Add orchestration metadata to state
        state["orchestration_metadata"] = {
            "workflow_start": self.workflow_start_time.isoformat(),
            "workflow_end": workflow_end_time.isoformat(),
            "total_duration_seconds": total_duration,
            "agent_timings": self.agent_timings,
            "execution_mode": "parallel",
            "stages": {
                "stage_1": "Sequential (Validation, Optimization)",
                "stage_2": "Parallel (5 Analysis Agents)",
                "stage_3": "Sequential (Comprehensive Report)",
                "stage_4": "Sequential (Final Reports)"
            }
        }
        
        print("\n" + "="*80)
        print(f"✅ MASTER ORCHESTRATOR: Workflow completed in {total_duration:.2f}s")
        print("="*80)
        
        # Print timing summary
        print("\n⏱️  Agent Execution Times:")
        for agent_name, timing in self.agent_timings.items():
            if 'duration' in timing:
                print(f"   • {agent_name}: {timing['duration']:.2f}s")
        
        return state


# Main entry point for parallel workflow
async def run_workflow_parallel_async(initial_state: Dict) -> Dict:
    """
    Run the workflow with parallel execution using Master Orchestrator
    This is the async version
    """
    orchestrator = MasterOrchestrator()
    return await orchestrator.orchestrate_workflow(initial_state)


def run_workflow_parallel(initial_state: Dict) -> Dict:
    """
    Run the workflow with parallel execution using Master Orchestrator
    This is the synchronous wrapper for compatibility
    """
    return asyncio.run(run_workflow_parallel_async(initial_state))


# Backward compatibility - can be used as drop-in replacement
def run_workflow(initial_state: Dict) -> Dict:
    """
    Run workflow with parallel execution (backward compatible interface)
    """
    return run_workflow_parallel(initial_state)


if __name__ == "__main__":
    # Test the parallel workflow
    print("Testing Parallel Agentic Workflow...")
    
    test_state = {
        "coal_quality_params": {
            "Coal A": {"gcv": 6000, "ash": 10, "sulfur": 0.5, "moisture": 8},
            "Coal B": {"gcv": 5500, "ash": 12, "sulfur": 0.6, "moisture": 10}
        },
        "cost_params": {"Coal A": 100, "Coal B": 80},
        "availability_constraints": {"Coal A": 10000, "Coal B": 15000},
        "target_specifications": {
            "gcv_min": 5800,
            "ash_max": 12,
            "sulfur_max": 0.6,
            "moisture_max": 10
        },
        "operational_constraints": {
            "total_required": 5000,
            "target_boiler_efficiency": 85.0
        },
        "agent_messages": []
    }
    
    result = run_workflow_parallel(test_state)
    print("\n✅ Test completed!")
    print(f"Total workflow time: {result['orchestration_metadata']['total_duration_seconds']:.2f}s")
