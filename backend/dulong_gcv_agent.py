"""
Dulong's Formula GCV Calculation Agent
Calculates Gross Calorific Value using Dulong's formula from ultimate analysis
"""

from typing import Dict, Optional
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage


class DulongGCVAgent:
    """
    Agent that calculates GCV using Dulong's formula
    
    Dulong's Formula:
    GCV (kcal/kg) = 8080*C + 34500*(H - O/8) + 2240*S
    
    Where:
    - C = Carbon content (%)
    - H = Hydrogen content (%)
    - O = Oxygen content (%)
    - S = Sulfur content (%)
    """
    
    def __init__(self):
        self.llm = self._create_llm()
    
    def _create_llm(self):
        """Create Bedrock LLM instance"""
        from botocore.config import Config
        
        config = Config(
            read_timeout=300,
            connect_timeout=60,
            retries={'max_attempts': 3}
        )
        
        return ChatBedrock(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            region_name="us-east-1",
            model_kwargs={
                "temperature": 0.3,
                "max_tokens": 4000
            },
            config=config
        )
    
    def calculate_gcv_dulong(
        self,
        carbon: float,
        hydrogen: float,
        oxygen: float,
        sulfur: float,
        nitrogen: Optional[float] = None,
        ash: Optional[float] = None,
        moisture: Optional[float] = None
    ) -> Dict:
        """
        Calculate GCV using Dulong's formula
        
        Args:
            carbon: Carbon content (%)
            hydrogen: Hydrogen content (%)
            oxygen: Oxygen content (%)
            sulfur: Sulfur content (%)
            nitrogen: Nitrogen content (%) - optional
            ash: Ash content (%) - optional
            moisture: Moisture content (%) - optional
        
        Returns:
            Dictionary with GCV calculation results and analysis
        """
        try:
            # Validate inputs
            if any(x < 0 or x > 100 for x in [carbon, hydrogen, oxygen, sulfur]):
                return {
                    'success': False,
                    'error': 'All percentages must be between 0 and 100'
                }
            
            # Calculate GCV using Dulong's formula
            # GCV (kcal/kg) = 8080*C + 34500*(H - O/8) + 2240*S
            gcv_gross = (
                8080 * carbon / 100 +
                34500 * (hydrogen / 100 - oxygen / 800) +
                2240 * sulfur / 100
            )
            
            # Calculate Net Calorific Value (NCV)
            # NCV = GCV - 600 * (9H + M) / 100
            # Where M is moisture content
            moisture_val = moisture if moisture is not None else 0
            ncv = gcv_gross - 600 * (9 * hydrogen / 100 + moisture_val / 100)
            
            # Calculate on dry basis if moisture is provided
            gcv_dry = None
            ncv_dry = None
            if moisture is not None and moisture > 0:
                dry_factor = 100 / (100 - moisture)
                gcv_dry = gcv_gross * dry_factor
                ncv_dry = ncv * dry_factor
            
            # Calculate on dry ash-free basis if both moisture and ash provided
            gcv_daf = None
            ncv_daf = None
            if moisture is not None and ash is not None:
                daf_factor = 100 / (100 - moisture - ash)
                gcv_daf = gcv_gross * daf_factor
                ncv_daf = ncv * daf_factor
            
            # Build result
            result = {
                'success': True,
                'gcv_as_received': round(gcv_gross, 2),
                'ncv_as_received': round(ncv, 2),
                'formula_used': "Dulong's Formula",
                'formula': "GCV = 8080*C + 34500*(H - O/8) + 2240*S",
                'inputs': {
                    'carbon': carbon,
                    'hydrogen': hydrogen,
                    'oxygen': oxygen,
                    'sulfur': sulfur,
                    'nitrogen': nitrogen,
                    'ash': ash,
                    'moisture': moisture
                },
                'calculations': {
                    'carbon_contribution': round(8080 * carbon / 100, 2),
                    'hydrogen_contribution': round(34500 * (hydrogen / 100 - oxygen / 800), 2),
                    'sulfur_contribution': round(2240 * sulfur / 100, 2)
                }
            }
            
            # Add dry basis if calculated
            if gcv_dry is not None:
                result['gcv_dry_basis'] = round(gcv_dry, 2)
                result['ncv_dry_basis'] = round(ncv_dry, 2)
            
            # Add DAF basis if calculated
            if gcv_daf is not None:
                result['gcv_daf_basis'] = round(gcv_daf, 2)
                result['ncv_daf_basis'] = round(ncv_daf, 2)
            
            # Get AI analysis
            analysis = self._get_ai_analysis(result)
            result['ai_analysis'] = analysis
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Calculation error: {str(e)}'
            }
    
    def _get_ai_analysis(self, calculation_result: Dict) -> str:
        """Get AI analysis of the GCV calculation"""
        
        system_prompt = """You are an expert coal scientist specializing in calorific value analysis and Dulong's formula. 
        Provide detailed analysis of GCV calculations, quality assessment, and practical implications."""
        
        user_prompt = f"""Analyze this GCV calculation using Dulong's formula:

**Calculation Results:**
- GCV (as received): {calculation_result['gcv_as_received']} kcal/kg
- NCV (as received): {calculation_result['ncv_as_received']} kcal/kg

**Ultimate Analysis:**
- Carbon: {calculation_result['inputs']['carbon']}%
- Hydrogen: {calculation_result['inputs']['hydrogen']}%
- Oxygen: {calculation_result['inputs']['oxygen']}%
- Sulfur: {calculation_result['inputs']['sulfur']}%

**Contribution Breakdown:**
- Carbon contribution: {calculation_result['calculations']['carbon_contribution']} kcal/kg
- Hydrogen contribution: {calculation_result['calculations']['hydrogen_contribution']} kcal/kg
- Sulfur contribution: {calculation_result['calculations']['sulfur_contribution']} kcal/kg

Please provide:
1. **Quality Assessment**: Is this high, medium, or low quality coal based on GCV?
2. **Composition Analysis**: How do the carbon, hydrogen, and oxygen ratios affect the GCV?
3. **Practical Implications**: What does this GCV mean for power generation?
4. **Comparison**: How does this compare to typical coal grades?
5. **Recommendations**: Any suggestions for blending or usage?

Keep the analysis concise but insightful (3-4 paragraphs)."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
    
    def validate_ultimate_analysis(
        self,
        carbon: float,
        hydrogen: float,
        oxygen: float,
        sulfur: float,
        nitrogen: float,
        ash: float,
        moisture: float
    ) -> Dict:
        """
        Validate that ultimate analysis components sum to approximately 100%
        
        Returns:
            Dictionary with validation results
        """
        total = carbon + hydrogen + oxygen + sulfur + nitrogen + ash + moisture
        
        is_valid = 98 <= total <= 102  # Allow 2% tolerance
        
        return {
            'valid': is_valid,
            'total': round(total, 2),
            'difference': round(total - 100, 2),
            'message': 'Valid ultimate analysis' if is_valid else f'Total is {total}%, should be ~100%',
            'components': {
                'carbon': carbon,
                'hydrogen': hydrogen,
                'oxygen': oxygen,
                'sulfur': sulfur,
                'nitrogen': nitrogen,
                'ash': ash,
                'moisture': moisture
            }
        }
    
    def estimate_missing_component(
        self,
        carbon: Optional[float] = None,
        hydrogen: Optional[float] = None,
        oxygen: Optional[float] = None,
        sulfur: Optional[float] = None,
        nitrogen: Optional[float] = None,
        ash: Optional[float] = None,
        moisture: Optional[float] = None
    ) -> Dict:
        """
        Estimate missing component if 6 out of 7 are provided
        
        Returns:
            Dictionary with estimated component
        """
        components = {
            'carbon': carbon,
            'hydrogen': hydrogen,
            'oxygen': oxygen,
            'sulfur': sulfur,
            'nitrogen': nitrogen,
            'ash': ash,
            'moisture': moisture
        }
        
        # Count provided components
        provided = {k: v for k, v in components.items() if v is not None}
        missing = [k for k, v in components.items() if v is None]
        
        if len(missing) != 1:
            return {
                'success': False,
                'error': f'Need exactly 6 components to estimate the 7th. Provided: {len(provided)}, Missing: {len(missing)}'
            }
        
        # Calculate missing component
        total_provided = sum(provided.values())
        missing_component = missing[0]
        estimated_value = 100 - total_provided
        
        if estimated_value < 0:
            return {
                'success': False,
                'error': f'Provided components sum to {total_provided}%, which exceeds 100%'
            }
        
        return {
            'success': True,
            'missing_component': missing_component,
            'estimated_value': round(estimated_value, 2),
            'provided_components': provided,
            'total_provided': round(total_provided, 2)
        }
    
    def compare_gcv_methods(
        self,
        carbon: float,
        hydrogen: float,
        oxygen: float,
        sulfur: float,
        measured_gcv: Optional[float] = None
    ) -> Dict:
        """
        Compare Dulong's formula with measured GCV (if available)
        
        Returns:
            Dictionary with comparison results
        """
        # Calculate using Dulong's formula
        dulong_result = self.calculate_gcv_dulong(carbon, hydrogen, oxygen, sulfur)
        
        if not dulong_result['success']:
            return dulong_result
        
        calculated_gcv = dulong_result['gcv_as_received']
        
        result = {
            'success': True,
            'dulong_gcv': calculated_gcv,
            'formula': "Dulong's Formula"
        }
        
        if measured_gcv is not None:
            difference = calculated_gcv - measured_gcv
            percent_diff = (difference / measured_gcv) * 100
            
            result['measured_gcv'] = measured_gcv
            result['difference'] = round(difference, 2)
            result['percent_difference'] = round(percent_diff, 2)
            result['accuracy'] = 'Good' if abs(percent_diff) < 5 else 'Fair' if abs(percent_diff) < 10 else 'Poor'
            result['note'] = self._get_comparison_note(percent_diff)
        
        return result
    
    def _get_comparison_note(self, percent_diff: float) -> str:
        """Get note about GCV comparison"""
        if abs(percent_diff) < 2:
            return "Excellent agreement between calculated and measured GCV"
        elif abs(percent_diff) < 5:
            return "Good agreement. Dulong's formula is reliable for this coal"
        elif abs(percent_diff) < 10:
            return "Fair agreement. Some deviation expected due to coal composition"
        else:
            return "Significant deviation. Verify ultimate analysis or consider bomb calorimeter measurement"


# Global agent instance
dulong_agent = DulongGCVAgent()


def calculate_gcv_from_ultimate_analysis(
    carbon: float,
    hydrogen: float,
    oxygen: float,
    sulfur: float,
    nitrogen: Optional[float] = None,
    ash: Optional[float] = None,
    moisture: Optional[float] = None
) -> Dict:
    """
    Calculate GCV using Dulong's formula
    
    Convenience function for API endpoints
    """
    return dulong_agent.calculate_gcv_dulong(
        carbon=carbon,
        hydrogen=hydrogen,
        oxygen=oxygen,
        sulfur=sulfur,
        nitrogen=nitrogen,
        ash=ash,
        moisture=moisture
    )


def validate_ultimate_analysis_sum(
    carbon: float,
    hydrogen: float,
    oxygen: float,
    sulfur: float,
    nitrogen: float,
    ash: float,
    moisture: float
) -> Dict:
    """
    Validate ultimate analysis components
    
    Convenience function for API endpoints
    """
    return dulong_agent.validate_ultimate_analysis(
        carbon=carbon,
        hydrogen=hydrogen,
        oxygen=oxygen,
        sulfur=sulfur,
        nitrogen=nitrogen,
        ash=ash,
        moisture=moisture
    )
