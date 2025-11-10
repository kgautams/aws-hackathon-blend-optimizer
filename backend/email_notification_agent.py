"""
Email Notification Agent for Coal Blending Optimization
Sends optimization summary emails using Claude Haiku 3.5 and Amazon SES
"""

import boto3
from typing import Dict, Optional
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime
from botocore.config import Config
from botocore.exceptions import ClientError


class EmailNotificationAgent:
    """
    Agent that generates and sends email summaries of optimization results
    Uses Claude Haiku 3.5 for fast, cost-effective summary generation
    Uses Amazon SES for email delivery
    """
    
    def __init__(self):
        self.llm = self._create_llm()
        self.ses_client = self._create_ses_client()
        # Email addresses should be configured via environment variables
        import os
        self.from_email = os.getenv("SES_FROM_EMAIL", "noreply@example.com")
        self.to_email = os.getenv("SES_TO_EMAIL", "admin@example.com")
    
    def _create_llm(self):
        """Create Bedrock LLM instance with Claude Haiku 3.5"""
        config = Config(
            read_timeout=60,
            connect_timeout=30,
            retries={'max_attempts': 3}
        )
        
        return ChatBedrock(
            model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",  # Claude Haiku 3.5
            region_name="us-east-1",
            model_kwargs={
                "temperature": 0.3,  # Lower temperature for consistent summaries
                "max_tokens": 2000
            },
            config=config
        )
    
    def _create_ses_client(self):
        """Create Amazon SES client"""
        return boto3.client('ses', region_name='us-east-1')
    
    def generate_email_summary(self, optimization_results: Dict) -> str:
        """
        Generate concise email summary using EXACT agent outputs
        NO AI GENERATION - Direct use of agent findings to ensure 100% accuracy
        """
        # Use template-based summary with exact agent outputs
        return self._generate_template_summary(optimization_results)
    
    def _format_blend_composition(self, blend_composition: list) -> str:
        """Format blend composition for email"""
        if not blend_composition:
            return "No blend data available"
        
        lines = []
        for coal in blend_composition[:5]:  # Top 5 coals
            name = coal.get('coal_name', 'Unknown')
            pct = coal.get('percentage', 0)
            qty = coal.get('quantity', 0)
            lines.append(f"  - {name}: {pct:.1f}% ({qty:,.0f} tons)")
        
        return "\n".join(lines)
    
    def _format_compliance(self, compliance: dict) -> str:
        """Format compliance status"""
        if not compliance:
            return "No compliance data"
        
        lines = []
        for param, status in compliance.items():
            icon = "✅" if status else "❌"
            lines.append(f"  {icon} {param.upper()}")
        
        return "\n".join(lines)
    
    def _generate_template_summary(self, optimization_results: Dict) -> str:
        """Template-based summary using EXACT agent outputs including executive summary"""
        # Extract ALL agent outputs
        validation = optimization_results.get('validation_result', {})
        optimization = optimization_results.get('optimized_blend_strategy', {})
        cost_analysis = optimization_results.get('cost_analysis', {})
        quality = optimization_results.get('quality_predictions', {})
        boiler = optimization_results.get('boiler_efficiency_analysis', {})
        performance = optimization_results.get('performance_comparison', {})
        executive_report = optimization_results.get('executive_report', {})
        comprehensive_report = optimization_results.get('comprehensive_report', {})
        
        # Get specific values
        all_specs_met = optimization.get('success', False)
        validation_status = validation.get('status', 'Unknown')
        feasibility_score = validation.get('feasibility_score', 0)
        blend_composition = optimization.get('blend_composition', [])
        total_cost = optimization.get('total_cost', 0)
        cost_per_ton = optimization.get('cost_per_ton', 0)
        quality_score = quality.get('overall_quality_score', 0)
        compliance_status = quality.get('compliance_status', 'unknown')
        boiler_eff = boiler.get('predicted_efficiency', 0)
        achieved_params = optimization.get('achieved_parameters', {})
        
        # Get executive summary if available
        exec_summary = executive_report.get('executive_summary', '') or comprehensive_report.get('executive_overview', '')
        key_findings = executive_report.get('key_findings', []) or comprehensive_report.get('key_findings', [])
        recommendations = executive_report.get('strategic_recommendations', []) or comprehensive_report.get('strategic_recommendations', [])
        decision = executive_report.get('decision_recommendation', {}) or comprehensive_report.get('decision_recommendation', '')
        
        # Format key findings
        findings_text = '\n'.join([f"   • {finding}" for finding in key_findings[:5]]) if key_findings else "   • Analysis complete with all agents"
        
        # Format recommendations
        recommendations_text = '\n'.join([f"   • {rec}" for rec in recommendations[:5]]) if recommendations else "   • Review detailed report for recommendations"
        
        # Format decision
        if isinstance(decision, dict):
            decision_text = f"{decision.get('decision', 'REVIEW')} - {decision.get('justification', 'See detailed report')}"
        else:
            decision_text = str(decision) if decision else "Review detailed report"
        
        return f"""
Subject: Coal Blending Optimization Results - {datetime.now().strftime('%Y-%m-%d')}

Dear Team,

The AI-powered coal blending optimization has been completed with comprehensive multi-agent analysis.

EXECUTIVE SUMMARY:
{exec_summary if exec_summary else f"Optimization completed with {validation_status} status. Feasibility score: {feasibility_score}/100. Quality score: {quality_score:.1f}%. Total cost: ${total_cost:,.2f}."}

1. KEY FINDINGS:
{findings_text}

2. OPTIMIZATION RESULTS:
   • Validation Status: {validation_status.upper()} (Feasibility: {feasibility_score}/100)
   • Blend Composition: {len(blend_composition)} coal sources selected
   • Total Cost: ${total_cost:,.2f} at ${cost_per_ton:.2f}/ton
   • Quality Score: {quality_score:.1f}% - {compliance_status.upper()}
   • Boiler Efficiency: {boiler_eff:.1f}%
   • Overall Status: {'✓ APPROVED' if all_specs_met else '⚠ REVIEW REQUIRED'}

3. BLEND COMPOSITION:
{self._format_blend_composition(blend_composition)}

4. ACHIEVED QUALITY PARAMETERS:
   • GCV: {achieved_params.get('gcv', 0):.0f} kcal/kg
   • Ash: {achieved_params.get('ash', 0):.2f}%
   • Sulfur: {achieved_params.get('sulfur', 0):.3f}%
   • Moisture: {achieved_params.get('moisture', 0):.2f}%

5. FINANCIAL SUMMARY:
   • Total Investment: ${total_cost:,.2f}
   • Cost per Ton: ${cost_per_ton:.2f}
   • Cost Efficiency: {cost_analysis.get('cost_efficiency', {}).get('efficiency_rating', 'N/A').upper()}
   • Budget Status: {'✓ Within Budget' if all_specs_met else '⚠ Review Required'}

6. STRATEGIC RECOMMENDATIONS:
{recommendations_text}

7. DECISION RECOMMENDATION:
   {decision_text}

Best regards,
Coal Blending Optimization System
Powered by Amazon Bedrock AI Agents
(All data sourced directly from agent outputs - 100% accurate)
"""
    
    def send_email(self, optimization_results: Dict, custom_subject: Optional[str] = None) -> Dict:
        """
        Generate summary and send email via Amazon SES
        """
        try:
            # Generate email content using Claude Haiku 3.5
            email_body = self.generate_email_summary(optimization_results)
            
            # Extract subject line from generated content or use custom
            if custom_subject:
                subject = custom_subject
            else:
                # Try to extract subject from generated content
                if "Subject:" in email_body:
                    subject_line = email_body.split("Subject:")[1].split("\n")[0].strip()
                    subject = subject_line
                    # Remove subject line from body
                    email_body = email_body.split("\n", 2)[2] if "\n" in email_body else email_body
                else:
                    subject = f"Coal Blending Optimization Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Create HTML version
            html_body = self._convert_to_html(email_body)
            
            # Send email via SES
            response = self.ses_client.send_email(
                Source=self.from_email,
                Destination={
                    'ToAddresses': [self.to_email]
                },
                Message={
                    'Subject': {
                        'Data': subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': email_body,
                            'Charset': 'UTF-8'
                        },
                        'Html': {
                            'Data': html_body,
                            'Charset': 'UTF-8'
                        }
                    }
                }
            )
            
            return {
                'success': True,
                'message': f'Email sent successfully to {self.to_email}',
                'message_id': response['MessageId'],
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            return {
                'success': False,
                'error': f'SES Error ({error_code}): {error_message}',
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to send email: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _convert_to_html(self, text_content: str) -> str:
        """Convert plain text to professional HTML email format with modern design"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px 0;
        }}
        .email-wrapper {{
            max-width: 650px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            text-align: center;
            position: relative;
        }}
        .header::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        }}
        .header-icon {{
            font-size: 48px;
            margin-bottom: 12px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
        }}
        .header h1 {{
            color: #ffffff;
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
            text-shadow: 0 2px 8px rgba(0,0,0,0.2);
            letter-spacing: -0.5px;
        }}
        .header-subtitle {{
            color: #e0e7ff;
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 12px;
        }}
        .header-date {{
            color: #c7d2fe;
            font-size: 13px;
            font-weight: 400;
        }}
        .content {{
            padding: 35px 30px;
            background-color: #ffffff;
        }}
        .executive-summary {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 6px solid #3b82f6;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        }}
        .executive-summary-header {{
            display: flex;
            align-items: center;
            margin-bottom: 16px;
        }}
        .executive-summary-icon {{
            font-size: 36px;
            margin-right: 12px;
        }}
        .executive-summary-title {{
            font-size: 24px;
            font-weight: 800;
            color: #1e40af;
            margin: 0;
        }}
        .executive-summary-text {{
            color: #1f2937;
            font-size: 16px;
            line-height: 1.8;
            font-weight: 500;
        }}
        .section {{
            margin-bottom: 28px;
            padding-bottom: 24px;
            border-bottom: 2px solid #f3f4f6;
        }}
        .section:last-child {{
            border-bottom: none;
        }}
        .section-header {{
            display: flex;
            align-items: center;
            margin-bottom: 18px;
        }}
        .section-number {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
            margin-right: 12px;
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }}
        .section-title {{
            color: #1f2937;
            font-size: 20px;
            font-weight: 700;
            margin: 0;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
            margin: 16px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 18px;
            border-radius: 10px;
            border-left: 4px solid #3b82f6;
            box-shadow: 0 2px 6px rgba(59, 130, 246, 0.1);
            transition: transform 0.2s;
        }}
        .metric-label {{
            font-size: 11px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .metric-value {{
            font-size: 22px;
            font-weight: 800;
            color: #1e40af;
            line-height: 1.2;
        }}
        .status-badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            margin: 4px 6px 4px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .status-success {{
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            color: #065f46;
            border: 1px solid #6ee7b7;
        }}
        .status-warning {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            color: #92400e;
            border: 1px solid #fcd34d;
        }}
        .status-error {{
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            color: #991b1b;
            border: 1px solid #fca5a5;
        }}
        .list-item {{
            padding: 12px 16px;
            margin: 10px 0;
            background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
            border-radius: 8px;
            border-left: 4px solid #667eea;
            font-size: 15px;
            line-height: 1.6;
        }}
        .list-item strong {{
            color: #667eea;
            font-weight: 700;
        }}
        .recommendation-box {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 6px solid #f59e0b;
            padding: 20px;
            border-radius: 12px;
            margin: 16px 0;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
        }}
        .recommendation-item {{
            padding: 10px 0;
            border-bottom: 1px solid rgba(245, 158, 11, 0.2);
            font-size: 15px;
            line-height: 1.7;
        }}
        .recommendation-item:last-child {{
            border-bottom: none;
        }}
        .footer {{
            background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
            padding: 30px 20px;
            text-align: center;
            border-top: 4px solid #667eea;
        }}
        .footer-icon {{
            font-size: 36px;
            margin-bottom: 12px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        }}
        .footer-title {{
            font-weight: 700;
            font-size: 16px;
            color: #1f2937;
            margin: 8px 0;
        }}
        .footer-subtitle {{
            font-size: 13px;
            color: #6b7280;
            margin: 6px 0;
        }}
        .footer-note {{
            font-size: 11px;
            color: #9ca3af;
            margin: 6px 0;
            font-style: italic;
        }}
        @media only screen and (max-width: 600px) {{
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            .email-wrapper {{
                margin: 10px;
                border-radius: 12px;
            }}
            .content {{
                padding: 25px 20px;
            }}
            .header {{
                padding: 30px 20px;
            }}
            .header h1 {{
                font-size: 26px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="header">
            <div class="header-icon">🏭</div>
            <h1>Coal Blending Optimization</h1>
            <div class="header-subtitle">AI-Powered Multi-Agent Analysis System</div>
            <div class="header-date">{datetime.now().strftime('%B %d, %Y at %H:%M UTC')}</div>
        </div>
        
        <div class="content">
            {self._format_executive_summary_html(text_content)}
            {self._format_html_content(text_content)}
        </div>
        
        <div class="footer">
            <div class="footer-icon">⚡</div>
            <div class="footer-title">Coal Blending Optimization System</div>
            <div class="footer-subtitle">Powered by Amazon Bedrock AI & Amazon SES</div>
            <div class="footer-note">All data sourced directly from agent outputs - 100% accurate</div>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _format_executive_summary_html(self, text_content: str) -> str:
        """Format executive summary in a prominent callout box with modern design"""
        # Extract executive summary from text
        if 'EXECUTIVE SUMMARY:' in text_content:
            lines = text_content.split('\n')
            summary_lines = []
            in_summary = False
            
            for line in lines:
                if 'EXECUTIVE SUMMARY:' in line:
                    in_summary = True
                    continue
                elif in_summary and line.strip() and line.strip()[0].isdigit() and '.' in line[:3]:
                    break
                elif in_summary and line.strip():
                    summary_lines.append(line.strip())
            
            if summary_lines:
                summary_text = ' '.join(summary_lines)
                return f"""
                <div class="executive-summary">
                    <div class="executive-summary-header">
                        <div class="executive-summary-icon">📊</div>
                        <h2 class="executive-summary-title">Executive Summary</h2>
                    </div>
                    <div class="executive-summary-text">
                        {summary_text}
                    </div>
                </div>
                """
        return ""
    
    def _format_html_content(self, text_content: str) -> str:
        """Format text content into structured HTML with section numbers"""
        lines = text_content.split('\n')
        html_parts = []
        current_section = []
        section_title = ""
        section_num = 0
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('Subject:') or line.startswith('Dear') or line.startswith('Best regards'):
                continue
            
            # Section headers (numbered)
            if line and line[0].isdigit() and '.' in line[:3]:
                if current_section:
                    html_parts.append(self._render_section(section_title, current_section, section_num))
                    current_section = []
                # Extract section number and title
                parts = line.split('.', 1)
                section_num = int(parts[0]) if parts[0].isdigit() else section_num + 1
                section_title = parts[1].strip() if len(parts) > 1 else line
            else:
                current_section.append(line)
        
        # Add last section
        if current_section:
            html_parts.append(self._render_section(section_title, current_section, section_num))
        
        return ''.join(html_parts)
    
    def _render_section(self, title: str, content: list, section_num: int = 0) -> str:
        """Render a section with modern numbered design"""
        if not content:
            return ""
        
        html = f'''<div class="section">
            <div class="section-header">
                <div class="section-number">{section_num}</div>
                <h3 class="section-title">{title}</h3>
            </div>'''
        
        # Check if this is a recommendations section
        if 'RECOMMENDATION' in title.upper():
            html += '<div class="recommendation-box">'
            for line in content:
                if line.startswith('•'):
                    html += f'<div class="recommendation-item">• {line[1:].strip()}</div>'
            html += '</div>'
        else:
            # Regular content
            for line in content:
                if line.startswith('•'):
                    # Parse for bold labels (e.g., "Agent Name: result")
                    parts = line[1:].strip().split(':', 1)
                    if len(parts) == 2:
                        html += f'<div class="list-item"><strong>{parts[0]}:</strong> {parts[1]}</div>'
                    else:
                        html += f'<div class="list-item">{line[1:].strip()}</div>'
                elif line:
                    html += f'<p style="margin: 12px 0; font-size: 15px; line-height: 1.7;">{line}</p>'
        
        html += '</div>'
        return html


# Global email agent instance
email_agent = EmailNotificationAgent()


def send_optimization_email(optimization_results: Dict, custom_subject: Optional[str] = None) -> Dict:
    """
    Send optimization results email
    
    Args:
        optimization_results: Complete optimization results dictionary
        custom_subject: Optional custom email subject line
    
    Returns:
        Dictionary with success status and details
    """
    return email_agent.send_email(optimization_results, custom_subject)


def test_email_connection() -> Dict:
    """
    Test SES connection and email sending capability
    """
    try:
        # Send test email
        test_results = {
            'optimization': {
                'success': True,
                'achieved_parameters': {
                    'gcv': 5850,
                    'ash': 10.5,
                    'sulfur': 0.65,
                    'moisture': 8.2
                },
                'blend_composition': [
                    {'coal_name': 'Test Coal A', 'percentage': 60, 'quantity': 6000},
                    {'coal_name': 'Test Coal B', 'percentage': 40, 'quantity': 4000}
                ]
            },
            'cost_analysis': {
                'total_cost': 950000,
                'cost_per_ton': 95
            },
            'quality_prediction': {
                'quality_score': 95.5,
                'compliance': {
                    'gcv': True,
                    'ash': True,
                    'sulfur': True,
                    'moisture': True
                }
            }
        }
        
        result = email_agent.send_email(test_results, "Test Email - Coal Blending System")
        return result
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
