from supabase import create_client, Client
from app.config import settings
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# ============================================
# SUPABASE CLIENT
# ============================================

# Initialize Supabase client with service key for backend operations
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY  # Use service key for backend (bypasses RLS)
)


# ============================================
# DATABASE HELPER FUNCTIONS
# ============================================

async def execute_rpc(function_name: str, params: Optional[Dict] = None) -> Any:
    """
    Execute a Supabase RPC (Remote Procedure Call) function
    
    Args:
        function_name: Name of the PostgreSQL function
        params: Optional parameters dictionary
        
    Returns:
        Function result
        
    Raises:
        Exception: If RPC call fails
    """
    try:
        result = supabase.rpc(function_name, params or {}).execute()
        return result.data
    except Exception as e:
        logger.error(f"RPC call to {function_name} failed: {str(e)}")
        raise


async def get_lead_full(lead_id: str) -> Dict[str, Any]:
    """
    Get complete lead data including products, activities, assignments
    
    Args:
        lead_id: UUID of the lead
        
    Returns:
        Complete lead data as dictionary
    """
    return await execute_rpc("get_lead_full", {"lead_uuid": lead_id})


async def get_dashboard_stats() -> Dict[str, Any]:
    """
    Get dashboard statistics
    
    Returns:
        Dashboard metrics dictionary with:
        - total_leads
        - new_leads_today
        - pending_follow_ups
        - pending_approvals
        - sla_violations
        - avg_response_time_minutes
        - conversion_rate
    """
    return await execute_rpc("get_dashboard_stats")


async def get_pending_follow_ups() -> List[Dict[str, Any]]:
    """
    Get all pending follow-ups that are due
    
    Returns:
        List of pending follow-ups with lead details
    """
    return await execute_rpc("get_pending_follow_ups")


# ============================================
# CRUD HELPERS
# ============================================

async def insert_record(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a record into a table
    
    Args:
        table: Table name
        data: Data dict to insert
        
    Returns:
        Inserted record
        
    Raises:
        Exception: If insert fails
    """
    try:
        result = supabase.table(table).insert(data).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        logger.error(f"Insert into {table} failed: {str(e)}")
        raise


async def update_record(
    table: str, 
    record_id: str, 
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a record in a table
    
    Args:
        table: Table name
        record_id: UUID of record to update
        data: Data dict to update
        
    Returns:
        Updated record
        
    Raises:
        Exception: If update fails
    """
    try:
        result = supabase.table(table).update(data).eq("id", record_id).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        logger.error(f"Update {table} record {record_id} failed: {str(e)}")
        raise


async def get_record(table: str, record_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a single record by ID
    
    Args:
        table: Table name
        record_id: UUID of record
        
    Returns:
        Record dict or None
    """
    try:
        result = supabase.table(table).select("*").eq("id", record_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Get {table} record {record_id} failed: {str(e)}")
        return None


async def query_records(
    table: str, 
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Query records from a table with filters
    
    Args:
        table: Table name
        filters: Dictionary of column: value filters
        order_by: Column to order by (e.g., "created_at" or "created_at.desc")
        limit: Max number of records
        
    Returns:
        List of records
    """
    try:
        query = supabase.table(table).select("*")
        
        # Apply filters
        if filters:
            for column, value in filters.items():
                query = query.eq(column, value)
        
        # Apply ordering
        if order_by:
            # Check if descending order
            if order_by.endswith(".desc"):
                col = order_by.replace(".desc", "")
                query = query.order(col, desc=True)
            else:
                query = query.order(order_by)
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        result = query.execute()
        return result.data or []
    except Exception as e:
        logger.error(f"Query {table} failed: {str(e)}")
        return []


async def delete_record(table: str, record_id: str) -> bool:
    """
    Delete a record from a table
    
    Args:
        table: Table name
        record_id: UUID of record to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        supabase.table(table).delete().eq("id", record_id).execute()
        return True
    except Exception as e:
        logger.error(f"Delete from {table} record {record_id} failed: {str(e)}")
        return False


# ============================================
# CONVENIENCE FUNCTIONS
# ============================================

async def get_leads_with_products() -> List[Dict[str, Any]]:
    """
    Get all leads with their associated products
    
    Returns:
        List of leads with products nested
    """
    try:
        result = supabase.table("leads").select("*, lead_products(*)").execute()
        return result.data or []
    except Exception as e:
        logger.error(f"Get leads with products failed: {str(e)}")
        return []


async def get_lead_activities(lead_id: str) -> List[Dict[str, Any]]:
    """
    Get all activities for a specific lead
    
    Args:
        lead_id: UUID of the lead
        
    Returns:
        List of activities ordered by created_at descending
    """
    return await query_records(
        "lead_activity",
        filters={"lead_id": lead_id},
        order_by="created_at.desc"
    )


async def get_pending_approvals() -> List[Dict[str, Any]]:
    """
    Get all pending approval activities
    
    Returns:
        List of pending approval activities
    """
    return await query_records(
        "lead_activity",
        filters={"type": "approval", "status": "pending"},
        order_by="created_at.desc"
    )
