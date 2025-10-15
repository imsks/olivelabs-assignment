"""
Query Executor Service
Handles SQL query execution with proper error handling and result formatting
"""

import redis
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import SessionLocal
from app.core.config import settings
from app.core.exceptions import QueryExecutionError
import json
import hashlib

class QueryExecutor:
    """Executes SQL queries with caching and error handling"""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.cache_ttl = 3600  # 1 hour
    
    def execute_query(self, sql: str, result_format: str = "table") -> Dict[str, Any]:
        """Execute SQL query and return formatted results"""
        
        # Check cache first
        cache_key = self._get_cache_key(sql)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Execute query
        try:
            db = SessionLocal()
            result = db.execute(text(sql))
            
            # Get column names
            columns = list(result.keys())
            
            # Get rows
            rows = [list(row) for row in result.fetchall()]
            
            db.close()
            
            # Format results
            formatted_result = {
                "columns": columns,
                "rows": rows,
                "inferred_chart": self._infer_chart_type(columns, rows)
            }
            
            # Cache result
            self._cache_result(cache_key, formatted_result)
            
            return formatted_result
            
        except Exception as e:
            raise QueryExecutionError(f"Query execution failed: {str(e)}")
    
    def _get_cache_key(self, sql: str) -> str:
        """Generate cache key for SQL query"""
        sql_hash = hashlib.md5(sql.encode()).hexdigest()
        return f"query:{sql_hash}"
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get result from cache"""
        try:
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception:
            pass
        return None
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]) -> None:
        """Cache query result"""
        try:
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(result)
            )
        except Exception:
            pass  # Cache failures shouldn't break the app
    
    def _infer_chart_type(self, columns: List[str], rows: List[List[Any]]) -> Optional[str]:
        """Infer chart type from query results"""
        if not rows or len(rows) < 2:
            return None
        
        # Check if we have numeric data for charting
        numeric_columns = []
        for i, col in enumerate(columns):
            if self._is_numeric_column(rows, i):
                numeric_columns.append(i)
        
        if len(numeric_columns) == 0:
            return None
        
        # Determine chart type based on data characteristics
        if len(rows) <= 10 and len(numeric_columns) == 1:
            return "pie"
        elif len(rows) > 10:
            return "line"
        else:
            return "bar"
    
    def _is_numeric_column(self, rows: List[List[Any]], column_index: int) -> bool:
        """Check if column contains numeric data"""
        try:
            for row in rows[:5]:  # Check first 5 rows
                if row[column_index] is not None:
                    float(row[column_index])
            return True
        except (ValueError, TypeError):
            return False

# Global query executor instance
query_executor = QueryExecutor()
