"""
Enhanced Boiler Efficiency Agent with AI Analysis
Combines computational analysis with AI-powered insights
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List

# Try to import LangChain AWS, but make it optional
try:
    import boto3
    from langchain_aws import ChatBedrock
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: langchain_aws not available. Boiler analysis will use computational mode only.")

# Initialize LLM for AI analysis
def get_boiler_llm():
    """Get LangChain LLM instance for boiler analysis"""
    if not LANGCHAIN_AVAILABLE:
        return None
    
    try:
        # Using Claude 3.5 Sonnet v2 - Proven, reliable model for technical analysis
        # Note: Claude Sonnet 4 not yet available in all regions
        return ChatBedrock(
            model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            region_name="us-east-1",
            model_kwargs={
                "temperature": 0.1,  # Low temperature for precise technical analysis
                "max_tokens": 8192,  # Extended for comprehensive Dulong Method analysis
                "top_p": 0.9
            }
        )
    except Exception as e:
        print(f"Warning: Could not initialize Bedrock LLM for boiler analysis: {e}")
        return None

# AI Analysis prompt template
BOILER_AI_PROMPT = """You are an elite boiler efficiency expert with deep knowledge of:
- Thermodynamics and heat transfer
- Coal combustion chemistry and Dulong's Formula for GCV calculation
- Boiler design and operation using ASME PTC 4 methodology
- Performance optimization and heat loss analysis

ANALYZE the provided boiler efficiency data and provide:

1. BOILER EFFICIENCY CALCULATION METHOD (INDIRECT/HEAT LOSS METHOD):
   - This analysis uses the **Indirect Method (Heat Loss Method)** per ASME PTC 4
   - Efficiency = (Heat Input - Total Losses) / Heat Input × 100%
   - Heat losses calculated include:
     * Dry flue gas losses
     * Moisture losses (from coal moisture and H2 combustion)
     * Radiation and convection losses
     * Unburned carbon losses
     * Excess air losses
   
   - Note: The GCV values provided are measured/proximate values, NOT calculated via Dulong's Formula
   - Dulong's Formula (GCV = 8080C + 34500(H - O/8) + 2240S) is used separately when ultimate analysis is available

2. GCV IMPACT ANALYSIS ON BOILER EFFICIENCY (PRIORITY):
   - Explain how the provided GCV affects boiler efficiency:
     * Higher GCV = Higher flame temperature = Better heat transfer = Higher efficiency
     * Lower GCV = More fuel mass needed = Higher flue gas volume = Lower efficiency
     * Optimal GCV range for thermal power plants: 5000-6500 kcal/kg
   
   - Assess the quality of the coal blend based on GCV:
     * <4500 kcal/kg: Low grade, poor efficiency
     * 4500-5500 kcal/kg: Medium grade, acceptable
     * 5500-6500 kcal/kg: High grade, good efficiency
     * >6500 kcal/kg: Premium grade, excellent efficiency
   
   - Provide specific GCV optimization recommendations for blending

2. COMPREHENSIVE EFFICIENCY ANALYSIS:
   - Interpret the calculated efficiency values
   - Explain the significance of each heat loss component:
     * Dry flue gas losses (largest component, ~4-8%)
     * Moisture losses from inherent moisture (~2-6%)
     * Moisture from combustion of hydrogen (~1-2%)
     * Radiation and convection losses (~1-2%)
     * Unburned carbon losses (~0.5-2%)
   - Assess combustion quality based on excess air percentage
   - Evaluate operational implications

3. ENGINEERING INSIGHTS:
   - Why is the efficiency at this level?
   - What are the dominant loss mechanisms?
   - How does coal quality (GCV, moisture, ash, sulfur) affect performance?
   - What are the thermodynamic limitations?
   - Impact of operational parameters (excess air, flue gas temperature)
   - Relationship between GCV and achievable efficiency

