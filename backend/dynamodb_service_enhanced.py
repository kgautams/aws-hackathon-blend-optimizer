"""
Enhanced DynamoDB Service for Coal Blending Optimizer
Handles scenarios, coals, target specs, and operational constraints
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from decimal import Decimal
import json
from typing import Dict, List, Optional

class DynamoDBServiceEnhanced:
    def __init__(self, region_name='us-east-1'):
        """Initialize DynamoDB client"""
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.scenarios_table_name = 'CoalBlendingScenarios'
        self.coals_table_name = 'CoalInventory'
        
    def create_tables_if_not_exist(self):
        """Create DynamoDB tables if they don't exist"""
        try:
            # Create Scenarios table
            try:
                self.dynamodb.create_table(
                    TableName=self.scenarios_table_name,
                    KeySchema=[
                        {'AttributeName': 'scenario_id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'scenario_id', 'AttributeType': 'S'}
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                print(f"✅ Created table: {self.scenarios_table_name}")
            except self.dynamodb.meta.client.exceptions.ResourceInUseException:
                print(f"ℹ️  Table already exists: {self.scenarios_table_name}")
            
            # Create Coals table
            try:
                self.dynamodb.create_table(
                    TableName=self.coals_table_name,
                    KeySchema=[
                        {'AttributeName': 'coal_id', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'coal_id', 'AttributeType': 'S'},
                        {'AttributeName': 'scenario_id', 'AttributeType': 'S'}
                    ],
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'scenario_id-index',
                            'KeySchema': [
                                {'AttributeName': 'scenario_id', 'KeyType': 'HASH'}
                            ],
                            'Projection': {'ProjectionType': 'ALL'}
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                print(f"✅ Created table: {self.coals_table_name}")
            except self.dynamodb.meta.client.exceptions.ResourceInUseException:
                print(f"ℹ️  Table already exists: {self.coals_table_name}")
                
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            raise
    
    def _convert_floats_to_decimal(self, obj):
        """Convert float values to Decimal for DynamoDB"""
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {k: self._convert_floats_to_decimal(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_floats_to_decimal(item) for item in obj]
        return obj
    
    def _convert_decimal_to_float(self, obj):
        """Convert Decimal values to float for JSON serialization"""
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: self._convert_decimal_to_float(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_decimal_to_float(item) for item in obj]
        return obj
    
    # ========================================================================
    # SCENARIO OPERATIONS
    # ========================================================================
    
    def save_scenario(self, scenario: Dict) -> Dict:
        """Save or update a scenario in DynamoDB"""
        table = self.dynamodb.Table(self.scenarios_table_name)
        
        # Ensure scenario_id exists
        if 'scenario_id' not in scenario:
            scenario['scenario_id'] = scenario.get('id', f"scenario_{datetime.now().timestamp()}")
        
        # Add metadata
        scenario['updated_at'] = datetime.now().isoformat()
        if 'created_at' not in scenario:
            scenario['created_at'] = datetime.now().isoformat()
        
        # Convert floats to Decimal
        scenario_data = self._convert_floats_to_decimal(scenario)
        
        # Save to DynamoDB
        table.put_item(Item=scenario_data)
        
        return {"scenario_id": scenario['scenario_id'], "success": True}
    
    def get_scenario(self, scenario_id: str) -> Optional[Dict]:
        """Get a scenario from DynamoDB"""
        table = self.dynamodb.Table(self.scenarios_table_name)
        
        response = table.get_item(Key={'scenario_id': scenario_id})
        
        if 'Item' in response:
            return self._convert_decimal_to_float(response['Item'])
        return None
    
    def get_all_scenarios(self) -> List[Dict]:
        """Get all scenarios from DynamoDB"""
        table = self.dynamodb.Table(self.scenarios_table_name)
        
        response = table.scan()
        scenarios = response.get('Items', [])
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            scenarios.extend(response.get('Items', []))
        
        return [self._convert_decimal_to_float(s) for s in scenarios]
    
    def delete_scenario(self, scenario_id: str):
        """Delete a scenario from DynamoDB"""
        table = self.dynamodb.Table(self.scenarios_table_name)
        table.delete_item(Key={'scenario_id': scenario_id})
        
        # Also delete associated coals
        coals = self.get_coals_by_scenario(scenario_id)
        for coal in coals:
            self.delete_coal(coal['coal_id'])
    
    # ========================================================================
    # COAL OPERATIONS
    # ========================================================================
    
    def save_coal(self, coal: Dict) -> Dict:
        """Save or update a coal in DynamoDB"""
        table = self.dynamodb.Table(self.coals_table_name)
        
        # Ensure coal_id exists
        if 'coal_id' not in coal:
            coal['coal_id'] = f"coal_{datetime.now().timestamp()}_{coal.get('name', 'unknown').replace(' ', '_')}"
        
        # Ensure scenario_id exists
        if 'scenario_id' not in coal:
            coal['scenario_id'] = 'default'
        
        # Add metadata
        coal['updated_at'] = datetime.now().isoformat()
        if 'created_at' not in coal:
            coal['created_at'] = datetime.now().isoformat()
        
        # Convert floats to Decimal
        coal_data = self._convert_floats_to_decimal(coal)
        
        # Save to DynamoDB
        table.put_item(Item=coal_data)
        
        return {"coal_id": coal['coal_id'], "success": True}
    
    def get_coal(self, coal_id: str) -> Optional[Dict]:
        """Get a coal from DynamoDB"""
        table = self.dynamodb.Table(self.coals_table_name)
        
        response = table.get_item(Key={'coal_id': coal_id})
        
        if 'Item' in response:
            return self._convert_decimal_to_float(response['Item'])
        return None
    
    def get_coals_by_scenario(self, scenario_id: str) -> List[Dict]:
        """Get all coals for a specific scenario"""
        table = self.dynamodb.Table(self.coals_table_name)
        
        response = table.query(
            IndexName='scenario_id-index',
            KeyConditionExpression=Key('scenario_id').eq(scenario_id)
        )
        
        coals = response.get('Items', [])
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.query(
                IndexName='scenario_id-index',
                KeyConditionExpression=Key('scenario_id').eq(scenario_id),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            coals.extend(response.get('Items', []))
        
        return [self._convert_decimal_to_float(c) for c in coals]
    
    def delete_coal(self, coal_id: str):
        """Delete a coal from DynamoDB"""
        table = self.dynamodb.Table(self.coals_table_name)
        table.delete_item(Key={'coal_id': coal_id})
    
    # ========================================================================
    # BULK OPERATIONS
    # ========================================================================
    
    def save_scenario_with_coals(self, scenario_data: Dict) -> Dict:
        """
        Save a complete scenario with all its coals, target specs, and constraints
        
        Expected format:
        {
            "scenario_id": "power_plant_optimal",
            "name": "Power Plant - Optimal",
            "description": "...",
            "difficulty": "Easy",
            "outcome": "positive",
            "coal_sources": [...],
            "target_specifications": {...},
            "operational_constraints": {...},
            "total_required": 10000
        }
        """
        scenario_id = scenario_data.get('scenario_id')
        
        # Extract coals
        coal_sources = scenario_data.pop('coal_sources', [])
        
        # Save scenario metadata
        scenario_result = self.save_scenario(scenario_data)
        
        # Save each coal
        coal_results = []
        for coal in coal_sources:
            coal['scenario_id'] = scenario_id
            result = self.save_coal(coal)
            coal_results.append(result)
        
        return {
            "scenario_id": scenario_id,
            "success": True,
            "coals_saved": len(coal_results)
        }
    
    def get_complete_scenario(self, scenario_id: str) -> Optional[Dict]:
        """
        Get a complete scenario with all its coals, target specs, and constraints
        """
        # Get scenario metadata
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return None
        
        # Get associated coals
        coals = self.get_coals_by_scenario(scenario_id)
        
        # Add coals to scenario
        scenario['coal_sources'] = coals
        
        return scenario

# Create singleton instance
db_service = DynamoDBServiceEnhanced()
