"""
Test Scenarios for LLM-Powered Coal Blending Optimization
5 coal types with realistic properties designed to produce optimal 2-3 coal blends
"""

# Scenario 1: Cost-Optimized Blend (Budget-Conscious)
# Expected: 2-3 coals, prioritizing Indonesian and Indian coals
SCENARIO_1_COST_OPTIMIZED = {
    "name": "Cost-Optimized Blend",
    "description": "Budget-conscious scenario prioritizing low-cost coals while meeting basic specs",
    "coal_sources": [
        {
            "name": "Indonesian Thermal",
            "ash": 8.5,
            "sulfur": 0.4,
            "moisture": 7.0,
            "gcv": 5800,
            "cost": 75,
            "available": 50000
        },
        {
            "name": "Indian Bituminous",
            "ash": 12.0,
            "sulfur": 0.6,
            "moisture": 8.5,
            "gcv": 5500,
            "cost": 65,
            "available": 60000
        },
        {
            "name": "Australian Premium",
            "ash": 9.0,
            "sulfur": 0.5,
            "moisture": 5.0,
            "gcv": 6800,
            "cost": 135,
            "available": 30000
        },
        {
            "name": "South African Export",
            "ash": 11.5,
            "sulfur": 0.7,
            "moisture": 7.5,
            "gcv": 6100,
            "cost": 95,
            "available": 40000
        },
        {
            "name": "Russian Thermal",
            "ash": 10.0,
            "sulfur": 0.55,
            "moisture": 6.5,
            "gcv": 6000,
            "cost": 85,
            "available": 45000
        }
    ],
    "target_specifications": {
        "gcv_min": 5700,
        "ash_max": 14.0,
        "sulfur_max": 0.9,
        "moisture_max": 9.0
    },
    "total_required": 15000,
    "target_boiler_efficiency": 84.0,
    "expected_blend": "Indonesian (60%) + Indian (40%) or Indonesian (50%) + Russian (30%) + Indian (20%)"
}

# Scenario 2: Quality-Focused Blend (High Performance)
# Expected: 2-3 coals, prioritizing Australian and South African
SCENARIO_2_QUALITY_FOCUSED = {
    "name": "Quality-Focused Blend",
    "description": "High-performance scenario prioritizing quality over cost",
    "coal_sources": [
        {
            "name": "Indonesian Thermal",
            "ash": 8.5,
            "sulfur": 0.4,
            "moisture": 7.0,
            "gcv": 5800,
            "cost": 75,
            "available": 50000
        },
        {
            "name": "Indian Bituminous",
            "ash": 12.0,
            "sulfur": 0.6,
            "moisture": 8.5,
            "gcv": 5500,
            "cost": 65,
            "available": 60000
        },
        {
            "name": "Australian Premium",
            "ash": 9.0,
            "sulfur": 0.5,
            "moisture": 5.0,
            "gcv": 6800,
            "cost": 135,
            "available": 30000
        },
        {
            "name": "South African Export",
            "ash": 11.5,
            "sulfur": 0.7,
            "moisture": 7.5,
            "gcv": 6100,
            "cost": 95,
            "available": 40000
        },
        {
            "name": "Russian Thermal",
            "ash": 10.0,
            "sulfur": 0.55,
            "moisture": 6.5,
            "gcv": 6000,
            "cost": 85,
            "available": 45000
        }
    ],
    "target_specifications": {
        "gcv_min": 6300,
        "ash_max": 10.0,
        "sulfur_max": 0.6,
        "moisture_max": 6.5
    },
    "total_required": 12000,
    "target_boiler_efficiency": 88.0,
    "expected_blend": "Australian (70%) + Indonesian (30%) or Australian (60%) + Russian (40%)"
}