4. HEAT LOSS BREAKDOWN ANALYSIS:
   - Analyze each heat loss component in detail:
     * Moisture loss: Latent heat of vaporization (584 kcal/kg water)
     * Ash loss: Sensible heat carried away with ash
     * Excess air loss: Heat carried away by excess combustion air
     * Radiation loss: Heat radiated from boiler surface (~1-2%)
     * Unburned carbon loss: Combustible material in ash
   
   - Identify the dominant loss mechanism
   - Calculate percentage contribution of each loss
   - Compare with industry benchmarks (ASME PTC 4, IS 8753)
   
   Note: If ultimate analysis (C, H, O, S) is available, Dulong's Formula can be used 
   to validate GCV: GCV = 8080C + 34500(H - O/8) + 2240S

5. OPERATIONAL RECOMMENDATIONS:
   - Specific actions to improve efficiency (prioritized list)
   - Blend optimization suggestions based on GCV analysis
   - Operational parameter adjustments:
     * Optimal excess air percentage
     * Flue gas temperature control
     * Air preheater optimization
   - Maintenance considerations
   - Target efficiency achievability assessment
   - Cost-benefit analysis of improvements

6. RISK ASSESSMENT:
   - Slagging and fouling potential based on ash and alkali content
   - Corrosion risks from sulfur content
   - Operational challenges with current blend
   - Long-term performance concerns
   - Mitigation strategies

7. COMPARATIVE ANALYSIS:
   - Compare to industry standards (ASME PTC 4, IS 8753)
   - Typical efficiency range for this coal quality
   - Benchmark against target efficiency
   - Identify red flags or exceptional performance indicators
   - Best practices from similar installations

Be specific, technical, and actionable. Provide real engineering value.
Use industry standards (ASME PTC 4, IS 8753).
Include numerical calculations and formulas where relevant.
EMPHASIZE Dulong Method GCV calculations and their impact on efficiency.

BOILER EFFICIENCY DATA:
{data}

