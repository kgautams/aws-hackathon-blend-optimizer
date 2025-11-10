"""
Complex Realistic Coal Blending Scenarios
Designed to test optimizer with real-world challenges
"""

COMPLEX_SCENARIOS = {
    "multi_source_complex": {
        "name": "Multi-Source Complex Blend - 8 Coals",
        "description": "Large-scale power plant with 8 diverse coal sources, complex quality requirements, and tight operational constraints",
        "difficulty": "Very Hard",
        "coal_sources": [
            {
                "name": "Indonesian Kalimantan Sub-Bit",
                "gcv": 5420,
                "ash": 9.8,
                "sulfur": 0.42,
                "moisture": 12.5,
                "volatile_matter": 42.5,
                "fixed_carbon": 35.2,
                "cost": 68.50,
                "available": 25000,
                "origin": "Indonesia",
                "notes": "High moisture, good ignition"
            },
            {
                "name": "Australian Newcastle Premium",
                "gcv": 6720,
                "ash": 10.2,
                "sulfur": 0.68,
                "moisture": 4.8,
                "volatile_matter": 28.5,
                "fixed_carbon": 56.5,
                "cost": 128.00,
                "available": 18000,
                "origin": "Australia",
                "notes": "Premium quality, low moisture"
            },
            {
                "name": "South African Witbank",
                "gcv": 5980,
                "ash": 14.5,
                "sulfur": 0.88,
                "moisture": 8.2,
                "volatile_matter": 24.8,
                "fixed_carbon": 52.5,
                "cost": 89.00,
                "available": 22000,
                "origin": "South Africa",
                "notes": "High ash, good value"
            },
            {
                "name": "Colombian Cerrejon Export",
                "gcv": 6180,
                "ash": 9.2,
                "sulfur": 0.58,
                "moisture": 6.5,
                "volatile_matter": 35.2,
                "fixed_carbon": 49.1,
                "cost": 102.00,
                "available": 20000,
                "origin": "Colombia",
                "notes": "Balanced quality"
            },
            {
                "name": "Russian Kuzbass Thermal",
                "gcv": 5850,
                "ash": 12.8,
                "sulfur": 0.52,
                "moisture": 9.5,
                "volatile_matter": 32.5,
                "fixed_carbon": 45.2,
                "cost": 82.00,
                "available": 28000,
                "origin": "Russia",
                "notes": "Low sulfur, moderate quality"
            },
            {
                "name": "US Appalachian High-Vol",
                "gcv": 6420,
                "ash": 11.5,
                "sulfur": 0.78,
                "moisture": 7.2,
                "volatile_matter": 38.5,
                "fixed_carbon": 42.8,
                "cost": 115.00,
                "available": 15000,
                "origin": "USA",
                "notes": "High volatile, good combustion"
            },
            {
                "name": "Indian Jharia Washed",
                "gcv": 5650,
                "ash": 16.2,
                "sulfur": 0.65,
                "moisture": 8.8,
                "volatile_matter": 28.5,
                "fixed_carbon": 46.5,
                "cost": 72.00,
                "available": 30000,
                "origin": "India",
                "notes": "High ash, economical"
            },
            {
                "name": "Mongolian Tavan Tolgoi",
                "gcv": 5520,
                "ash": 13.5,
                "sulfur": 0.48,
                "moisture": 10.2,
                "volatile_matter": 31.8,
                "fixed_carbon": 44.5,
                "cost": 75.00,
                "available": 26000,
                "origin": "Mongolia",
                "notes": "Low sulfur, moderate ash"
            }
        ],
        "target_specs": {
            "gcv_min": 5900,
            "ash_max": 13.5,
            "sulfur_max": 0.75,
            "moisture_max": 9.0,
            "volatile_matter_min": 28.0,
            "fixed_carbon_min": 45.0
        },
        "operational_constraints": {
            "total_required": 50000,
            "min_blend_percentage": 8.0,
            "max_blend_percentage": 35.0,
            "stacker_reclaimer_available": True,
            "num_stacker_reclaimer": 3,
            "stacker_speed_rpm": 28.0,
            "ambient_temperature": 32.0,
            "conveyor_speed_mpm": 140.0,
            "max_moisture_handling": 12.0,
            "blending_time_hours": 48,
            "storage_capacity_tons": 80000,
            "simultaneous_sources_max": 6
        },
        "additional_constraints": {
            "max_high_ash_coals": 2,
            "min_premium_coals": 1,
            "regional_diversity_required": True,
            "sulfur_weighted_avg_target": 0.65
        }
    },
    
    "seasonal_monsoon": {
        "name": "Seasonal Monsoon Challenge",
        "description": "Monsoon season with high moisture coals, limited storage, and urgent delivery requirements",
        "difficulty": "Hard",
        "coal_sources": [
            {
                "name": "Indonesian Monsoon Stock",
                "gcv": 5280,
                "ash": 10.5,
                "sulfur": 0.38,
                "moisture": 15.8,
                "volatile_matter": 41.2,
                "fixed_carbon": 32.5,
                "cost": 62.00,
                "available": 35000,
                "origin": "Indonesia",
                "notes": "High moisture due to monsoon"
            },
            {
                "name": "Australian Dry Stock Reserve",
                "gcv": 6580,
                "ash": 9.8,
                "sulfur": 0.62,
                "moisture": 5.2,
                "volatile_matter": 29.5,
                "fixed_carbon": 55.5,
                "cost": 135.00,
                "available": 12000,
                "origin": "Australia",
                "notes": "Limited availability, premium"
            },
            {
                "name": "South African Covered Storage",
                "gcv": 6050,
                "ash": 13.2,
                "sulfur": 0.82,
                "moisture": 7.5,
                "volatile_matter": 26.8,
                "fixed_carbon": 52.5,
                "cost": 92.00,
                "available": 18000,
                "origin": "South Africa",
                "notes": "Protected from rain"
            },
            {
                "name": "Vietnamese Wet Season",
                "gcv": 5380,
                "ash": 11.8,
                "sulfur": 0.45,
                "moisture": 14.2,
                "volatile_matter": 38.5,
                "fixed_carbon": 35.5,
                "cost": 65.00,
                "available": 28000,
                "origin": "Vietnam",
                "notes": "Monsoon affected"
            },
            {
                "name": "Russian Siberian Dry",
                "gcv": 5920,
                "ash": 12.5,
                "sulfur": 0.55,
                "moisture": 8.8,
                "volatile_matter": 31.2,
                "fixed_carbon": 47.5,
                "cost": 88.00,
                "available": 22000,
                "origin": "Russia",
                "notes": "Stable quality"
            }
        ],
        "target_specs": {
            "gcv_min": 5700,
            "ash_max": 14.0,
            "sulfur_max": 0.85,
            "moisture_max": 11.0
        },
        "operational_constraints": {
            "total_required": 25000,
            "min_blend_percentage": 12.0,
            "max_blend_percentage": 45.0,
            "stacker_reclaimer_available": True,
            "num_stacker_reclaimer": 2,
            "stacker_speed_rpm": 25.0,
            "ambient_temperature": 28.0,
            "conveyor_speed_mpm": 110.0,
            "max_moisture_handling": 15.0,
            "blending_time_hours": 36,
            "storage_capacity_tons": 40000,
            "humidity_percent": 85.0,
            "rain_protection_required": True
        }
    },
    
    "ultra_low_emissions": {
        "name": "Ultra-Low Emissions Compliance",
        "description": "Strict environmental regulations requiring ultra-low sulfur and optimized combustion",
        "difficulty": "Hard",
        "coal_sources": [
            {
                "name": "Wyoming Powder River Basin",
                "gcv": 5680,
                "ash": 8.5,
                "sulfur": 0.22,
                "moisture": 8.5,
                "volatile_matter": 44.5,
                "fixed_carbon": 38.5,
                "cost": 92.00,
                "available": 40000,
                "origin": "USA",
                "notes": "Ultra-low sulfur"
            },
            {
                "name": "Colombian Ultra-Clean",
                "gcv": 6280,
                "ash": 9.2,
                "sulfur": 0.28,
                "moisture": 5.8,
                "volatile_matter": 36.5,
                "fixed_carbon": 48.5,
                "cost": 112.00,
                "available": 25000,
                "origin": "Colombia",
                "notes": "Premium low-sulfur"
            },
            {
                "name": "Indonesian Low-S Blend",
                "gcv": 5850,
                "ash": 10.8,
                "sulfur": 0.32,
                "moisture": 7.2,
                "volatile_matter": 40.2,
                "fixed_carbon": 41.8,
                "cost": 95.00,
                "available": 30000,
                "origin": "Indonesia",
                "notes": "Specially washed"
            },
            {
                "name": "Australian Low-Sulfur Premium",
                "gcv": 6520,
                "ash": 10.5,
                "sulfur": 0.35,
                "moisture": 5.5,
                "volatile_matter": 30.5,
                "fixed_carbon": 53.5,
                "cost": 125.00,
                "available": 20000,
                "origin": "Australia",
                "notes": "Export quality"
            },
            {
                "name": "Canadian Clean Coal",
                "gcv": 6180,
                "ash": 11.2,
                "sulfur": 0.38,
                "moisture": 6.8,
                "volatile_matter": 33.5,
                "fixed_carbon": 48.5,
                "cost": 108.00,
                "available": 22000,
                "origin": "Canada",
                "notes": "Environmental grade"
            }
        ],
        "target_specs": {
            "gcv_min": 6000,
            "ash_max": 11.5,
            "sulfur_max": 0.40,
            "moisture_max": 7.5,
            "volatile_matter_min": 32.0
        },
        "operational_constraints": {
            "total_required": 30000,
            "min_blend_percentage": 15.0,
            "max_blend_percentage": 40.0,
            "stacker_reclaimer_available": True,
            "num_stacker_reclaimer": 2,
            "stacker_speed_rpm": 30.0,
            "ambient_temperature": 22.0,
            "conveyor_speed_mpm": 130.0,
            "blending_time_hours": 40,
            "storage_capacity_tons": 50000,
            "emissions_monitoring_required": True,
            "so2_limit_mg_nm3": 200,
            "nox_limit_mg_nm3": 300
        }
    },
    
    "supply_chain_crisis": {
        "name": "Supply Chain Crisis - Limited Availability",
        "description": "Emergency situation with limited coal availability, spot market purchases, and urgent requirements",
        "difficulty": "Extreme",
        "coal_sources": [
            {
                "name": "Spot Market Premium A",
                "gcv": 6380,
                "ash": 11.2,
                "sulfur": 0.72,
                "moisture": 6.5,
                "volatile_matter": 32.5,
                "fixed_carbon": 49.8,
                "cost": 145.00,
                "available": 5500,
                "origin": "Various",
                "notes": "Spot market, limited"
            },
            {
                "name": "Emergency Reserve Stock",
                "gcv": 5720,
                "ash": 14.8,
                "sulfur": 0.88,
                "moisture": 9.2,
                "volatile_matter": 28.5,
                "fixed_carbon": 47.5,
                "cost": 98.00,
                "available": 6200,
                "origin": "Domestic",
                "notes": "Emergency stock"
            },
            {
                "name": "Local Supplier Batch 1",
                "gcv": 5580,
                "ash": 15.5,
                "sulfur": 0.92,
                "moisture": 10.5,
                "volatile_matter": 26.8,
                "fixed_carbon": 47.2,
                "cost": 88.00,
                "available": 7800,
                "origin": "Regional",
                "notes": "Available immediately"
            },
            {
                "name": "Spot Market Standard B",
                "gcv": 6120,
                "ash": 12.8,
                "sulfur": 0.78,
                "moisture": 7.8,
                "volatile_matter": 30.5,
                "fixed_carbon": 48.9,
                "cost": 118.00,
                "available": 5200,
                "origin": "Various",
                "notes": "Spot market"
            },
            {
                "name": "Alternative Source C",
                "gcv": 5850,
                "ash": 13.5,
                "sulfur": 0.82,
                "moisture": 8.5,
                "volatile_matter": 29.8,
                "fixed_carbon": 48.2,
                "cost": 105.00,
                "available": 6500,
                "origin": "Alternative",
                "notes": "New supplier"
            },
            {
                "name": "Backup Supplier D",
                "gcv": 5920,
                "ash": 14.2,
                "sulfur": 0.85,
                "moisture": 9.0,
                "volatile_matter": 28.2,
                "fixed_carbon": 48.6,
                "cost": 102.00,
                "available": 5800,
                "origin": "Backup",
                "notes": "Limited time offer"
            }
        ],
        "target_specs": {
            "gcv_min": 5850,
            "ash_max": 14.5,
            "sulfur_max": 0.95,
            "moisture_max": 10.0
        },
        "operational_constraints": {
            "total_required": 20000,
            "min_blend_percentage": 12.0,
            "max_blend_percentage": 35.0,
            "stacker_reclaimer_available": True,
            "num_stacker_reclaimer": 1,
            "stacker_speed_rpm": 22.0,
            "ambient_temperature": 26.0,
            "conveyor_speed_mpm": 95.0,
            "blending_time_hours": 24,
            "storage_capacity_tons": 25000,
            "urgent_delivery_required": True,
            "quality_testing_expedited": True
        }
    },
    
    "high_efficiency_plant": {
        "name": "High-Efficiency Supercritical Plant",
        "description": "Modern supercritical power plant requiring premium coal blend for maximum efficiency",
        "difficulty": "Hard",
        "coal_sources": [
            {
                "name": "Australian Premium Black",
                "gcv": 6850,
                "ash": 8.2,
                "sulfur": 0.48,
                "moisture": 4.2,
                "volatile_matter": 27.5,
                "fixed_carbon": 60.1,
                "cost": 142.00,
                "available": 20000,
                "origin": "Australia",
                "notes": "Top grade export"
            },
            {
                "name": "US Appalachian Premium",
                "gcv": 6720,
                "ash": 9.5,
                "sulfur": 0.65,
                "moisture": 5.0,
                "volatile_matter": 29.5,
                "fixed_carbon": 56.0,
                "cost": 135.00,
                "available": 18000,
                "origin": "USA",
                "notes": "High-grade bituminous"
            },
            {
                "name": "South African Premium",
                "gcv": 6580,
                "ash": 10.2,
                "sulfur": 0.72,
                "moisture": 5.8,
                "volatile_matter": 28.5,
                "fixed_carbon": 55.5,
                "cost": 128.00,
                "available": 22000,
                "origin": "South Africa",
                "notes": "Export quality"
            },
            {
                "name": "Colombian High-Grade",
                "gcv": 6420,
                "ash": 9.8,
                "sulfur": 0.58,
                "moisture": 5.5,
                "volatile_matter": 32.5,
                "fixed_carbon": 52.2,
                "cost": 122.00,
                "available": 25000,
                "origin": "Colombia",
                "notes": "Premium export"
            },
            {
                "name": "Canadian Export Grade",
                "gcv": 6380,
                "ash": 10.5,
                "sulfur": 0.62,
                "moisture": 6.2,
                "volatile_matter": 31.5,
                "fixed_carbon": 51.8,
                "cost": 118.00,
                "available": 20000,
                "origin": "Canada",
                "notes": "High quality"
            }
        ],
        "target_specs": {
            "gcv_min": 6500,
            "ash_max": 10.5,
            "sulfur_max": 0.70,
            "moisture_max": 6.0,
            "volatile_matter_min": 28.0,
            "fixed_carbon_min": 52.0
        },
        "operational_constraints": {
            "total_required": 35000,
            "min_blend_percentage": 15.0,
            "max_blend_percentage": 35.0,
            "stacker_reclaimer_available": True,
            "num_stacker_reclaimer": 3,
            "stacker_speed_rpm": 32.0,
            "ambient_temperature": 24.0,
            "conveyor_speed_mpm": 150.0,
            "blending_time_hours": 48,
            "storage_capacity_tons": 60000,
            "quality_control_strict": True,
            "boiler_efficiency_target": 45.0,
            "heat_rate_target_kcal_kwh": 1950
        }
    }
}


def get_complex_scenario(scenario_id: str) -> dict:
    """Get a complex scenario by ID"""
    return COMPLEX_SCENARIOS.get(scenario_id)


def list_complex_scenarios() -> list:
    """List all complex scenarios"""
    return [
        {
            "id": scenario_id,
            "name": scenario["name"],
            "description": scenario["description"],
            "difficulty": scenario["difficulty"],
            "num_coals": len(scenario["coal_sources"]),
            "total_required": scenario["operational_constraints"]["total_required"]
        }
        for scenario_id, scenario in COMPLEX_SCENARIOS.items()
    ]