# Scenario 3: Balanced Blend (Optimal Trade-off)
# Expected: 3 coals for balanced cost and quality
SCENARIO_3_BALANCED = {
    "name": "Balanced Blend",
    "description": "Optimal trade-off between cost and quality",
    "coal_sources": [
        {
            "name": "Indonesian Thermal",
            "ash": 8.5,
            "sulfur": 0.4,
            "moisture": 7.0,
            "gcv": 5800,
            "cost": 75,
            "available": 50000
        },
        {
            "name": "Indian Bituminous",
            "ash": 12.0,
            "sulfur": 0.6,
            "moisture": 8.5,
            "gcv": 5500,
            "cost": 65,
            "available": 60000
        },
        {
            "name": "Australian Premium",
            "ash": 9.0,
            "sulfur": 0.5,
            "moisture": 5.0,
            "gcv": 6800,
            "cost": 135,
            "available": 30000
        },
        {
            "name": "South African Export",
            "ash": 11.5,
            "sulfur": 0.7,
            "moisture": 7.5,
            "gcv": 6100,
            "cost": 95,
            "available": 40000
        },
        {
            "name": "Russian Thermal",
            "ash": 10.0,
            "sulfur": 0.55,
            "moisture": 6.5,
            "gcv": 6000,
            "cost": 85,
            "available": 45000
        }
    ],
    "target_specifications": {
        "gcv_min": 6000,
        "ash_max": 11.0,
        "sulfur_max": 0.7,
        "moisture_max": 7.5
    },
    "total_required": 18000,
    "target_boiler_efficiency": 86.0,
    "expected_blend": "Indonesian (40%) + Russian (35%) + South African (25%)"
}

# Scenario 4: Low Sulfur Requirement (Environmental Focus)
# Expected: 2-3 coals with low sulfur content
SCENARIO_4_LOW_SULFUR = {
    "name": "Low Sulfur Blend",
    "description": "Environmentally-focused scenario with strict sulfur limits",
    "coal_sources": [
        {
            "name": "Indonesian Thermal",
            "ash": 8.5,
            "sulfur": 0.4,
            "moisture": 7.0,
            "gcv": 5800,
            "cost": 75,
            "available": 50000
        },
        {
            "name": "Indian Bituminous",
            "ash": 12.0,
            "sulfur": 0.6,
            "moisture": 8.5,
            "gcv": 5500,
            "cost": 65,
            "available": 60000
        },
        {
            "name": "Australian Premium",
            "ash": 9.0,
            "sulfur": 0.5,
            "moisture": 5.0,
            "gcv": 6800,
            "cost": 135,
            "available": 30000
        },
        {
            "name": "South African Export",
            "ash": 11.5,
            "sulfur": 0.7,
            "moisture": 7.5,
            "gcv": 6100,
            "cost": 95,
            "available": 40000
        },
        {
            "name": "Russian Thermal",
            "ash": 10.0,
            "sulfur": 0.55,
            "moisture": 6.5,
            "gcv": 6000,
            "cost": 85,
            "available": 45000
        }
    ],
    "target_specifications": {
        "gcv_min": 5900,
        "ash_max": 12.0,
        "sulfur_max": 0.5,
        "moisture_max": 8.0
    },
    "total_required": 20000,
    "target_boiler_efficiency": 85.0,
    "expected_blend": "Indonesian (65%) + Australian (35%) or Indonesian (50%) + Australian (30%) + Russian (20%)"
}

# Scenario 5: High Volume Requirement (Large Scale)
# Expected: 3 coals to meet large volume with cost efficiency
SCENARIO_5_HIGH_VOLUME = {
    "name": "High Volume Blend",
    "description": "Large-scale operation requiring high volume with cost efficiency",
    "coal_sources": [
        {
            "name": "Indonesian Thermal",
            "ash": 8.5,
            "sulfur": 0.4,
            "moisture": 7.0,
            "gcv": 5800,
            "cost": 75,
            "available": 50000
        },
        {
            "name": "Indian Bituminous",
            "ash": 12.0,
            "sulfur": 0.6,
            "moisture": 8.5,
            "gcv": 5500,
            "cost": 65,
            "available": 60000
        },
        {
            "name": "Australian Premium",
            "ash": 9.0,
            "sulfur": 0.5,
            "moisture": 5.0,
            "gcv": 6800,
            "cost": 135,
            "available": 30000
        },
        {
            "name": "South African Export",
            "ash": 11.5,
            "sulfur": 0.7,
            "moisture": 7.5,
            "gcv": 6100,
            "cost": 95,
            "available": 40000
        },
        {
            "name": "Russian Thermal",
            "ash": 10.0,
            "sulfur": 0.55,
            "moisture": 6.5,
            "gcv": 6000,
            "cost": 85,
            "available": 45000
        }
    ],
    "target_specifications": {
        "gcv_min": 5800,
        "ash_max": 13.0,
        "sulfur_max": 0.8,
        "moisture_max": 8.5
    },
    "total_required": 35000,
    "target_boiler_efficiency": 84.0,
    "expected_blend": "Indonesian (45%) + Indian (30%) + Russian (25%)"
}

