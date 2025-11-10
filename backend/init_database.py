"""
Initialize DynamoDB with sample coal inventory and test scenarios
Run this script once to set up the database with default data
"""

from dynamodb_service import get_db_service
from complex_scenarios import COMPLEX_SCENARIOS

def initialize_database():
    """Initialize database with sample data"""
    print("=" * 60)
    print("🚀 Initializing DynamoDB with Sample Data")
    print("=" * 60)
    
    db = get_db_service()
    
    # Sample default coal inventory
    default_coals = [
        {
            "name": "Indonesian Thermal",
            "gcv": 5500,
            "ash": 12.0,
            "moisture": 15.0,
            "sulfur": 0.6,
            "cost": 65.0,
            "available": 50000
        },
        {
            "name": "Australian Premium",
            "gcv": 6200,
            "ash": 10.0,
            "moisture": 8.0,
            "sulfur": 0.5,
            "cost": 95.0,
            "available": 30000
        },
        {
            "name": "South African Grade A",
            "gcv": 5800,
            "ash": 14.0,
            "moisture": 10.0,
            "sulfur": 0.7,
            "cost": 75.0,
            "available": 40000
        },
        {
            "name": "Russian Export",
            "gcv": 5600,
            "ash": 16.0,
            "moisture": 12.0,
            "sulfur": 0.8,
            "cost": 70.0,
            "available": 35000
        },
        {
            "name": "Colombian High GCV",
            "gcv": 6000,
            "ash": 11.0,
            "moisture": 9.0,
            "sulfur": 0.6,
            "cost": 85.0,
            "available": 25000
        }
    ]
    
    print("\n📦 Adding default coal inventory...")
    added_coals = db.bulk_add_coals(default_coals, scenario_id='default')
    print(f"✅ Added {len(added_coals)} coals to default inventory")
    
    # Get test scenarios from complex_scenarios.py
    print("\n📋 Loading test scenarios...")
    try:
        scenarios = COMPLEX_SCENARIOS
        
        for scenario_id, scenario_data in scenarios.items():
            print(f"\n  Processing scenario: {scenario_id}")
            
            # Save scenario metadata
            db.save_scenario(scenario_id, {
                'name': scenario_data.get('name', scenario_id),
                'description': scenario_data.get('description', ''),
                'coals': scenario_data.get('coal_sources', []),
                'target_specs': scenario_data.get('target_specifications', {}),
                'operational_constraints': scenario_data.get('operational_constraints', {})
            })
            
            # Add coals for this scenario
            coals = scenario_data.get('coal_sources', [])
            if coals:
                db.bulk_add_coals(coals, scenario_id=scenario_id)
                print(f"  ✅ Added {len(coals)} coals for scenario: {scenario_id}")
        
        print(f"\n✅ Loaded {len(scenarios)} test scenarios")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not load test scenarios: {str(e)}")
        print("   Continuing with default inventory only...")
    
    print("\n" + "=" * 60)
    print("✅ Database Initialization Complete!")
    print("=" * 60)
    print("\nDatabase Contents:")
    print(f"  - Default Inventory: {len(default_coals)} coals")
    print(f"  - Test Scenarios: Available")
    print("\nYou can now:")
    print("  1. View inventory via API: GET /api/inventory")
    print("  2. Add new coals via API: POST /api/inventory/coal")
    print("  3. Load scenarios via API: GET /api/scenarios")
    print("=" * 60)

if __name__ == "__main__":
    initialize_database()