Provide your expert analysis with detailed Dulong Method GCV calculations:"""


class EnhancedBoilerEfficiencyAgent:
    """
    Enhanced agent combining computational analysis with AI insights
    """
    
    def __init__(self):
        self.efficiency_factors = {
            'combustion_efficiency': 0.98,
            'radiation_loss': 0.01,
            'convection_loss': 0.005,
            'unburnt_carbon_loss': 0.005,
        }
    
    def calculate_boiler_efficiency(self, gcv: float, moisture: float, ash: float,
                                   excess_air: float = 20.0, target_efficiency: float = 85.0) -> Dict:
        """
        Calculate boiler efficiency with comprehensive analysis
        
        Args:
            gcv: Gross Calorific Value (kcal/kg)
            moisture: Moisture content (%)
            ash: Ash content (%)
            excess_air: Excess air percentage
            target_efficiency: Target boiler efficiency (default 85%)
        
        Returns:
            Complete efficiency analysis
        """
        # Heat losses
        moisture_loss = moisture * 5.84
        ash_loss = ash * 0.5
        excess_air_loss = excess_air * 0.3
        
        # Radiation and convection losses (typically 1-2%)
        radiation_loss = gcv * 0.015
        
        # Unburned carbon loss (depends on ash and combustion quality)
        unburned_carbon_loss = ash * 0.1
        
        # Total heat input
        heat_input = gcv
        
        # Total losses
        total_losses = (moisture_loss + ash_loss + excess_air_loss + 
                       radiation_loss + unburned_carbon_loss)
        
        # Boiler efficiency (indirect method)
        efficiency = ((heat_input - total_losses) / heat_input) * 100
        
        # Apply combustion efficiency factor
        actual_efficiency = efficiency * self.efficiency_factors['combustion_efficiency']
        
        # Calculate efficiency margin
        efficiency_margin = actual_efficiency - target_efficiency
        
        # Determine efficiency rating
        if actual_efficiency >= target_efficiency + 2:
            rating = "Excellent"
        elif actual_efficiency >= target_efficiency:
            rating = "Good"
        elif actual_efficiency >= target_efficiency - 2:
            rating = "Fair"
        else:
            rating = "Poor"
        
        return {
            'predicted_efficiency': actual_efficiency,
            'target_efficiency': target_efficiency,
            'efficiency_margin': efficiency_margin,
            'efficiency_rating': rating,
            'heat_input': heat_input,
            'heat_losses': {
                'moisture_loss': moisture_loss,
                'ash_loss': ash_loss,
                'excess_air_loss': excess_air_loss,
                'radiation_loss': radiation_loss,
                'unburned_carbon_loss': unburned_carbon_loss,
                'total_losses': total_losses
            },
            'net_heat_available': heat_input - total_losses,
            'heat_rate': 860 / (actual_efficiency / 100)  # kcal/kWh
        }
    
    def estimate_ultimate_analysis_from_gcv(self, gcv: float, moisture: float, ash: float, sulfur: float) -> Dict:
        """
        Estimate ultimate analysis (C, H, O) from proximate analysis using empirical correlations
        Based on typical coal composition relationships
        """
        # Dry ash-free (DAF) basis GCV
        daf_gcv = gcv * 100 / (100 - moisture - ash)
        
        # Empirical correlations for bituminous coal
        # Carbon (DAF): Typically 75-90% for thermal coals
        carbon_daf = 75 + (daf_gcv - 5000) / 100  # Increases with GCV
        carbon_daf = min(90, max(70, carbon_daf))  # Clamp between 70-90%
        
        # Hydrogen (DAF): Typically 4-6%
        hydrogen_daf = 5.0 + (daf_gcv - 5500) / 1000  # Slight increase with GCV
        hydrogen_daf = min(6.5, max(3.5, hydrogen_daf))
        
        # Oxygen (DAF): Decreases as rank increases
        oxygen_daf = 20 - (daf_gcv - 5000) / 200  # Decreases with GCV
        oxygen_daf = min(25, max(5, oxygen_daf))
        
        # Nitrogen (DAF): Typically 1-2%
        nitrogen_daf = 1.5
        
        # Sulfur is known from proximate analysis
        sulfur_daf = sulfur * 100 / (100 - moisture - ash)
        
        # Normalize to 100% (DAF basis)
        total = carbon_daf + hydrogen_daf + oxygen_daf + nitrogen_daf + sulfur_daf
        carbon_daf = carbon_daf / total * 100
        hydrogen_daf = hydrogen_daf / total * 100
        oxygen_daf = oxygen_daf / total * 100
        nitrogen_daf = nitrogen_daf / total * 100
        sulfur_daf = sulfur_daf / total * 100
        
        # Convert to as-received basis
        dry_factor = (100 - moisture) / 100
        combustible_factor = (100 - moisture - ash) / 100
        
        carbon_ar = carbon_daf * combustible_factor
        hydrogen_ar = hydrogen_daf * combustible_factor
        oxygen_ar = oxygen_daf * combustible_factor
        nitrogen_ar = nitrogen_daf * combustible_factor
        sulfur_ar = sulfur
        
        return {
            'carbon': carbon_ar,
            'hydrogen': hydrogen_ar,
            'oxygen': oxygen_ar,
            'nitrogen': nitrogen_ar,
            'sulfur': sulfur_ar,
            'ash': ash,
            'moisture': moisture,
            'basis': 'as-received',
            'estimation_method': 'Empirical correlation from GCV',
            'note': 'Estimated values - actual ultimate analysis recommended for precision'
        }
    
    def calculate_dulong_gcv(self, carbon: float, hydrogen: float, oxygen: float, sulfur: float) -> Dict:
        """
        Calculate theoretical GCV using Dulong's Formula
        GCV (kcal/kg) = 8080*C + 34500*(H - O/8) + 2240*S
        """
        # Convert percentages to fractions
        C = carbon / 100
        H = hydrogen / 100
        O = oxygen / 100
        S = sulfur / 100
        
        # Calculate contributions
        carbon_contribution = 8080 * C
        hydrogen_contribution = 34500 * (H - O/8)
        sulfur_contribution = 2240 * S
        
        # Total GCV
        gcv_calculated = carbon_contribution + hydrogen_contribution + sulfur_contribution
        
        return {
            'gcv_dulong': gcv_calculated,
            'carbon_contribution': carbon_contribution,
            'hydrogen_contribution': hydrogen_contribution,
            'sulfur_contribution': sulfur_contribution,
            'formula': "GCV = 8080*C + 34500*(H - O/8) + 2240*S",
            'carbon_percent': carbon,
            'hydrogen_percent': hydrogen,
            'oxygen_percent': oxygen,
            'sulfur_percent': sulfur
        }
    
    def analyze_with_ai(self, coal_data: List[Dict], blend_percentages: List[float],
                       target_efficiency: float = 85.0) -> Dict:
        """
        Perform comprehensive analysis with AI insights including Dulong's method
        
        Args:
            coal_data: List of coal properties
            blend_percentages: Blend percentages
            target_efficiency: Target efficiency (default 85% if not specified)
        
        Returns:
            Complete analysis with AI insights and Dulong's method calculations
        """
        # Calculate weighted average properties
        weighted_gcv = sum(coal['gcv'] * pct / 100 for coal, pct in zip(coal_data, blend_percentages))
        weighted_moisture = sum(coal['moisture'] * pct / 100 for coal, pct in zip(coal_data, blend_percentages))
        weighted_ash = sum(coal['ash'] * pct / 100 for coal, pct in zip(coal_data, blend_percentages))
        weighted_sulfur = sum(coal['sulfur'] * pct / 100 for coal, pct in zip(coal_data, blend_percentages))
        
        # Estimate ultimate analysis and calculate Dulong GCV
        ultimate_analysis = self.estimate_ultimate_analysis_from_gcv(
            weighted_gcv, weighted_moisture, weighted_ash, weighted_sulfur
        )
        
        dulong_result = self.calculate_dulong_gcv(
            ultimate_analysis['carbon'],
            ultimate_analysis['hydrogen'],
            ultimate_analysis['oxygen'],
            ultimate_analysis['sulfur']
        )
        
        # Calculate difference between measured and Dulong GCV
        gcv_difference = weighted_gcv - dulong_result['gcv_dulong']
        gcv_difference_percent = (gcv_difference / weighted_gcv) * 100
        
        # Calculate boiler efficiency
        efficiency_data = self.calculate_boiler_efficiency(
            weighted_gcv, weighted_moisture, weighted_ash, target_efficiency=target_efficiency
        )
        
        # Generate visualizations
        visualizations = self._generate_comprehensive_visualizations(
            weighted_gcv, weighted_moisture, weighted_ash, weighted_sulfur,
            efficiency_data, coal_data, blend_percentages, target_efficiency
        )
        
        # Prepare data for AI analysis with Dulong's method
        analysis_context = f"""
