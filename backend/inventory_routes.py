"""
API Routes for Coal Inventory Management
Handles all inventory-related endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dynamodb_service import get_db_service

router = APIRouter(prefix="/api/inventory", tags=["inventory"])

# Pydantic models
class CoalInventoryItem(BaseModel):
    name: str
    gcv: float
    ash: float
    moisture: float
    sulfur: float
    cost: float
    available: float

class CoalInventoryUpdate(BaseModel):
    gcv: Optional[float] = None
    ash: Optional[float] = None
    moisture: Optional[float] = None
    sulfur: Optional[float] = None
    cost: Optional[float] = None
    available: Optional[float] = None

# Inventory Endpoints

@router.get("")
async def get_inventory(scenario_id: str = "default"):
    """Get all coals in inventory for a scenario"""
    try:
        db = get_db_service()
        coals = db.get_all_coals(scenario_id)
        return {
            "success": True,
            "scenario_id": scenario_id,
            "count": len(coals),
            "coals": coals
        }
    except Exception as e:
        # Return empty inventory if database not initialized
        print(f"Database error: {str(e)}")
        return {
            "success": True,
            "scenario_id": scenario_id,
            "count": 0,
            "coals": [],
            "message": "Database not initialized. Run init_database.py to set up."
        }

@router.post("/coal")
async def add_coal(coal: CoalInventoryItem, scenario_id: str = "default"):
    """Add a new coal to inventory"""
    try:
        db = get_db_service()
        coal_data = coal.model_dump()
        added_coal = db.add_coal(coal_data, scenario_id)
        return {
            "success": True,
            "message": f"Coal '{coal.name}' added successfully",
            "coal": added_coal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coal/{coal_id}")
async def get_coal(coal_id: str):
    """Get a specific coal by ID"""
    try:
        db = get_db_service()
        coal = db.get_coal(coal_id)
        if not coal:
            raise HTTPException(status_code=404, detail="Coal not found")
        return {
            "success": True,
            "coal": coal
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/coal/{coal_id}")
async def update_coal(coal_id: str, coal_update: CoalInventoryUpdate):
    """Update coal information"""
    try:
        db = get_db_service()
        # Only include non-None values
        update_data = {k: v for k, v in coal_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        updated_coal = db.update_coal(coal_id, update_data)
        return {
            "success": True,
            "message": f"Coal updated successfully",
            "coal": updated_coal
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/coal/{coal_id}")
async def delete_coal(coal_id: str):
    """Delete a coal from inventory"""
    try:
        db = get_db_service()
        success = db.delete_coal(coal_id)
        if not success:
            raise HTTPException(status_code=404, detail="Coal not found or could not be deleted")
        return {
            "success": True,
            "message": "Coal deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk")
async def bulk_add_coals(coals: List[CoalInventoryItem], scenario_id: str = "default"):
    """Add multiple coals at once"""
    try:
        db = get_db_service()
        coal_data_list = [coal.model_dump() for coal in coals]
        added_coals = db.bulk_add_coals(coal_data_list, scenario_id)
        return {
            "success": True,
            "message": f"Added {len(added_coals)} coals successfully",
            "coals": added_coals
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/scenario/{scenario_id}")
async def clear_scenario(scenario_id: str):
    """Clear all coals for a scenario"""
    try:
        db = get_db_service()
        success = db.clear_scenario_coals(scenario_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to clear scenario")
        return {
            "success": True,
            "message": f"Cleared all coals for scenario: {scenario_id}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scenario Endpoints

@router.get("/scenarios")
async def get_scenarios():
    """Get all available scenarios"""
    try:
        db = get_db_service()
        scenarios = db.get_all_scenarios()
        return {
            "success": True,
            "count": len(scenarios),
            "scenarios": scenarios
        }
    except Exception as e:
        # Return empty scenarios if database not initialized
        print(f"Database error: {str(e)}")
        return {
            "success": True,
            "count": 0,
            "scenarios": [],
            "message": "Database not initialized. Run init_database.py to set up."
        }

@router.get("/scenario/{scenario_id}")
async def get_scenario(scenario_id: str):
    """Get a specific scenario with its coals"""
    try:
        db = get_db_service()
        scenario = db.get_scenario(scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        # Get coals for this scenario
        coals = db.get_all_coals(scenario_id)
        scenario['coals'] = coals
        
        return {
            "success": True,
            "scenario": scenario
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
