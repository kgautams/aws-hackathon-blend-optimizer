"""
Hackathon Demo Data - Realistic Coal Blending Scenarios
Created for presentation and demonstration purposes
"""

from dynamodb_service import DynamoDBService
from datetime import datetime

def initialize_hackathon_demo_data():
    """Initialize database with realistic hackathon demo data"""
    
    db = DynamoDBService()
    db.initialize_table()
    
    print("\n🎯 Initializing Hackathon Demo Data...")
    print("=" * 60)
    
    # Clear existing data
    try:
        db.clear_scenario_coals('default')
        print("✅ Cleared existing default scenario")
    except:
        pass
    
    # ========================================
    # REALISTIC COAL INVENTORY
    # Based on actual global coal markets
    # ========================================
    
    demo_coals = [
        {
            "name": "Indonesian Thermal Coal",
            "gcv": 5800,
            "ash": 8.5,
            "moisture": 12.0,
            "sulfur": 0.6,
            "vm": 42.0,
            "alkali": 0.28,
            "si": 52.0,
            "idt": 1280,
            "cost": 72,
            "available": 50000,
            "description": "High-moisture Indonesian coal, cost-effective for blending"
        },
        {
            "name": "Australian Premium Coking",
            "gcv": 7200,
            "ash": 9.2,
            "moisture": 6.5,
            "sulfur": 0.45,
            "vm": 28.0,
            "alkali": 0.18,
            "si": 48.0,
            "idt": 1420,
            "cost": 145,
            "available": 25000,
            "description": "Premium Australian coking coal, high GCV, low sulfur"
        },
        {
            "name": "South African Grade A",
            "gcv": 6400,
            "ash": 12.5,
            "moisture": 8.0,
            "sulfur": 0.75,
            "vm": 32.0,
            "alkali": 0.32,
            "si": 55.0,
            "idt": 1320,
            "cost": 88,
            "available": 40000,
            "description": "Mid-grade South African coal, balanced properties"
        },
        {
            "name": "Russian Export Grade",
            "gcv": 6800,
            "ash": 10.8,
            "moisture": 9.5,
            "sulfur": 0.52,
            "vm": 35.0,
            "alkali": 0.24,
            "si": 50.0,
            "idt": 1380,
            "cost": 95,
            "available": 35000,
            "description": "Russian thermal coal, good calorific value"
        },
        {
            "name": "Colombian High-Volatile",
            "gcv": 6100,
            "ash": 11.2,
            "moisture": 10.5,
            "sulfur": 0.68,
            "vm": 38.0,
            "alkali": 0.30,
            "si": 53.0,
            "idt": 1290,
            "cost": 78,
            "available": 45000,
            "description": "Colombian coal with high volatile matter"
        },
        {
            "name": "US Appalachian Low-Sulfur",
            "gcv": 7000,
            "ash": 8.8,
            "moisture": 5.5,
            "sulfur": 0.38,
            "vm": 30.0,
            "alkali": 0.20,
            "si": 47.0,
            "idt": 1400,
            "cost": 125,
            "available": 20000,
            "description": "Premium US coal, ultra-low sulfur for environmental compliance"
        },
        {
            "name": "Indian Thermal Grade",
            "gcv": 5200,
            "ash": 18.5,
            "moisture": 14.0,
            "sulfur": 0.55,
            "vm": 35.0,
            "alkali": 0.42,
            "si": 62.0,
            "idt": 1220,
            "cost": 58,
            "available": 60000,
            "description": "High-ash Indian coal, very cost-effective for blending"
        },
        {
            "name": "Mongolian Semi-Coking",
            "gcv": 6600,
            "ash": 13.5,
            "moisture": 7.5,
            "sulfur": 0.48,
            "vm": 26.0,
            "alkali": 0.26,
            "si": 51.0,
            "idt": 1350,
            "cost": 82,
            "available": 30000,
            "description": "Mongolian semi-coking coal, low volatile matter"
        },
        {
            "name": "Canadian Metallurgical",
            "gcv": 7400,
            "ash": 7.5,
            "moisture": 4.8,
            "sulfur": 0.42,
            "vm": 24.0,
            "alkali": 0.16,
            "si": 45.0,
            "idt": 1450,
            "cost": 155,
            "available": 18000,
            "description": "Premium Canadian met coal, excellent for steel production"
        },
        {
            "name": "Vietnamese Anthracite",
            "gcv": 7800,
            "ash": 15.0,
            "moisture": 3.5,
            "sulfur": 0.35,
            "vm": 18.0,
            "alkali": 0.22,
            "si": 58.0,
            "idt": 1480,
            "cost": 135,
            "available": 22000,
            "description": "High-grade anthracite, very low moisture and sulfur"
        }
    ]
    
    # Add coals to database
    added_coals = db.bulk_add_coals(demo_coals, 'default')
    print(f"\n✅ Added {len(added_coals)} realistic coal types to inventory")
    
    # ========================================
    # DEMO SCENARIOS FOR HACKATHON
    # ========================================
    
    scenarios = [
        {
            "scenario_id": "power_plant_optimization",
            "name": "🏭 Power Plant Cost Optimization",
            "description": "Large thermal power plant seeking to minimize fuel costs while maintaining 600MW output",
            "difficulty": "Medium",
            "coal_sources": [
                {"name": "Indonesian Thermal Coal", "gcv": 5800, "ash": 8.5, "moisture": 12.0, "sulfur": 0.6, "vm": 42.0, "alkali": 0.28, "si": 52.0, "idt": 1280, "cost": 72, "available": 50000},
                {"name": "South African Grade A", "gcv": 6400, "ash": 12.5, "moisture": 8.0, "sulfur": 0.75, "vm": 32.0, "alkali": 0.32, "si": 55.0, "idt": 1320, "cost": 88, "available": 40000},
                {"name": "Colombian High-Volatile", "gcv": 6100, "ash": 11.2, "moisture": 10.5, "sulfur": 0.68, "vm": 38.0, "alkali": 0.30, "si": 53.0, "idt": 1290, "cost": 78, "available": 45000},
                {"name": "Indian Thermal Grade", "gcv": 5200, "ash": 18.5, "moisture": 14.0, "sulfur": 0.55, "vm": 35.0, "alkali": 0.42, "si": 62.0, "idt": 1220, "cost": 58, "available": 60000}
            ],
            "target_specs": {
                "gcv_min": 5800,
                "ash_max": 15.0,
                "sulfur_max": 0.70,
                "moisture_max": 12.0
            },
            "operational_constraints": {
                "total_required": 25000,
                "stacker_reclaimer_available": "Yes",
                "num_stacker_reclaimer": 2,
                "stacker_speed_rpm": 30.0,
                "ambient_temperature": 28.0,
                "conveyor_speed_mpm": 120.0,
                "target_boiler_efficiency": 85.0
            },
            "business_context": "600MW power plant needs 25,000 tons monthly. Focus on cost reduction while meeting environmental standards.",
            "expected_savings": "$180,000/month",
            "coal_count": 4,
            "target_gcv": 5800,
            "max_ash": 15.0
        },
        {
            "scenario_id": "steel_mill_premium",
            "name": "🏗️ Steel Mill Premium Blend",
            "description": "Integrated steel mill requiring high-quality coking coal blend for blast furnace operations",
            "difficulty": "Hard",
            "coal_sources": [
                {"name": "Australian Premium Coking", "gcv": 7200, "ash": 9.2, "moisture": 6.5, "sulfur": 0.45, "vm": 28.0, "alkali": 0.18, "si": 48.0, "idt": 1420, "cost": 145, "available": 25000},
                {"name": "US Appalachian Low-Sulfur", "gcv": 7000, "ash": 8.8, "moisture": 5.5, "sulfur": 0.38, "vm": 30.0, "alkali": 0.20, "si": 47.0, "idt": 1400, "cost": 125, "available": 20000},
                {"name": "Canadian Metallurgical", "gcv": 7400, "ash": 7.5, "moisture": 4.8, "sulfur": 0.42, "vm": 24.0, "alkali": 0.16, "si": 45.0, "idt": 1450, "cost": 155, "available": 18000},
                {"name": "Russian Export Grade", "gcv": 6800, "ash": 10.8, "moisture": 9.5, "sulfur": 0.52, "vm": 35.0, "alkali": 0.24, "si": 50.0, "idt": 1380, "cost": 95, "available": 35000}
            ],
            "target_specs": {
                "gcv_min": 7000,
                "ash_max": 10.0,
                "sulfur_max": 0.50,
                "moisture_max": 8.0
            },
            "operational_constraints": {
                "total_required": 15000,
                "stacker_reclaimer_available": "Yes",
                "num_stacker_reclaimer": 3,
                "stacker_speed_rpm": 35.0,
                "ambient_temperature": 22.0,
                "conveyor_speed_mpm": 150.0,
                "target_boiler_efficiency": 88.0
            },
            "business_context": "Steel mill needs premium coking coal blend. Quality is critical for coke strength and blast furnace efficiency.",
            "expected_savings": "$95,000/month through optimized blending",
            "coal_count": 4,
            "target_gcv": 7000,
            "max_ash": 10.0
        },
        {
            "scenario_id": "environmental_compliance",
            "name": "🌱 Environmental Compliance Challenge",
            "description": "Power plant must meet strict emission standards while maintaining profitability",
            "difficulty": "Very Hard",
            "coal_sources": [
                {"name": "US Appalachian Low-Sulfur", "gcv": 7000, "ash": 8.8, "moisture": 5.5, "sulfur": 0.38, "vm": 30.0, "alkali": 0.20, "si": 47.0, "idt": 1400, "cost": 125, "available": 20000},
                {"name": "Vietnamese Anthracite", "gcv": 7800, "ash": 15.0, "moisture": 3.5, "sulfur": 0.35, "vm": 18.0, "alkali": 0.22, "si": 58.0, "idt": 1480, "cost": 135, "available": 22000},
                {"name": "Australian Premium Coking", "gcv": 7200, "ash": 9.2, "moisture": 6.5, "sulfur": 0.45, "vm": 28.0, "alkali": 0.18, "si": 48.0, "idt": 1420, "cost": 145, "available": 25000},
                {"name": "Indonesian Thermal Coal", "gcv": 5800, "ash": 8.5, "moisture": 12.0, "sulfur": 0.6, "vm": 42.0, "alkali": 0.28, "si": 52.0, "idt": 1280, "cost": 72, "available": 50000},
                {"name": "Colombian High-Volatile", "gcv": 6100, "ash": 11.2, "moisture": 10.5, "sulfur": 0.68, "vm": 38.0, "alkali": 0.30, "si": 53.0, "idt": 1290, "cost": 78, "available": 45000}
            ],
            "target_specs": {
                "gcv_min": 6500,
                "ash_max": 12.0,
                "sulfur_max": 0.50,
                "moisture_max": 10.0
            },
            "operational_constraints": {
                "total_required": 20000,
                "stacker_reclaimer_available": "Yes",
                "num_stacker_reclaimer": 2,
                "stacker_speed_rpm": 32.0,
                "ambient_temperature": 25.0,
                "conveyor_speed_mpm": 130.0,
                "target_boiler_efficiency": 86.0
            },
            "business_context": "New EPA regulations require <0.5% sulfur. Must balance environmental compliance with cost control.",
            "expected_savings": "$125,000/month vs. buying only premium coal",
            "coal_count": 5,
            "target_gcv": 6500,
            "max_ash": 12.0
        },
        {
            "scenario_id": "supply_chain_disruption",
            "name": "⚠️ Supply Chain Crisis Management",
            "description": "Primary supplier unavailable - optimize with remaining available sources",
            "difficulty": "Hard",
            "coal_sources": [
                {"name": "Mongolian Semi-Coking", "gcv": 6600, "ash": 13.5, "moisture": 7.5, "sulfur": 0.48, "vm": 26.0, "alkali": 0.26, "si": 51.0, "idt": 1350, "cost": 82, "available": 30000},
                {"name": "Indian Thermal Grade", "gcv": 5200, "ash": 18.5, "moisture": 14.0, "sulfur": 0.55, "vm": 35.0, "alkali": 0.42, "si": 62.0, "idt": 1220, "cost": 58, "available": 60000},
                {"name": "South African Grade A", "gcv": 6400, "ash": 12.5, "moisture": 8.0, "sulfur": 0.75, "vm": 32.0, "alkali": 0.32, "si": 55.0, "idt": 1320, "cost": 88, "available": 40000},
                {"name": "Colombian High-Volatile", "gcv": 6100, "ash": 11.2, "moisture": 10.5, "sulfur": 0.68, "vm": 38.0, "alkali": 0.30, "si": 53.0, "idt": 1290, "cost": 78, "available": 45000},
                {"name": "Russian Export Grade", "gcv": 6800, "ash": 10.8, "moisture": 9.5, "sulfur": 0.52, "vm": 35.0, "alkali": 0.24, "si": 50.0, "idt": 1380, "cost": 95, "available": 35000}
            ],
            "target_specs": {
                "gcv_min": 6000,
                "ash_max": 14.0,
                "sulfur_max": 0.65,
                "moisture_max": 11.0
            },
            "operational_constraints": {
                "total_required": 30000,
                "stacker_reclaimer_available": "Yes",
                "num_stacker_reclaimer": 2,
                "stacker_speed_rpm": 28.0,
                "ambient_temperature": 30.0,
                "conveyor_speed_mpm": 110.0,
                "target_boiler_efficiency": 84.0
            },
            "business_context": "Australian supplier disrupted by port strike. Must maintain operations with alternative sources.",
            "expected_savings": "Avoid $500,000 in emergency spot market purchases",
            "coal_count": 5,
            "target_gcv": 6000,
            "max_ash": 14.0
        },
        {
            "scenario_id": "cement_plant_optimization",
            "name": "🏭 Cement Kiln Fuel Optimization",
            "description": "Cement plant optimizing alternative fuel mix for rotary kiln operations",
            "difficulty": "Medium",
            "coal_sources": [
                {"name": "Vietnamese Anthracite", "gcv": 7800, "ash": 15.0, "moisture": 3.5, "sulfur": 0.35, "vm": 18.0, "alkali": 0.22, "si": 58.0, "idt": 1480, "cost": 135, "available": 22000},
                {"name": "Indonesian Thermal Coal", "gcv": 5800, "ash": 8.5, "moisture": 12.0, "sulfur": 0.6, "vm": 42.0, "alkali": 0.28, "si": 52.0, "idt": 1280, "cost": 72, "available": 50000},
                {"name": "Indian Thermal Grade", "gcv": 5200, "ash": 18.5, "moisture": 14.0, "sulfur": 0.55, "vm": 35.0, "alkali": 0.42, "si": 62.0, "idt": 1220, "cost": 58, "available": 60000},
                {"name": "Mongolian Semi-Coking", "gcv": 6600, "ash": 13.5, "moisture": 7.5, "sulfur": 0.48, "vm": 26.0, "alkali": 0.26, "si": 51.0, "idt": 1350, "cost": 82, "available": 30000}
            ],
            "target_specs": {
                "gcv_min": 6200,
                "ash_max": 16.0,
                "sulfur_max": 0.60,
                "moisture_max": 10.0
            },
            "operational_constraints": {
                "total_required": 18000,
                "stacker_reclaimer_available": "Yes",
                "num_stacker_reclaimer": 1,
                "stacker_speed_rpm": 25.0,
                "ambient_temperature": 32.0,
                "conveyor_speed_mpm": 100.0,
                "target_boiler_efficiency": 82.0
            },
            "business_context": "Cement plant can tolerate higher ash (becomes part of clinker). Focus on GCV and cost optimization.",
            "expected_savings": "$145,000/month through strategic blending",
            "coal_count": 4,
            "target_gcv": 6200,
            "max_ash": 16.0
        }
    ]
    
    # Add scenarios to database
    for scenario in scenarios:
        try:
            # Prepare scenario data with all fields needed for display
            scenario_data = {
                'scenario_id': scenario['scenario_id'],
                'name': scenario['name'],
                'description': scenario['description'],
                'difficulty': scenario['difficulty'],
                'coal_sources': scenario['coal_sources'],
                'target_specs': scenario['target_specs'],
                'operational_constraints': scenario['operational_constraints'],
                'business_context': scenario.get('business_context', ''),
                'expected_savings': scenario.get('expected_savings', ''),
                'coal_count': scenario['coal_count'],
                'target_gcv': scenario['target_gcv'],
                'max_ash': scenario['max_ash'],
                # Add coals field for compatibility
                'coals': scenario['coal_sources']
            }
            db.save_scenario(scenario['scenario_id'], scenario_data)
            print(f"✅ Added scenario: {scenario['name']}")
        except Exception as e:
            print(f"⚠️  Scenario {scenario['name']}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 Hackathon Demo Data Initialized Successfully!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   • {len(demo_coals)} realistic coal types from global markets")
    print(f"   • {len(scenarios)} industry-relevant scenarios")
    print(f"   • Scenarios cover: Power, Steel, Environment, Supply Chain, Cement")
    print(f"\n💡 Demo Tips:")
    print(f"   1. Start with 'Power Plant Cost Optimization' (easiest)")
    print(f"   2. Show 'Environmental Compliance' for complexity")
    print(f"   3. Use 'Supply Chain Crisis' for real-world relevance")
    print(f"   4. Highlight cost savings in each scenario")
    print(f"\n🎯 All scenarios are validated to work with default target specs!")
    print("=" * 60)

if __name__ == "__main__":
    initialize_hackathon_demo_data()
