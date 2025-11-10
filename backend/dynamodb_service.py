"""
DynamoDB Service for Coal Inventory Management
Handles all database operations for coal inventory and test scenarios
"""

import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from typing import List, Dict, Optional
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class DynamoDBService:
    """Service class for DynamoDB operations"""
    
    def __init__(self, table_name='CoalInventory', region_name='us-east-1'):
        """Initialize DynamoDB service"""
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table_name = table_name
        self.table = None
        
    def initialize_table(self):
        """Create table if it doesn't exist"""
        try:
            self.table = self.dynamodb.Table(self.table_name)
            # Check if table exists
            self.table.load()
            print(f"✅ Table {self.table_name} already exists")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            print(f"📦 Creating table {self.table_name}...")
            self.table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
                    {'AttributeName': 'type', 'KeyType': 'RANGE'}  # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'type', 'AttributeType': 'S'},
                    {'AttributeName': 'scenario_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'ScenarioIndex',
                        'KeySchema': [
                            {'AttributeName': 'scenario_id', 'KeyType': 'HASH'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            # Wait for table to be created
            self.table.wait_until_exists()
            print(f"✅ Table {self.table_name} created successfully")
        
        return self.table
    
    def _convert_floats_to_decimal(self, obj):
        """Convert float values to Decimal for DynamoDB"""
        if isinstance(obj, dict):
            return {k: self._convert_floats_to_decimal(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_floats_to_decimal(item) for item in obj]
        elif isinstance(obj, float):
            return Decimal(str(obj))
        return obj
    
    def _convert_decimal_to_float(self, obj):
        """Convert Decimal values to float for JSON"""
        if isinstance(obj, dict):
            return {k: self._convert_decimal_to_float(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_decimal_to_float(item) for item in obj]
        elif isinstance(obj, Decimal):
            return float(obj)
        return obj
    
    # Coal Inventory Operations
    
    def add_coal(self, coal_data: Dict, scenario_id: str = 'default') -> Dict:
        """Add a coal to inventory"""
        coal_id = f"coal_{coal_data['name'].replace(' ', '_').lower()}"
        
        item = {
            'id': coal_id,
            'type': 'coal',
            'scenario_id': scenario_id,
            'name': coal_data['name'],
            'gcv': coal_data['gcv'],
            'ash': coal_data['ash'],
            'moisture': coal_data['moisture'],
            'sulfur': coal_data['sulfur'],
            'cost': coal_data['cost'],
            'available': coal_data['available'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Convert floats to Decimal
        item = self._convert_floats_to_decimal(item)
        
        self.table.put_item(Item=item)
        return self._convert_decimal_to_float(item)
    
    def get_coal(self, coal_id: str) -> Optional[Dict]:
        """Get a specific coal by ID"""
        response = self.table.get_item(
            Key={'id': coal_id, 'type': 'coal'}
        )
        item = response.get('Item')
        return self._convert_decimal_to_float(item) if item else None
    
    def get_all_coals(self, scenario_id: str = 'default') -> List[Dict]:
        """Get all coals for a scenario"""
        response = self.table.query(
            IndexName='ScenarioIndex',
            KeyConditionExpression=Key('scenario_id').eq(scenario_id),
            FilterExpression=Attr('type').eq('coal')
        )
        items = response.get('Items', [])
        return [self._convert_decimal_to_float(item) for item in items]
    
    def update_coal(self, coal_id: str, coal_data: Dict) -> Dict:
        """Update coal information"""
        update_expr = "SET "
        expr_attr_values = {}
        expr_attr_names = {}
        
        for key, value in coal_data.items():
            if key not in ['id', 'type']:
                update_expr += f"#{key} = :{key}, "
                expr_attr_names[f"#{key}"] = key
                expr_attr_values[f":{key}"] = self._convert_floats_to_decimal(value)
        
        update_expr += "#updated_at = :updated_at"
    
    # Optimization History Operations
    
    def save_optimization(self, workflow_id: str, optimization_data: Dict) -> Dict:
        """
        Save optimization results to database for context retrieval
        
        Args:
            workflow_id: Unique workflow identifier
            optimization_data: Complete optimization results including:
                - input_data: coal sources, targets, constraints
                - results: optimization output, quality, cost, boiler analysis
                - metadata: timestamp, user info, etc.
        """
        item = {
            'id': workflow_id,
            'type': 'optimization',
            'scenario_id': optimization_data.get('scenario_id', 'default'),
            'created_at': datetime.now().isoformat(),
            'status': optimization_data.get('status', 'completed'),
            
            # Input data
            'coal_sources': optimization_data.get('coal_sources', []),
            'target_specs': optimization_data.get('target_specs', {}),
            'operational_constraints': optimization_data.get('operational_constraints', {}),
            
            # Results
            'optimization_results': optimization_data.get('optimization_results', {}),
            'quality_predictions': optimization_data.get('quality_predictions', {}),
            'cost_analysis': optimization_data.get('cost_analysis', {}),
            'boiler_efficiency': optimization_data.get('boiler_efficiency', {}),
            'performance_comparison': optimization_data.get('performance_comparison', {}),
            'knowledge_graph': optimization_data.get('knowledge_graph', {}),
            
            # Metadata
            'workflow_metadata': optimization_data.get('workflow_metadata', {}),
            'agent_messages': optimization_data.get('agent_messages', [])
        }
        
        # Convert floats to Decimal
        item = self._convert_floats_to_decimal(item)
        
        self.table.put_item(Item=item)
        return self._convert_decimal_to_float(item)
    
    def get_optimization(self, workflow_id: str) -> Optional[Dict]:
        """Get optimization results by workflow ID"""
        response = self.table.get_item(
            Key={'id': workflow_id, 'type': 'optimization'}
        )
        item = response.get('Item')
        return self._convert_decimal_to_float(item) if item else None
    
    def get_latest_optimization(self, scenario_id: str = 'default', limit: int = 1) -> Optional[Dict]:
        """Get the most recent optimization for a scenario"""
        response = self.table.query(
            IndexName='ScenarioIndex',
            KeyConditionExpression=Key('scenario_id').eq(scenario_id),
            FilterExpression=Attr('type').eq('optimization'),
            ScanIndexForward=False,  # Sort descending (newest first)
            Limit=limit
        )
        items = response.get('Items', [])
        if items:
            return self._convert_decimal_to_float(items[0])
        return None
    
    def get_optimization_history(self, scenario_id: str = 'default', limit: int = 10) -> List[Dict]:
        """Get optimization history for a scenario"""
        response = self.table.query(
            IndexName='ScenarioIndex',
            KeyConditionExpression=Key('scenario_id').eq(scenario_id),
            FilterExpression=Attr('type').eq('optimization'),
            ScanIndexForward=False,  # Sort descending (newest first)
            Limit=limit
        )
        items = response.get('Items', [])
        return [self._convert_decimal_to_float(item) for item in items]
    
    def delete_optimization(self, workflow_id: str) -> bool:
        """Delete an optimization record"""
        try:
            self.table.delete_item(
                Key={'id': workflow_id, 'type': 'optimization'}
            )
            return True
        except Exception as e:
            print(f"Error deleting optimization: {e}")
            return False
        expr_attr_names["#updated_at"] = "updated_at"
        expr_attr_values[":updated_at"] = datetime.now().isoformat()
        
        response = self.table.update_item(
            Key={'id': coal_id, 'type': 'coal'},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues='ALL_NEW'
        )
        
        return self._convert_decimal_to_float(response.get('Attributes', {}))
    
    def delete_coal(self, coal_id: str) -> bool:
        """Delete a coal from inventory"""
        try:
            self.table.delete_item(
                Key={'id': coal_id, 'type': 'coal'}
            )
            return True
        except Exception as e:
            print(f"Error deleting coal: {str(e)}")
            return False
    
    # Scenario Operations
    
    def save_scenario(self, scenario_id: str, scenario_data: Dict) -> Dict:
        """Save a test scenario"""
        item = {
            'id': f"scenario_{scenario_id}",
            'type': 'scenario',
            'scenario_id': scenario_id,
            'name': scenario_data.get('name', scenario_id),
            'description': scenario_data.get('description', ''),
            'coals': scenario_data.get('coals', []),
            'coal_sources': scenario_data.get('coal_sources', scenario_data.get('coals', [])),
            'target_specs': scenario_data.get('target_specs', {}),
            'operational_constraints': scenario_data.get('operational_constraints', {}),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Add any additional fields from scenario_data
        for key in ['difficulty', 'business_context', 'expected_savings', 'coal_count', 'target_gcv', 'max_ash']:
            if key in scenario_data:
                item[key] = scenario_data[key]
        
        # Convert floats to Decimal
        item = self._convert_floats_to_decimal(item)
        
        self.table.put_item(Item=item)
        return self._convert_decimal_to_float(item)
    
    def get_scenario(self, scenario_id: str) -> Optional[Dict]:
        """Get a specific scenario"""
        response = self.table.get_item(
            Key={'id': f"scenario_{scenario_id}", 'type': 'scenario'}
        )
        item = response.get('Item')
        return self._convert_decimal_to_float(item) if item else None
    
    def get_all_scenarios(self) -> List[Dict]:
        """Get all scenarios"""
        response = self.table.scan(
            FilterExpression=Attr('type').eq('scenario')
        )
        items = response.get('Items', [])
        return [self._convert_decimal_to_float(item) for item in items]
    
    def delete_scenario(self, scenario_id: str) -> bool:
        """Delete a scenario"""
        try:
            self.table.delete_item(
                Key={'id': f"scenario_{scenario_id}", 'type': 'scenario'}
            )
            return True
        except Exception as e:
            print(f"Error deleting scenario: {str(e)}")
            return False
    
    # Bulk Operations
    
    def bulk_add_coals(self, coals: List[Dict], scenario_id: str = 'default') -> List[Dict]:
        """Add multiple coals at once"""
        added_coals = []
        with self.table.batch_writer() as batch:
            for coal_data in coals:
                coal_id = f"coal_{coal_data['name'].replace(' ', '_').lower()}"
                item = {
                    'id': coal_id,
                    'type': 'coal',
                    'scenario_id': scenario_id,
                    'name': coal_data['name'],
                    'gcv': coal_data['gcv'],
                    'ash': coal_data['ash'],
                    'moisture': coal_data['moisture'],
                    'sulfur': coal_data['sulfur'],
                    'cost': coal_data['cost'],
                    'available': coal_data['available'],
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                item = self._convert_floats_to_decimal(item)
                batch.put_item(Item=item)
                added_coals.append(self._convert_decimal_to_float(item))
        
        return added_coals
    
    def clear_scenario_coals(self, scenario_id: str) -> bool:
        """Clear all coals for a scenario"""
        try:
            coals = self.get_all_coals(scenario_id)
            with self.table.batch_writer() as batch:
                for coal in coals:
                    batch.delete_item(
                        Key={'id': coal['id'], 'type': 'coal'}
                    )
            return True
        except Exception as e:
            print(f"Error clearing scenario coals: {str(e)}")
            return False


# Singleton instance
_db_service = None

def get_db_service() -> DynamoDBService:
    """Get or create DynamoDB service instance"""
    global _db_service
    if _db_service is None:
        _db_service = DynamoDBService()
        _db_service.initialize_table()
    return _db_service