BOILER EFFICIENCY ANALYSIS DATA:

COAL BLEND PROPERTIES (PROXIMATE ANALYSIS):
- Weighted GCV (Measured): {weighted_gcv:.2f} kcal/kg
- Weighted Moisture: {weighted_moisture:.2f}%
- Weighted Ash: {weighted_ash:.2f}%
- Weighted Sulfur: {weighted_sulfur:.2f}%

DULONG'S FORMULA ANALYSIS (THEORETICAL GCV CALCULATION):
Formula: GCV = 8080*C + 34500*(H - O/8) + 2240*S

ESTIMATED ULTIMATE ANALYSIS (As-Received Basis):
- Carbon (C): {ultimate_analysis['carbon']:.2f}%
- Hydrogen (H): {ultimate_analysis['hydrogen']:.2f}%
- Oxygen (O): {ultimate_analysis['oxygen']:.2f}%
- Nitrogen (N): {ultimate_analysis['nitrogen']:.2f}%
- Sulfur (S): {ultimate_analysis['sulfur']:.2f}%
- Ash: {ultimate_analysis['ash']:.2f}%
- Moisture: {ultimate_analysis['moisture']:.2f}%
Note: {ultimate_analysis['note']}

DULONG GCV CALCULATION BREAKDOWN:
- Carbon Contribution: {dulong_result['carbon_contribution']:.2f} kcal/kg (8080 × {ultimate_analysis['carbon']:.2f}%)
- Hydrogen Contribution: {dulong_result['hydrogen_contribution']:.2f} kcal/kg (34500 × ({ultimate_analysis['hydrogen']:.2f}% - {ultimate_analysis['oxygen']:.2f}%/8))
- Sulfur Contribution: {dulong_result['sulfur_contribution']:.2f} kcal/kg (2240 × {ultimate_analysis['sulfur']:.2f}%)
- **Calculated GCV (Dulong): {dulong_result['gcv_dulong']:.2f} kcal/kg**

