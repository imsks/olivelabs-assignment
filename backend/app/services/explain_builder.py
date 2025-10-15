"""
Explain Builder Service
Extracts SQL components and generates human-readable explanations
"""

import re
from typing import Dict, List, Any
from app.services.schema_registry import schema_registry

class ExplainBuilder:
    """Builds explainability objects from SQL queries"""
    
    def __init__(self):
        self.schema_registry = schema_registry
    
    def build_explanation(self, sql: str) -> Dict[str, Any]:
        """Build explanation object from SQL query"""
        
        sql_upper = sql.upper()
        
        # Extract components
        filters = self._extract_filters(sql)
        group_by = self._extract_group_by(sql)
        aggregates = self._extract_aggregates(sql)
        source_tables = self._extract_source_tables(sql)
        
        return {
            "filters": filters,
            "groupBy": group_by,
            "aggregates": aggregates,
            "sourceTables": source_tables
        }
    
    def _extract_filters(self, sql: str) -> List[str]:
        """Extract WHERE clause conditions"""
        filters = []
        
        # Find WHERE clause
        where_match = re.search(r'WHERE\s+(.*?)(?:\s+GROUP\s+BY|\s+ORDER\s+BY|\s+LIMIT|$)', sql, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1).strip()
            
            # Split by AND/OR and clean up
            conditions = re.split(r'\s+(?:AND|OR)\s+', where_clause, flags=re.IGNORECASE)
            
            for condition in conditions:
                condition = condition.strip()
                if condition:
                    # Clean up the condition for human readability
                    human_readable = self._make_condition_human_readable(condition)
                    filters.append(human_readable)
        
        return filters
    
    def _extract_group_by(self, sql: str) -> List[str]:
        """Extract GROUP BY columns"""
        group_by = []
        
        group_by_match = re.search(r'GROUP\s+BY\s+(.*?)(?:\s+ORDER\s+BY|\s+LIMIT|$)', sql, re.IGNORECASE | re.DOTALL)
        if group_by_match:
            group_by_clause = group_by_match.group(1).strip()
            
            # Split by comma and clean up
            columns = [col.strip() for col in group_by_clause.split(',')]
            
            for col in columns:
                if col:
                    # Remove table prefixes for readability
                    clean_col = col.split('.')[-1] if '.' in col else col
                    group_by.append(clean_col)
        
        return group_by
    
    def _extract_aggregates(self, sql: str) -> List[str]:
        """Extract aggregate functions"""
        aggregates = []
        
        # Find SELECT clause
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
        if select_match:
            select_clause = select_match.group(1)
            
            # Find aggregate functions
            agg_patterns = [
                r'SUM\s*\(\s*([^)]+)\s*\)',
                r'COUNT\s*\(\s*([^)]+)\s*\)',
                r'AVG\s*\(\s*([^)]+)\s*\)',
                r'MAX\s*\(\s*([^)]+)\s*\)',
                r'MIN\s*\(\s*([^)]+)\s*\)'
            ]
            
            for pattern in agg_patterns:
                matches = re.findall(pattern, select_clause, re.IGNORECASE)
                for match in matches:
                    # Determine function type
                    if 'SUM' in pattern:
                        aggregates.append(f"sum({match.strip()})")
                    elif 'COUNT' in pattern:
                        aggregates.append(f"count({match.strip()})")
                    elif 'AVG' in pattern:
                        aggregates.append(f"avg({match.strip()})")
                    elif 'MAX' in pattern:
                        aggregates.append(f"max({match.strip()})")
                    elif 'MIN' in pattern:
                        aggregates.append(f"min({match.strip()})")
        
        return aggregates
    
    def _extract_source_tables(self, sql: str) -> List[str]:
        """Extract source tables from FROM and JOIN clauses"""
        tables = []
        
        # Extract FROM clause
        from_match = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
        if from_match:
            table_name = from_match.group(1).lower()
            if self.schema_registry.validate_table(table_name):
                tables.append(table_name)
        
        # Extract JOIN clauses
        join_matches = re.findall(r'JOIN\s+(\w+)', sql, re.IGNORECASE)
        for table_name in join_matches:
            table_name = table_name.lower()
            if self.schema_registry.validate_table(table_name):
                tables.append(table_name)
        
        return list(set(tables))  # Remove duplicates
    
    def _make_condition_human_readable(self, condition: str) -> str:
        """Convert SQL condition to human-readable format"""
        
        # Handle date ranges
        if 'BETWEEN' in condition.upper():
            return condition.replace('BETWEEN', 'between').replace('AND', 'and')
        
        # Handle IN clauses
        if ' IN ' in condition.upper():
            return condition.replace(' IN ', ' in ')
        
        # Handle comparison operators
        condition = condition.replace('>=', 'greater than or equal to')
        condition = condition.replace('<=', 'less than or equal to')
        condition = condition.replace('>', 'greater than')
        condition = condition.replace('<', 'less than')
        condition = condition.replace('=', 'equals')
        
        # Handle LIKE patterns
        if 'LIKE' in condition.upper():
            condition = condition.replace('LIKE', 'contains')
        
        return condition.strip()

# Global explain builder instance
explain_builder = ExplainBuilder()
