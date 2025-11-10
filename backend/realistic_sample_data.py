"""
Realistic Sample Data for Hackathon Demo
Returns data in the same format as the API, no database needed
"""

REALISTIC_SAMPLE_DATA = {
    "coal_sources": [
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
            "available": 50000
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
            "available": 40000
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
            "available": 45000
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
            "available": 60000
        },
        {
            "name": "Australian Export Blend",
            "gcv": 6800,
            "ash": 10.0,
            "moisture": 9.0,
            "sulfur": 0.52,
            "vm": 34.0,
            "alkali": 0.26,
            "si": 51.0,
            "idt": 1350,
            "cost": 95,
            "available": 35000
        }
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
        "target_boiler_efficiency": 85.0,
        "min_blend_components": 3,
        "max_single_coal_percentage": 50.0
    },
    "total_required": 25000
}

TEST_SCENARIOS = {
    "power_plant_optimization": {
        "id": "power_plant_optimization",
        "name": "🏭 Power Plant Cost Optimization",
        "description": "600MW power plant optimizing fuel costs while maintaining quality",
        "difficulty": "Medium",
        "coal_sources": [
            {"name": "Indonesian Thermal Coal", "gcv": 5800, "ash": 8.5, "moisture": 12.0, "sulfur": 0.6, "vm": 42.0, "alkali": 0.28, "si": 52.0, "idt": 1280, "cost": 72, "available": 50000},
            {"name": "South African Grade A", "gcv": 6400, "ash": 12.5, "moisture": 8.0, "sulfur": 0.75, "vm": 32.0, "alkali": 0.32, "si": 55.0, "idt": 1320, "cost": 88, "available": 40000},
            {"name": "Colombian High-Volatile", "gcv": 6100, "ash": 11.2, "moisture": 10.5, "sulfur": 0.68, "vm": 38.0, "alkali": 0.30, "si": 53.0, "idt": 1290, "cost": 78, "available": 45000},
            {"name": "Indian Thermal Grade", "gcv": 5200, "ash": 18.5, "moisture": 14.0, "sulfur": 0.55, "vm": 35.0, "alkali": 0.42, "si": 62.0, "idt": 1220, "cost": 58, "available": 60000},
            {"name": "Australian Export Blend", "gcv": 6800, "ash": 10.0, "moisture": 9.0, "sulfur": 0.52, "vm": 34.0, "alkali": 0.26, "si": 51.0, "idt": 1350, "cost": 95, "available": 35000}
        ],
        "target_specifications": {
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
            "target_boiler_efficiency": 85.0,
            "min_blend_components": 3,
            "max_single_coal_percentage": 50.0,
            "blending_time_hours": 8.0,
            "storage_capacity_tons": 100000
        },
        "total_required": 25000,
        "expected_cost": "$1.85M",
        "num_coals": 5
    },
    "steel_mill_premium": {
        "id": "steel_mill_premium",
        "name": "🏗️ Steel Mill Premium Blend",
        "description": "High-quality coking coal blend for blast furnace operations",
        "difficulty": "Hard",
        "coal_sources": [
            {"name": "Australian Premium Coking", "gcv": 7200, "ash": 9.2, "moisture": 6.5, "sulfur": 0.45, "vm": 28.0, "alkali": 0.18, "si": 48.0, "idt": 1420, "cost": 145, "available": 25000},
            {"name": "US Appalachian Low-Sulfur", "gcv": 7000, "ash": 8.8, "moisture": 5.5, "sulfur": 0.38, "vm": 30.0, "alkali": 0.20, "si": 47.0, "idt": 1400, "cost": 125, "available": 20000},
            {"name": "Canadian Metallurgical", "gcv": 7400, "ash": 7.5, "moisture": 4.8, "sulfur": 0.42, "vm": 24.0, "alkali": 0.16, "si": 45.0, "idt": 1450, "cost": 155, "available": 18000},
            {"name": "Russian Export Grade", "gcv": 6800, "ash": 10.8, "moisture": 9.5, "sulfur": 0.52, "vm": 35.0, "alkali": 0.24, "si": 50.0, "idt": 1380, "cost": 95, "available": 35000},
            {"name": "Mongolian Semi-Soft", "gcv": 6900, "ash": 9.5, "moisture": 7.2, "sulfur": 0.48, "vm": 32.0, "alkali": 0.22, "si": 49.0, "idt": 1390, "cost": 110, "available": 28000}
        ],
        "target_specifications": {
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
            "target_boiler_efficiency": 88.0,
            "min_blend_components": 3,
            "max_single_coal_percentage": 45.0,
            "blending_time_hours": 6.0,
            "storage_capacity_tons": 80000
        },
        "total_required": 15000,
        "expected_cost": "$1.75M",
        "num_coals": 5
    },
    "environmental_compliance": {
        "id": "environmental_compliance",
        "name": "🌱 Environmental Compliance",
        "description": "Strict EPA sulfur and emissions limits for clean energy",
        "difficulty": "Very Hard",
        "coal_sources": [
            {"name": "US Appalachian Low-Sulfur", "gcv": 7000, "ash": 8.8, "moisture": 5.5, "sulfur": 0.38, "vm": 30.0, "alkali": 0.20, "si": 47.0, "idt": 1400, "cost": 125, "available": 20000},
            {"name": "Vietnamese Anthracite", "gcv": 7800, "ash": 15.0, "moisture": 3.5, "sulfur": 0.35, "vm": 18.0, "alkali": 0.22, "si": 58.0, "idt": 1480, "cost": 135, "available": 22000},
            {"name": "Australian Premium Coking", "gcv": 7200, "ash": 9.2, "moisture": 6.5, "sulfur": 0.45, "vm": 28.0, "alkali": 0.18, "si": 48.0, "idt": 1420, "cost": 145, "available": 25000},
            {"name": "Indonesian Thermal Coal", "gcv": 5800, "ash": 8.5, "moisture": 12.0, "sulfur": 0.6, "vm": 42.0, "alkali": 0.28, "si": 52.0, "idt": 1280, "cost": 72, "available": 50000},
            {"name": "Wyoming Sub-Bituminous", "gcv": 5400, "ash": 6.2, "moisture": 18.0, "sulfur": 0.32, "vm": 44.0, "alkali": 0.25, "si": 50.0, "idt": 1250, "cost": 65, "available": 55000}
        ],
        "target_specifications": {
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
            "target_boiler_efficiency": 86.0,
            "min_blend_components": 3,
            "max_single_coal_percentage": 40.0,
            "blending_time_hours": 10.0,
            "storage_capacity_tons": 90000
        },
        "total_required": 20000,
        "expected_cost": "$2.15M",
        "num_coals": 5
    },
    "balanced_multi_objective": {
        "id": "balanced_multi_objective",
        "name": "⚖️ Balanced Multi-Objective",
        "description": "Optimize cost, quality, and environmental impact simultaneously",
        "difficulty": "Hard",
        "coal_sources": [
            {"name": "Indonesian Thermal Coal", "gcv": 5800, "ash": 8.5, "moisture": 12.0, "sulfur": 0.6, "vm": 42.0, "alkali": 0.28, "si": 52.0, "idt": 1280, "cost": 72, "available": 50000},
            {"name": "South African Grade A", "gcv": 6400, "ash": 12.5, "moisture": 8.0, "sulfur": 0.75, "vm": 32.0, "alkali": 0.32, "si": 55.0, "idt": 1320, "cost": 88, "available": 40000},
            {"name": "Australian Export Blend", "gcv": 6800, "ash": 10.0, "moisture": 9.0, "sulfur": 0.52, "vm": 34.0, "alkali": 0.26, "si": 51.0, "idt": 1350, "cost": 95, "available": 35000},
            {"name": "Colombian High-Volatile", "gcv": 6100, "ash": 11.2, "moisture": 10.5, "sulfur": 0.68, "vm": 38.0, "alkali": 0.30, "si": 53.0, "idt": 1290, "cost": 78, "available": 45000},
            {"name": "US Appalachian Low-Sulfur", "gcv": 7000, "ash": 8.8, "moisture": 5.5, "sulfur": 0.38, "vm": 30.0, "alkali": 0.20, "si": 47.0, "idt": 1400, "cost": 125, "available": 20000}
        ],
        "target_specifications": {
            "gcv_min": 6200,
            "ash_max": 13.0,
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
            "target_boiler_efficiency": 84.0,
            "min_blend_components": 3,
            "max_single_coal_percentage": 45.0,
            "blending_time_hours": 12.0,
            "storage_capacity_tons": 120000
        },
        "total_required": 30000,
        "expected_cost": "$2.45M",
        "num_coals": 5
    }
}

def get_sample_data():
    """Get default sample data"""
    return REALISTIC_SAMPLE_DATA

def get_test_scenario(scenario_id):
    """Get a specific test scenario"""
    return TEST_SCENARIOS.get(scenario_id, REALISTIC_SAMPLE_DATA)

def get_all_test_scenarios():
    """Get all available test scenarios"""
    return {
        "scenarios": [
            {
                "id": scenario_id,
                "name": data["name"],
                "description": data["description"],
                "difficulty": data["difficulty"],
                "num_coals": data["num_coals"],
                "expected_cost": data.get("expected_cost", "N/A"),
                "total_required": data["total_required"]
            }
            for scenario_id, data in TEST_SCENARIOS.items()
        ]
    }