GCV COMPARISON:
- Measured GCV: {weighted_gcv:.2f} kcal/kg
- Dulong GCV: {dulong_result['gcv_dulong']:.2f} kcal/kg
- Difference: {gcv_difference:.2f} kcal/kg ({gcv_difference_percent:.1f}%)
- Analysis: {'Good agreement' if abs(gcv_difference_percent) < 5 else 'Fair agreement' if abs(gcv_difference_percent) < 10 else 'Significant deviation'}

EFFICIENCY RESULTS (HEAT LOSS METHOD - ASME PTC 4):
- Predicted Efficiency: {efficiency_data['predicted_efficiency']:.2f}%
- Target Efficiency: {target_efficiency}%
- Efficiency Margin: {efficiency_data['efficiency_margin']:.2f}%
- Rating: {efficiency_data['efficiency_rating']}
- Heat Rate: {efficiency_data['heat_rate']:.2f} kcal/kWh

HEAT LOSSES BREAKDOWN:
- Moisture Loss: {efficiency_data['heat_losses']['moisture_loss']:.2f} kcal/kg ({efficiency_data['heat_losses']['moisture_loss']/weighted_gcv*100:.1f}%)
- Ash Loss: {efficiency_data['heat_losses']['ash_loss']:.2f} kcal/kg ({efficiency_data['heat_losses']['ash_loss']/weighted_gcv*100:.1f}%)
- Excess Air Loss: {efficiency_data['heat_losses']['excess_air_loss']:.2f} kcal/kg ({efficiency_data['heat_losses']['excess_air_loss']/weighted_gcv*100:.1f}%)
- Radiation Loss: {efficiency_data['heat_losses']['radiation_loss']:.2f} kcal/kg ({efficiency_data['heat_losses']['radiation_loss']/weighted_gcv*100:.1f}%)
- Unburned Carbon Loss: {efficiency_data['heat_losses']['unburned_carbon_loss']:.2f} kcal/kg ({efficiency_data['heat_losses']['unburned_carbon_loss']/weighted_gcv*100:.1f}%)
- Total Losses: {efficiency_data['heat_losses']['total_losses']:.2f} kcal/kg ({efficiency_data['heat_losses']['total_losses']/weighted_gcv*100:.1f}%)

INDIVIDUAL COALS IN BLEND:
{self._format_coal_data(coal_data, blend_percentages)}

Provide comprehensive analysis including detailed Dulong's method interpretation, GCV validation, and efficiency optimization recommendations.
"""
        
        # Get AI analysis (optional, falls back to computational)
        ai_insights = self._get_ai_analysis(analysis_context)
        
        return {
            'efficiency_analysis': efficiency_data,
            'dulong_analysis': {
                'ultimate_analysis': ultimate_analysis,
                'dulong_gcv': dulong_result,
                'gcv_comparison': {
                    'measured_gcv': weighted_gcv,
                    'dulong_gcv': dulong_result['gcv_dulong'],
                    'difference': gcv_difference,
                    'difference_percent': gcv_difference_percent,
                    'agreement': 'Good' if abs(gcv_difference_percent) < 5 else 'Fair' if abs(gcv_difference_percent) < 10 else 'Poor'
                }
            },
            'blend_properties': {
                'weighted_gcv': weighted_gcv,
                'weighted_moisture': weighted_moisture,
                'weighted_ash': weighted_ash,
                'weighted_sulfur': weighted_sulfur
            },
            'visualizations': visualizations,
            'ai_insights': ai_insights,
            'coal_data': coal_data,
            'blend_percentages': blend_percentages,
            'computational_insights': self._generate_computational_insights(
                efficiency_data, weighted_gcv, weighted_moisture, weighted_ash, target_efficiency
            )
        }
    
    def _get_ai_analysis(self, analysis_context: str) -> str:
        """Get AI analysis with fallback to computational insights"""
        llm = get_boiler_llm()
        
        if llm:
            try:
                print("🤖 Generating AI-powered boiler efficiency analysis...")
                prompt = BOILER_AI_PROMPT.format(data=analysis_context)
                response = llm.invoke(prompt)
                return response.content if hasattr(response, 'content') else str(response)
            except Exception as e:
                print(f"⚠️ AI analysis unavailable: {e}")
                return self._generate_fallback_analysis()
        else:
            return self._generate_fallback_analysis()
    
    def _generate_fallback_analysis(self) -> str:
        """Generate basic analysis when AI is unavailable"""
        return """
