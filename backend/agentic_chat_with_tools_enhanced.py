"""
Enhanced Agentic Chat with Tool-Calling Capabilities
Comprehensive AI assistant for coal blending optimization
"""

from typing import Dict, List, Optional, Any
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from datetime import datetime
import json
import re
from botocore.config import Config


class AgenticChatWithTools:
    """
    Advanced chat agent with tool-calling capabilities for:
    - Analyzing agent outputs
    - Downloading reports
    - Sending emails
    - Answering coal blending questions
    - Providing recommendations
    """
    
    def __init__(self):
        self.llm = self._create_llm()
        self.conversation_history = []
        self.optimization_results = None
        self.coal_blending_knowledge = self._load_knowledge_base()
    
    def _create_llm(self):
        """Create Bedrock LLM with tool-calling support"""
        config = Config(
            read_timeout=60,  # Reduced from 300 to 60 seconds
            connect_timeout=10,  # Reduced from 60 to 10 seconds
            retries={'max_attempts': 2}  # Reduced from 3 to 2
        )
        
        return ChatBedrock(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "temperature": 0.7,
                "max_tokens": 4000  # Balanced for comprehensive but fast responses
            },
            config=config
        )
    
    def _load_knowledge_base(self) -> Dict:
        """Load coal blending knowledge base"""
        return {
            "gcv_ranges": {
                "excellent": (6500, 7500),
                "good": (5500, 6500),
                "acceptable": (4500, 5500),
                "poor": (3500, 4500)
            },
            "ash_limits": {
                "low": (0, 10),
                "medium": (10, 20),
                "high": (20, 30),
                "very_high": (30, 100)
            },
            "sulfur_limits": {
                "low_sulfur": (0, 0.5),
                "medium_sulfur": (0.5, 1.0),
                "high_sulfur": (1.0, 2.0),
                "very_high_sulfur": (2.0, 100)
            },
            "best_practices": [
                "Blend coals with complementary properties",
                "Balance cost with quality requirements",
                "Consider boiler design and capacity",
                "Monitor ash fusion temperature",
                "Maintain consistent blend ratios",
                "Test blends before full-scale use"
            ],
            "boiler_efficiency_factors": [
                "Higher GCV improves combustion efficiency",
                "Lower ash reduces heat transfer losses",
                "Lower moisture reduces evaporation losses",
                "Proper air-fuel ratio is critical",
                "Regular maintenance prevents efficiency loss"
            ]
        }
    
    def _get_historical_data(self, limit: int = 5) -> List[Dict]:
        """Fetch historical optimization data from DynamoDB"""
        try:
            from dynamodb_service import DynamoDBService
            db = DynamoDBService()
            db.initialize_table()
            
            history = db.get_optimization_history(limit=limit)
            print(f"📊 Retrieved {len(history)} historical optimizations")
            return history
        except Exception as e:
            print(f"⚠️ Could not retrieve history: {e}")
            return []
    
    def chat(self, user_message: str, optimization_results: Optional[Dict] = None) -> Dict:
        """
        Process user message with tool-calling capabilities
        
        Returns:
            {
                'response': str,
                'tools_used': List[str],
                'actions_taken': List[Dict],
                'suggestions': List[str]
            }
        """
        # Update optimization results if provided
        if optimization_results:
            self.optimization_results = optimization_results
        
        # Detect intent and required tools
        intent = self._detect_intent(user_message)
        
        # Fetch historical data if needed
        historical_data = None
        if intent == 'historical_analysis':
            historical_data = self._get_historical_data(limit=5)
        
        # Build system prompt with tool descriptions
        system_prompt = self._build_system_prompt_with_tools()
        
        # Build context-aware prompt
        context_prompt = self._build_context_prompt(user_message, intent, historical_data)
        
        # Create messages
        messages = [
            SystemMessage(content=system_prompt),
            *self.conversation_history[-6:],  # Last 6 messages
            HumanMessage(content=context_prompt)
        ]
        
        # Get AI response with timeout
        try:
            print(f"🤖 Calling LLM for: {user_message[:50]}...")
            response = self.llm.invoke(messages)
            ai_response = response.content
            print(f"✅ LLM responded ({len(ai_response)} chars)")
            
            # Validate response for hallucinations
            ai_response = self._validate_response(ai_response)
            
            # Parse for tool calls
            tool_calls = self._extract_tool_calls(ai_response)
            
            # Execute tools
            tool_results = self._execute_tools(tool_calls)
            
            # Generate final response with tool results
            final_response = self._generate_final_response(
                ai_response, tool_results, intent
            )
            
            # Update conversation history
            self.conversation_history.append(HumanMessage(content=user_message))
            self.conversation_history.append(AIMessage(content=final_response['response']))
            
            return final_response
            
        except Exception as e:
            return {
                'response': f"I encountered an error: {str(e)}. Please try rephrasing your question.",
                'tools_used': [],
                'actions_taken': [],
                'suggestions': [],
                'error': str(e)
            }
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower()
        
        # Historical analysis intents
        if any(word in message_lower for word in ['history', 'previous', 'past', 'last', 'compare', 'trend']):
            return 'historical_analysis'
        
        # Analysis intents
        if any(word in message_lower for word in ['why', 'explain', 'how', 'analyze', 'impact']):
            return 'analysis'
        
        # Task intents
        if any(word in message_lower for word in ['download', 'report', 'pdf']):
            return 'download_report'
        if any(word in message_lower for word in ['send', 'email', 'mail']):
            return 'send_email'
        if any(word in message_lower for word in ['add coal', 'new coal', 'add source']):
            return 'add_coal'
        if any(word in message_lower for word in ['set target', 'change target', 'update target']):
            return 'set_target'
        
        # Knowledge intents
        if any(word in message_lower for word in ['what is', 'define', 'explain', 'tell me about']):
            return 'knowledge'
        
        # Recommendation intents
        if any(word in message_lower for word in ['recommend', 'suggest', 'improve', 'optimize']):
            return 'recommendation'
        
        return 'general'
    
    def _validate_response(self, response: str) -> str:
        """Validate response to catch potential hallucinations"""
        # Check for common hallucination patterns
        warning_phrases = [
            "I don't have",
            "not available",
            "no data",
            "cannot determine",
            "insufficient information"
        ]
        
        # If response contains uncertainty phrases, it's likely accurate
        has_uncertainty = any(phrase.lower() in response.lower() for phrase in warning_phrases)
        
        # Check if response has actual data when optimization results exist
        if self.optimization_results and not has_uncertainty:
            # Verify response contains some actual numbers
            import re
            numbers = re.findall(r'\d+[,\d]*\.?\d*', response)
            if len(numbers) < 2:
                # Response should have at least a few numbers if data is available
                print("⚠️ Warning: Response may lack specific data")
        
        return response
    
    def _build_system_prompt_with_tools(self) -> str:
        """Build comprehensive system prompt with tool descriptions"""
        return f"""You are an expert AI assistant for coal blending optimization.

CONTEXT: {'Optimization data available' if self.optimization_results else 'No optimization data'}

CRITICAL RULES - NO HALLUCINATION:
1. ONLY use data explicitly provided in the context
2. If data is not available, say "Data not available" - DO NOT make up numbers
3. NEVER invent coal names, costs, or parameters
4. NEVER assume or estimate values not in the data
5. If asked about something not in the data, clearly state you don't have that information
6. Always cite specific numbers from the provided data
7. If historical data is empty, say "No historical data available"

YOUR ROLE:
- Analyze coal blend optimization results using ONLY provided data
- Explain decisions based on actual numbers
- Provide recommendations grounded in real data
- Answer questions ONLY with information you have

RESPONSE FORMAT:
- Use ## for section headers
- Use • for bullet points
- Use **bold** for numbers (ONLY real numbers from data)
- Be comprehensive but ONLY with available data
- Add blank lines between sections

COAL QUALITY KNOWLEDGE (General reference only):
- GCV: Excellent (6500+), Good (5500-6500), Acceptable (4500-5500) kcal/kg
- Ash: Low (<10%), Medium (10-20%), High (20-30%)
- Sulfur: Low (<0.5%), Medium (0.5-1%), High (1-2%)

REMEMBER: Accuracy over completeness. Say "I don't have that data" rather than guessing."""
    
    def _build_context_prompt(self, user_message: str, intent: str, historical_data: Optional[List[Dict]] = None) -> str:
        """Build context-aware prompt with optimization results"""
        prompt = f"User Question: {user_message}\n\n"
        
        # Add historical data if available
        if historical_data and len(historical_data) > 0:
            prompt += f"HISTORICAL DATA ({len(historical_data)} optimizations):\n"
            for i, opt_data in enumerate(historical_data[:5], 1):
                opt = opt_data.get('optimization_results', {})
                quality = opt_data.get('quality_predictions', {})
                created = opt_data.get('created_at', 'Unknown')
                
                prompt += f"\n{i}. Optimization from {created[:10]}:\n"
                prompt += f"   Cost: ${opt.get('total_cost', 0):,.0f}\n"
                prompt += f"   Quality: {quality.get('overall_quality_score', 0):.0f}%\n"
                prompt += f"   Coals: {len(opt.get('blend_composition', []))}\n"
                
                achieved = opt.get('achieved_parameters', {})
                prompt += f"   GCV: {achieved.get('gcv', 0):.0f}, Ash: {achieved.get('ash', 0):.1f}%, S: {achieved.get('sulfur', 0):.2f}%\n"
            
            prompt += "\n"
        
        # Add optimization results context if available
        if self.optimization_results:
            opt = self.optimization_results.get('optimized_blend_strategy') or self.optimization_results.get('optimization', {})
            quality = self.optimization_results.get('quality_predictions') or self.optimization_results.get('quality_prediction', {})
            cost = self.optimization_results.get('cost_analysis', {})
            
            prompt += "OPTIMIZATION DATA AVAILABLE:\n"
            prompt += f"• Total Cost: ${opt.get('total_cost', 0):,.2f}\n"
            prompt += f"• Quality Score: {quality.get('overall_quality_score', 0):.1f}%\n"
            prompt += f"• Number of Coals: {len(opt.get('blend_composition', []))}\n"
            
            # Add blend composition details
            blend = opt.get('blend_composition', [])
            if blend:
                prompt += f"\nBlend Composition:\n"
                for coal in blend[:5]:  # Top 5 coals
                    prompt += f"• {coal.get('coal_name', 'Unknown')}: {coal.get('percentage', 0):.1f}% ({coal.get('quantity', 0):,.0f} tons)\n"
            
            # Add achieved parameters
            achieved = opt.get('achieved_parameters', {})
            prompt += f"\nAchieved Parameters:\n"
            prompt += f"• GCV: {achieved.get('gcv', 0):.0f} kcal/kg\n"
            prompt += f"• Ash: {achieved.get('ash', 0):.2f}%\n"
            prompt += f"• Sulfur: {achieved.get('sulfur', 0):.3f}%\n"
            prompt += f"• Moisture: {achieved.get('moisture', 0):.2f}%\n\n"
            
            # Add cost efficiency if available
            if cost:
                efficiency = cost.get('cost_efficiency', {})
                prompt += f"Cost Efficiency: {efficiency.get('efficiency_rating', 'N/A')}\n\n"
        
        prompt += "INSTRUCTIONS:\n"
        prompt += "Provide a comprehensive, well-structured answer using:\n"
        prompt += "• ## for section headers\n"
        prompt += "• • for bullet points\n"
        prompt += "• **bold** for key metrics and numbers\n"
        prompt += "• ONLY data explicitly provided above\n"
        prompt += "• Actionable insights based on real data\n\n"
        
        prompt += "ANTI-HALLUCINATION CHECKLIST:\n"
        prompt += "✓ Every number comes from the data above\n"
        prompt += "✓ Every coal name is from the data above\n"
        prompt += "✓ If data is missing, explicitly state it\n"
        prompt += "✓ No assumptions or estimates\n"
        prompt += "✓ No invented details\n\n"
        
        return prompt
    
    def _extract_tool_calls(self, ai_response: str) -> List[Dict]:
        """Extract tool calls from AI response"""
        tool_calls = []
        
        # Look for [TOOL: tool_name] patterns
        pattern = r'\[TOOL:\s*(\w+)\]'
        matches = re.findall(pattern, ai_response)
        
        for tool_name in matches:
            tool_calls.append({
                'tool': tool_name,
                'parameters': {}
            })
        
        return tool_calls
    
    def _execute_tools(self, tool_calls: List[Dict]) -> List[Dict]:
        """Execute requested tools"""
        results = []
        
        for call in tool_calls:
            tool_name = call['tool']
            
            if tool_name == 'analyze_agent_output':
                result = self._tool_analyze_agent_output()
            elif tool_name == 'download_report':
                result = self._tool_download_report()
            elif tool_name == 'send_email':
                result = self._tool_send_email()
            elif tool_name == 'search_knowledge':
                result = self._tool_search_knowledge()
            elif tool_name == 'get_recommendations':
                result = self._tool_get_recommendations()
            else:
                result = {'success': False, 'message': f'Unknown tool: {tool_name}'}
            
            results.append({
                'tool': tool_name,
                'result': result
            })
        
        return results
    
    def _tool_analyze_agent_output(self) -> Dict:
        """Analyze agent outputs in detail"""
        if not self.optimization_results:
            return {'success': False, 'message': 'No optimization results available'}
        
        analysis = {
            'success': True,
            'insights': []
        }
        
        # Analyze blend composition - handle both key formats
        opt = self.optimization_results.get('optimized_blend_strategy') or self.optimization_results.get('optimization', {})
        blend = opt.get('blend_composition', [])
        
        if blend:
            analysis['insights'].append(f"Blend uses {len(blend)} coal sources")
            for coal in blend[:3]:  # Top 3
                analysis['insights'].append(
                    f"{coal.get('coal_name')}: {coal.get('percentage', 0):.1f}% "
                    f"({coal.get('quantity', 0):,.0f} tons)"
                )
        
        # Analyze quality - handle both key formats
        quality = self.optimization_results.get('quality_predictions') or self.optimization_results.get('quality_prediction', {})
        score = quality.get('overall_quality_score', 0)
        analysis['insights'].append(f"Quality score: {score:.1f}% - {'Excellent' if score >= 90 else 'Good' if score >= 80 else 'Acceptable'}")
        
        # Analyze cost
        cost = self.optimization_results.get('cost_analysis', {})
        total_cost = cost.get('total_cost', 0)
        analysis['insights'].append(f"Total cost: ${total_cost:,.2f}")
        
        return analysis
    
    def _tool_download_report(self) -> Dict:
        """Generate download report action"""
        return {
            'success': True,
            'action': 'download_report',
            'message': 'Report generation initiated',
            'report_types': ['executive', 'detailed', 'technical']
        }
    
    def _tool_send_email(self) -> Dict:
        """Generate send email action"""
        import os
        recipient = os.getenv("SES_TO_EMAIL", "admin@example.com")
        return {
            'success': True,
            'action': 'send_email',
            'message': 'Email sending initiated',
            'recipient': recipient
        }
    
    def _tool_search_knowledge(self) -> Dict:
        """Search coal blending knowledge base"""
        return {
            'success': True,
            'knowledge': self.coal_blending_knowledge,
            'best_practices': self.coal_blending_knowledge['best_practices']
        }
    
    def _tool_get_recommendations(self) -> Dict:
        """Generate AI-powered recommendations"""
        if not self.optimization_results:
            return {'success': False, 'message': 'No results to analyze'}
        
        recommendations = []
        
        # Analyze quality score - handle both key formats
        quality = self.optimization_results.get('quality_predictions') or self.optimization_results.get('quality_prediction', {})
        score = quality.get('overall_quality_score', 0)
        
        if score < 85:
            recommendations.append("Consider adjusting blend ratios to improve quality score")
        
        # Analyze cost
        cost = self.optimization_results.get('cost_analysis', {})
        efficiency = cost.get('cost_efficiency', {}).get('efficiency_rating', '')
        
        if efficiency in ['average', 'poor']:
            recommendations.append("Explore alternative coal sources for better cost efficiency")
        
        # Analyze boiler efficiency
        boiler = self.optimization_results.get('boiler_efficiency_analysis', {})
        eff = boiler.get('predicted_efficiency', 0)
        
        if eff < 85:
            recommendations.append("Optimize blend to improve boiler efficiency above 85%")
        
        return {
            'success': True,
            'recommendations': recommendations if recommendations else ['Current blend is well-optimized']
        }
    
    def _generate_final_response(self, ai_response: str, tool_results: List[Dict], intent: str) -> Dict:
        """Generate final response with tool results"""
        # Remove tool markers from response
        clean_response = re.sub(r'\[TOOL:\s*\w+\]', '', ai_response).strip()
        
        # Add tool results to response
        tools_used = [r['tool'] for r in tool_results]
        actions_taken = []
        suggestions = []
        
        for result in tool_results:
            if result['result'].get('success'):
                tool_name = result['tool']
                tool_data = result['result']
                
                # Add insights from analysis
                if 'insights' in tool_data:
                    clean_response += "\n\n📊 Analysis:\n" + "\n".join(f"• {i}" for i in tool_data['insights'])
                
                # Add recommendations
                if 'recommendations' in tool_data:
                    suggestions.extend(tool_data['recommendations'])
                
                # Add actions
                if 'action' in tool_data:
                    actions_taken.append(tool_data)
        
        # Add suggestions section
        if suggestions:
            clean_response += "\n\n💡 Recommendations:\n" + "\n".join(f"• {s}" for s in suggestions)
        
        return {
            'response': clean_response,
            'tools_used': tools_used,
            'actions_taken': actions_taken,
            'suggestions': suggestions
        }
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []


# Global instance
agentic_chat = AgenticChatWithTools()


def chat_with_tools(message: str, optimization_results: Optional[Dict] = None) -> Dict:
    """
    Main chat interface with tool-calling capabilities
    
    Args:
        message: User message
        optimization_results: Optional optimization results for context
    
    Returns:
        Response dictionary with answer, tools used, and actions
    """
    return agentic_chat.chat(message, optimization_results)


def reset_chat():
    """Reset chat conversation"""
    agentic_chat.reset_conversation()