# Scenario 6: Premium Quality (Maximum Performance)
# Expected: 2 coals, Australian dominant
SCENARIO_6_PREMIUM = {
    "name": "Premium Quality Blend",
    "description": "Maximum performance scenario for critical operations",
    "coal_sources": [
        {
            "name": "Indonesian Thermal",
            "ash": 8.5,
            "sulfur": 0.4,
            "moisture": 7.0,
            "gcv": 5800,
            "cost": 75,
            "available": 50000
        },
        {
            "name": "Indian Bituminous",
            "ash": 12.0,
            "sulfur": 0.6,
            "moisture": 8.5,
            "gcv": 5500,
            "cost": 65,
            "available": 60000
        },
        {
            "name": "Australian Premium",
            "ash": 9.0,
            "sulfur": 0.5,
            "moisture": 5.0,
            "gcv": 6800,
            "cost": 135,
            "available": 30000
        },
        {
            "name": "South African Export",
            "ash": 11.5,
            "sulfur": 0.7,
            "moisture": 7.5,
            "gcv": 6100,
            "cost": 95,
            "available": 40000
        },
        {
            "name": "Russian Thermal",
            "ash": 10.0,
            "sulfur": 0.55,
            "moisture": 6.5,
            "gcv": 6000,
            "cost": 85,
            "available": 45000
        }
    ],
    "target_specifications": {
        "gcv_min": 6500,
        "ash_max": 9.5,
        "sulfur_max": 0.55,
        "moisture_max": 6.0
    },
    "total_required": 10000,
    "target_boiler_efficiency": 89.0,
    "expected_blend": "Australian (85%) + Indonesian (15%) or Australian (90%) + Russian (10%)"
}

# All scenarios
ALL_SCENARIOS = {
    "scenario_1": SCENARIO_1_COST_OPTIMIZED,
    "scenario_2": SCENARIO_2_QUALITY_FOCUSED,
    "scenario_3": SCENARIO_3_BALANCED,
    "scenario_4": SCENARIO_4_LOW_SULFUR,
    "scenario_5": SCENARIO_5_HIGH_VOLUME,
    "scenario_6": SCENARIO_6_PREMIUM
}

def get_scenario(scenario_id):
    """Get a specific scenario by ID"""
    return ALL_SCENARIOS.get(scenario_id)

def list_scenarios():
    """List all available scenarios"""
    return [
        {
            "id": key,
            "name": scenario["name"],
            "description": scenario["description"],
            "expected_blend": scenario["expected_blend"]
        }
        for key, scenario in ALL_SCENARIOS.items()
    ]

if __name__ == "__main__":
    import json
    
    print("="*80)
    print("LLM TEST SCENARIOS - 5 Coal Types")
    print("="*80)
    
    for scenario_id, scenario in ALL_SCENARIOS.items():
        print(f"\n{scenario_id.upper()}: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Total Required: {scenario['total_required']:,} tons")
        print(f"Expected Blend: {scenario['expected_blend']}")
        print(f"Target GCV: {scenario['target_specifications']['gcv_min']} kcal/kg")
        print(f"Max Ash: {scenario['target_specifications']['ash_max']}%")
        print("-"*80)
    
    # Save scenarios to JSON file
    with open('llm_test_scenarios.json', 'w') as f:
        json.dump(ALL_SCENARIOS, f, indent=2)
    
    print("\n✅ Scenarios saved to llm_test_scenarios.json")