BOILER EFFICIENCY ANALYSIS (Computational Mode)

The boiler efficiency has been calculated using standard thermodynamic principles 
and ASME PTC 4 methodology. Key factors affecting efficiency:

1. HEAT LOSSES:
   - Dry flue gas losses are the dominant factor
   - Moisture losses depend on coal moisture content
   - Radiation and unburned carbon contribute smaller losses

2. OPTIMIZATION OPPORTUNITIES:
   - Reduce excess air to minimize flue gas losses
   - Select lower moisture coals to reduce evaporation losses
   - Maintain proper combustion to minimize unburned carbon
   - Optimize air preheater performance

3. OPERATIONAL RECOMMENDATIONS:
   - Monitor flue gas temperature and oxygen levels
   - Maintain proper air-fuel ratio
   - Regular soot blowing to maintain heat transfer
   - Periodic boiler tube cleaning

For detailed AI-powered insights, ensure AWS Bedrock access is configured.
"""
    
    def _format_coal_data(self, coal_data: List[Dict], blend_percentages: List[float]) -> str:
        """Format coal data for AI analysis"""
        formatted = []
        for coal, pct in zip(coal_data, blend_percentages):
            formatted.append(
                f"- {coal['name']} ({pct:.1f}%): "
                f"GCV={coal['gcv']} kcal/kg, "
                f"Ash={coal['ash']}%, "
                f"Moisture={coal['moisture']}%, "
                f"Sulfur={coal['sulfur']}%"
            )
        return "\n".join(formatted)
    
    def _generate_computational_insights(self, efficiency_data: Dict, gcv: float,
                                        moisture: float, ash: float, target: float) -> List[str]:
        """Generate computational insights"""
        insights = []
        
        eff = efficiency_data['predicted_efficiency']
        margin = efficiency_data['efficiency_margin']
        
        # Efficiency status
        if margin >= 0:
            insights.append(f"✅ Efficiency target achieved! {margin:.2f}% above target.")
        else:
            insights.append(f"⚠️ Efficiency {abs(margin):.2f}% below target. Optimization needed.")
        
        # GCV analysis
        if gcv < 5000:
            insights.append("🔥 Low GCV (<5000). Consider higher quality coals.")
        elif gcv > 6500:
            insights.append("🔥 Excellent GCV (>6500). Premium coal quality.")
        else:
            insights.append(f"🔥 GCV ({gcv:.0f}) is acceptable for thermal power generation.")
        
        # Loss analysis
        losses = efficiency_data['heat_losses']
        dominant_loss = max(losses.items(), key=lambda x: x[1] if x[0] != 'total_losses' else 0)
        insights.append(f"📊 Dominant heat loss: {dominant_loss[0].replace('_', ' ').title()} ({dominant_loss[1]:.2f} kcal/kg)")
        
        # Heat rate
        heat_rate = efficiency_data['heat_rate']
        if heat_rate < 2500:
            insights.append(f"⚡ Excellent heat rate: {heat_rate:.0f} kcal/kWh")
        elif heat_rate < 3000:
            insights.append(f"⚡ Good heat rate: {heat_rate:.0f} kcal/kWh")
        else:
            insights.append(f"⚡ Heat rate needs improvement: {heat_rate:.0f} kcal/kWh")
        
        return insights
    
    def _generate_comprehensive_visualizations(self, gcv: float, moisture: float, ash: float,
                                              sulfur: float, efficiency_data: Dict,
                                              coal_data: List[Dict], blend_percentages: List[float],
                                              target_efficiency: float) -> Dict:
        """Generate comprehensive visualizations"""
        visualizations = {}
        
        # 1. Efficiency Gauge Chart
        fig1, ax1 = plt.subplots(figsize=(10, 6), subplot_kw={'projection': 'polar'})
        
        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = np.ones(100)
        
        # Color zones
        ax1.fill_between(theta[0:33], 0, 1, color='red', alpha=0.3, label='Poor (<80%)')
        ax1.fill_between(theta[33:66], 0, 1, color='yellow', alpha=0.3, label='Fair (80-85%)')
        ax1.fill_between(theta[66:100], 0, 1, color='green', alpha=0.3, label='Good (>85%)')
        
        # Efficiency needle
        eff_angle = (efficiency_data['predicted_efficiency'] - 70) / 30 * np.pi
        ax1.plot([eff_angle, eff_angle], [0, 0.9], 'b-', linewidth=4)
        ax1.plot(eff_angle, 0.9, 'bo', markersize=15)
        
        # Target marker
        target_angle = (target_efficiency - 70) / 30 * np.pi
        ax1.plot([target_angle, target_angle], [0, 0.95], 'r--', linewidth=2, label='Target')
        
        ax1.set_ylim(0, 1)
        ax1.set_theta_zero_location('W')
        ax1.set_theta_direction(1)
        ax1.set_xticks(np.linspace(0, np.pi, 7))
        ax1.set_xticklabels(['70%', '75%', '80%', '85%', '90%', '95%', '100%'])
        ax1.set_yticks([])
        ax1.set_title(f'Boiler Efficiency: {efficiency_data["predicted_efficiency"]:.2f}%\n'
                     f'Rating: {efficiency_data["efficiency_rating"]}',
                     fontsize=14, fontweight='bold', pad=20)
        ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        visualizations['efficiency_gauge'] = self._fig_to_base64(fig1)
        plt.close(fig1)
        
        # 2. Heat Loss Waterfall
        fig2, ax2 = plt.subplots(figsize=(12, 7))
        
        categories = ['Heat\nInput', 'Moisture\nLoss', 'Ash\nLoss', 'Excess Air\nLoss',
                     'Radiation\nLoss', 'Unburned\nCarbon', 'Net Heat\nOutput']
        
        losses = efficiency_data['heat_losses']
        values = [
            gcv,
            -losses['moisture_loss'],
            -losses['ash_loss'],
            -losses['excess_air_loss'],
            -losses['radiation_loss'],
            -losses['unburned_carbon_loss'],
            efficiency_data['net_heat_available']
        ]
        
        # Calculate positions
        cumulative = [values[0]]
        for i in range(1, len(values) - 1):
            cumulative.append(cumulative[-1] + values[i])
        cumulative.append(values[-1])
        
        colors = ['green'] + ['red'] * 5 + ['blue']
        
        for i in range(len(categories)):
            if i == 0 or i == len(categories) - 1:
                ax2.bar(i, abs(values[i]), color=colors[i], alpha=0.7, edgecolor='black', linewidth=2)
                ax2.text(i, abs(values[i])/2, f'{abs(values[i]):.0f}', 
                        ha='center', va='center', fontweight='bold', fontsize=10)
            else:
                bottom = cumulative[i]
                ax2.bar(i, abs(values[i]), bottom=bottom, color=colors[i], 
                       alpha=0.7, edgecolor='black', linewidth=2)
                ax2.text(i, bottom + abs(values[i])/2, f'{abs(values[i]):.0f}', 
                        ha='center', va='center', fontweight='bold', fontsize=9)
        
        ax2.set_xticks(range(len(categories)))
        ax2.set_xticklabels(categories, fontsize=10, fontweight='bold')
        ax2.set_ylabel('Heat Value (kcal/kg)', fontsize=12, fontweight='bold')
        ax2.set_title('Heat Balance Waterfall Analysis', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        visualizations['heat_waterfall'] = self._fig_to_base64(fig2)
        plt.close(fig2)
        
        # 3. Loss Distribution Pie Chart
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        
        loss_values = [
            losses['moisture_loss'],
            losses['ash_loss'],
            losses['excess_air_loss'],
            losses['radiation_loss'],
            losses['unburned_carbon_loss']
        ]
        loss_labels = ['Moisture', 'Ash', 'Excess Air', 'Radiation', 'Unburned Carbon']
        colors_pie = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
        
        explode = tuple(0.05 if v == max(loss_values) else 0 for v in loss_values)
        
        wedges, texts, autotexts = ax3.pie(loss_values, labels=loss_labels, autopct='%1.1f%%',
                                           startangle=90, colors=colors_pie, explode=explode,
                                           shadow=True, textprops={'fontweight': 'bold'})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
        
        ax3.set_title('Heat Loss Distribution', fontsize=14, fontweight='bold')
        
        visualizations['loss_distribution'] = self._fig_to_base64(fig3)
        plt.close(fig3)
        
        # 4. Sensitivity Analysis
        fig4, ax4 = plt.subplots(figsize=(12, 7))
        
        param_range = np.linspace(0.7, 1.3, 30)
        
        gcv_sensitivity = []
        moisture_sensitivity = []
        ash_sensitivity = []
        
        for factor in param_range:
            eff1 = self.calculate_boiler_efficiency(gcv * factor, moisture, ash)
            gcv_sensitivity.append(eff1['predicted_efficiency'])
            
            eff2 = self.calculate_boiler_efficiency(gcv, moisture * factor, ash)
            moisture_sensitivity.append(eff2['predicted_efficiency'])
            
            eff3 = self.calculate_boiler_efficiency(gcv, moisture, ash * factor)
            ash_sensitivity.append(eff3['predicted_efficiency'])
        
        ax4.plot(param_range * 100, gcv_sensitivity, 'b-', linewidth=3, label='GCV Impact', marker='o', markersize=4)
        ax4.plot(param_range * 100, moisture_sensitivity, 'r-', linewidth=3, label='Moisture Impact', marker='s', markersize=4)
        ax4.plot(param_range * 100, ash_sensitivity, 'g-', linewidth=3, label='Ash Impact', marker='^', markersize=4)
        
        ax4.axvline(x=100, color='gray', linestyle='--', linewidth=2, alpha=0.7, label='Baseline')
        ax4.axhline(y=target_efficiency, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Target')
        
        ax4.set_xlabel('Parameter Value (% of baseline)', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Boiler Efficiency (%)', fontsize=12, fontweight='bold')
        ax4.set_title('Sensitivity Analysis: Impact of Coal Parameters on Efficiency', 
                     fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.legend(fontsize=11, loc='best')
        plt.tight_layout()
        
        visualizations['sensitivity_analysis'] = self._fig_to_base64(fig4)
        plt.close(fig4)
        
        return visualizations
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=120, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return img_base64


# Main function for integration
def analyze_boiler_efficiency_enhanced(coal_data: List[Dict], blend_percentages: List[float],
                                      target_efficiency: float = None) -> Dict:
    """
    Enhanced boiler efficiency analysis with AI insights
    
    Args:
        coal_data: List of coal properties
        blend_percentages: Blend percentages
        target_efficiency: Target efficiency (defaults to 85% if None)
    
    Returns:
        Comprehensive analysis with AI insights and visualizations
    """
    # Default to 85% if not specified
    if target_efficiency is None:
        target_efficiency = 85.0
    
    agent = EnhancedBoilerEfficiencyAgent()
    return agent.analyze_with_ai(coal_data, blend_percentages, target_efficiency)
