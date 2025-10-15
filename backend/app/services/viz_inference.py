"""
Visualization Inference Engine
Analyzes query results to suggest appropriate chart types
"""

from typing import List, Dict, Any, Optional
import re

class ChartInferenceEngine:
    """Infers chart types from query results"""
    
    def __init__(self):
        self.chart_types = ["bar", "line", "pie", "scatter"]
    
    def infer_chart_type(self, columns: List[str], rows: List[List[Any]], sql: str) -> Optional[str]:
        """Infer the best chart type for the given data"""
        
        if not rows or len(rows) < 2:
            return None
        
        # Analyze SQL to understand query intent
        sql_analysis = self._analyze_sql(sql)
        
        # Analyze data structure
        data_analysis = self._analyze_data_structure(columns, rows)
        
        # Combine analyses to determine chart type
        chart_type = self._determine_chart_type(sql_analysis, data_analysis)
        
        return chart_type
    
    def _analyze_sql(self, sql: str) -> Dict[str, Any]:
        """Analyze SQL query to understand intent"""
        sql_upper = sql.upper()
        
        analysis = {
            "has_group_by": "GROUP BY" in sql_upper,
            "has_aggregates": any(func in sql_upper for func in ["SUM(", "COUNT(", "AVG(", "MAX(", "MIN("]),
            "has_time_series": any(time_col in sql_upper for time_col in ["DATE", "MONTH", "YEAR", "QUARTER"]),
            "has_limit": "LIMIT" in sql_upper,
            "row_count_estimate": self._estimate_row_count(sql_upper)
        }
        
        return analysis
    
    def _analyze_data_structure(self, columns: List[str], rows: List[List[Any]]) -> Dict[str, Any]:
        """Analyze the structure of the data"""
        
        numeric_columns = []
        categorical_columns = []
        date_columns = []
        
        for i, col in enumerate(columns):
            if self._is_numeric_column(rows, i):
                numeric_columns.append(i)
            elif self._is_date_column(rows, i):
                date_columns.append(i)
            else:
                categorical_columns.append(i)
        
        analysis = {
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "date_columns": date_columns,
            "row_count": len(rows),
            "column_count": len(columns),
            "has_time_series": len(date_columns) > 0,
            "has_categories": len(categorical_columns) > 0,
            "has_metrics": len(numeric_columns) > 0
        }
        
        return analysis
    
    def _determine_chart_type(self, sql_analysis: Dict[str, Any], data_analysis: Dict[str, Any]) -> Optional[str]:
        """Determine the best chart type based on analysis"""
        
        # Time series data -> Line chart
        if sql_analysis["has_time_series"] or data_analysis["has_time_series"]:
            return "line"
        
        # Categorical data with metrics -> Bar chart
        if data_analysis["has_categories"] and data_analysis["has_metrics"]:
            if data_analysis["row_count"] <= 10:
                return "pie"
            else:
                return "bar"
        
        # Large datasets -> Line chart
        if data_analysis["row_count"] > 20:
            return "line"
        
        # Small datasets with categories -> Pie chart
        if data_analysis["row_count"] <= 5 and data_analysis["has_categories"]:
            return "pie"
        
        # Default to bar chart
        if data_analysis["has_metrics"]:
            return "bar"
        
        return None
    
    def _is_numeric_column(self, rows: List[List[Any]], column_index: int) -> bool:
        """Check if column contains numeric data"""
        try:
            for row in rows[:5]:  # Check first 5 rows
                if row[column_index] is not None:
                    float(row[column_index])
            return True
        except (ValueError, TypeError):
            return False
    
    def _is_date_column(self, rows: List[List[Any]], column_index: int) -> bool:
        """Check if column contains date data"""
        try:
            for row in rows[:3]:  # Check first 3 rows
                if row[column_index] is not None:
                    str(row[column_index])
                    # Simple date pattern check
                    if re.match(r'\d{4}-\d{2}-\d{2}', str(row[column_index])):
                        return True
            return False
        except (ValueError, TypeError):
            return False
    
    def _estimate_row_count(self, sql_upper: str) -> int:
        """Estimate row count from SQL"""
        limit_match = re.search(r'LIMIT\s+(\d+)', sql_upper)
        if limit_match:
            return int(limit_match.group(1))
        
        # Default estimate based on query type
        if "GROUP BY" in sql_upper:
            return 10  # Grouped queries typically return fewer rows
        else:
            return 100  # Default estimate

# Global chart inference engine instance
chart_inference_engine = ChartInferenceEngine()
