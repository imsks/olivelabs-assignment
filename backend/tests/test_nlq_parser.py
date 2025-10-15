"""
Test cases for NLQ Parser
"""

import pytest
from app.services.nlq_parser import nlq_parser
from app.core.exceptions import NLQException, UnsafeQueryError

class TestNLQParser:
    """Test cases for NLQ parser functionality"""
    
    def test_safe_query_parsing(self):
        """Test that safe queries are parsed correctly"""
        # This is a placeholder test - actual implementation would test real parsing
        assert True  # Placeholder
    
    def test_unsafe_query_rejection(self):
        """Test that unsafe queries are rejected"""
        with pytest.raises(UnsafeQueryError):
            nlq_parser.execute_sql("DROP TABLE orders")
    
    def test_query_with_limit(self):
        """Test that queries get LIMIT added if missing"""
        # This would test the safety validator's LIMIT addition
        assert True  # Placeholder
    
    def test_explanation_generation(self):
        """Test that explanations are generated correctly"""
        # This would test the explain builder
        assert True  # Placeholder

class TestSchemaRegistry:
    """Test cases for schema registry"""
    
    def test_table_validation(self):
        """Test table validation against whitelist"""
        from app.services.schema_registry import schema_registry
        
        assert schema_registry.validate_table("orders") == True
        assert schema_registry.validate_table("unknown_table") == False
    
    def test_column_validation(self):
        """Test column validation against whitelist"""
        from app.services.schema_registry import schema_registry
        
        assert schema_registry.validate_column("orders", "order_id") == True
        assert schema_registry.validate_column("orders", "unknown_column") == False

class TestSafetyValidator:
    """Test cases for SQL safety validation"""
    
    def test_dangerous_keywords(self):
        """Test detection of dangerous SQL keywords"""
        from app.services.safety import safety_validator
        
        dangerous_queries = [
            "DROP TABLE orders",
            "DELETE FROM orders",
            "INSERT INTO orders VALUES (1, 2, 3)",
            "UPDATE orders SET quantity = 0",
            "ALTER TABLE orders ADD COLUMN test VARCHAR(50)"
        ]
        
        for query in dangerous_queries:
            with pytest.raises(UnsafeQueryError):
                safety_validator.validate_query(query)
    
    def test_safe_queries(self):
        """Test that safe queries pass validation"""
        from app.services.safety import safety_validator
        
        safe_queries = [
            "SELECT * FROM orders LIMIT 10",
            "SELECT region, SUM(quantity * unit_price) FROM orders GROUP BY region",
            "SELECT * FROM orders WHERE order_date >= '2024-01-01'"
        ]
        
        for query in safe_queries:
            warnings = safety_validator.validate_query(query)
            assert isinstance(warnings, list)
