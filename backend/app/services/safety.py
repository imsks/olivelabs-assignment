"""
SQL Safety Validator
Validates SQL queries for security and safety
"""

import re
from typing import List, Set
from app.core.exceptions import UnsafeQueryError
from app.services.schema_registry import schema_registry

class SQLSafetyValidator:
    """Validates SQL queries for safety and security"""
    
    def __init__(self):
        self.dangerous_keywords = {
            'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 'TRUNCATE',
            'EXEC', 'EXECUTE', 'UNION', 'UNION ALL', '--', '/*', '*/', ';',
            'xp_', 'sp_', 'fn_', 'xp_cmdshell', 'sp_executesql'
        }
        
        self.max_limit = 10000
        self.whitelist = schema_registry.get_whitelist()
    
    def validate_query(self, sql: str) -> List[str]:
        """Validate SQL query and return warnings"""
        warnings = []
        
        # Check for dangerous keywords
        sql_upper = sql.upper()
        for keyword in self.dangerous_keywords:
            if keyword in sql_upper:
                raise UnsafeQueryError(f"Dangerous keyword detected: {keyword}")
        
        # Ensure it's a SELECT statement
        if not sql_upper.strip().startswith('SELECT'):
            raise UnsafeQueryError("Only SELECT statements are allowed")
        
        # Check for LIMIT clause
        if 'LIMIT' not in sql_upper:
            warnings.append("Query missing LIMIT clause - adding default LIMIT 1000")
        
        # Validate table references
        table_warnings = self._validate_table_references(sql)
        warnings.extend(table_warnings)
        
        # Validate column references
        column_warnings = self._validate_column_references(sql)
        warnings.extend(column_warnings)
        
        return warnings
    
    def _validate_table_references(self, sql: str) -> List[str]:
        """Validate table references against whitelist"""
        warnings = []
        
        # Extract table names from FROM and JOIN clauses
        from_match = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
        if from_match:
            table_name = from_match.group(1).lower()
            if not schema_registry.validate_table(table_name):
                raise UnsafeQueryError(f"Unknown table: {table_name}")
        
        # Check JOIN clauses
        join_matches = re.findall(r'JOIN\s+(\w+)', sql, re.IGNORECASE)
        for table_name in join_matches:
            table_name = table_name.lower()
            if not schema_registry.validate_table(table_name):
                raise UnsafeQueryError(f"Unknown table: {table_name}")
        
        return warnings
    
    def _validate_column_references(self, sql: str) -> List[str]:
        """Validate column references against whitelist"""
        warnings = []
        
        # Extract column names from SELECT clause
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
        if select_match:
            select_clause = select_match.group(1)
            columns = self._extract_columns_from_select(select_clause)
            
            for col in columns:
                if '.' in col:
                    table_name, column_name = col.split('.', 1)
                    table_name = table_name.lower()
                    column_name = column_name.lower()
                    
                    if not schema_registry.validate_column(table_name, column_name):
                        raise UnsafeQueryError(f"Unknown column: {table_name}.{column_name}")
                else:
                    # Column without table prefix - check against all tables
                    found = False
                    for table_name in self.whitelist:
                        if schema_registry.validate_column(table_name, col.lower()):
                            found = True
                            break
                    
                    if not found:
                        raise UnsafeQueryError(f"Unknown column: {col}")
        
        return warnings
    
    def _extract_columns_from_select(self, select_clause: str) -> List[str]:
        """Extract column names from SELECT clause"""
        columns = []
        
        # Split by comma and clean up
        parts = select_clause.split(',')
        for part in parts:
            part = part.strip()
            
            # Handle AS clauses
            if ' AS ' in part.upper():
                part = part.split(' AS ')[0].strip()
            
            # Handle functions like SUM(), COUNT(), etc.
            if '(' in part and ')' in part:
                # Extract column from function
                func_match = re.search(r'\(([^)]+)\)', part)
                if func_match:
                    inner_col = func_match.group(1).strip()
                    if '.' in inner_col:
                        columns.append(inner_col)
                    else:
                        columns.append(inner_col)
            else:
                columns.append(part)
        
        return columns
    
    def add_limit_if_missing(self, sql: str) -> str:
        """Add LIMIT clause if missing"""
        sql_upper = sql.upper()
        
        if 'LIMIT' not in sql_upper:
            # Add LIMIT at the end
            sql = sql.rstrip(';') + f' LIMIT {self.max_limit}'
        
        return sql

# Global safety validator instance
safety_validator = SQLSafetyValidator()
