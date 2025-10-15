"""
Schema Registry System
Manages table/column metadata, validation, and LLM context serialization
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import json

class ColumnMetadata(BaseModel):
    name: str
    type: str
    description: str
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[str] = None

class TableMetadata(BaseModel):
    name: str
    description: str
    columns: List[ColumnMetadata]
    relationships: List[str] = []

class SchemaRegistry:
    """Registry for database schema metadata"""
    
    def __init__(self):
        self.tables: Dict[str, TableMetadata] = {}
        self._load_default_schema()
    
    def _load_default_schema(self):
        """Load default schema configuration"""
        # Orders table
        self.tables["orders"] = TableMetadata(
            name="orders",
            description="Customer orders with product details and pricing",
            columns=[
                ColumnMetadata(name="order_id", type="int", description="Unique order identifier", primary_key=True),
                ColumnMetadata(name="customer_id", type="int", description="Customer who placed the order", foreign_key="customers.customer_id"),
                ColumnMetadata(name="product_id", type="int", description="Product ordered", foreign_key="products.product_id"),
                ColumnMetadata(name="order_date", type="date", description="Date when order was placed"),
                ColumnMetadata(name="quantity", type="int", description="Number of items ordered"),
                ColumnMetadata(name="unit_price", type="float", description="Price per unit"),
                ColumnMetadata(name="region", type="string", description="Geographic region"),
                ColumnMetadata(name="revenue", type="float", description="Calculated: quantity * unit_price", nullable=False)
            ],
            relationships=["customers", "products"]
        )
        
        # Customers table
        self.tables["customers"] = TableMetadata(
            name="customers",
            description="Customer information and segmentation",
            columns=[
                ColumnMetadata(name="customer_id", type="int", description="Unique customer identifier", primary_key=True),
                ColumnMetadata(name="name", type="string", description="Customer company name"),
                ColumnMetadata(name="segment", type="string", description="Customer segment (Enterprise/SMB)"),
                ColumnMetadata(name="country", type="string", description="Customer country")
            ]
        )
        
        # Products table
        self.tables["products"] = TableMetadata(
            name="products",
            description="Product catalog with categories and lines",
            columns=[
                ColumnMetadata(name="product_id", type="int", description="Unique product identifier", primary_key=True),
                ColumnMetadata(name="product_line", type="string", description="Product line (Software/Hardware)"),
                ColumnMetadata(name="category", type="string", description="Product category")
            ]
        )
    
    def get_table(self, table_name: str) -> Optional[TableMetadata]:
        """Get table metadata by name"""
        return self.tables.get(table_name)
    
    def get_all_tables(self) -> Dict[str, TableMetadata]:
        """Get all table metadata"""
        return self.tables
    
    def validate_table(self, table_name: str) -> bool:
        """Validate if table exists in registry"""
        return table_name in self.tables
    
    def validate_column(self, table_name: str, column_name: str) -> bool:
        """Validate if column exists in table"""
        table = self.get_table(table_name)
        if not table:
            return False
        return any(col.name == column_name for col in table.columns)
    
    def get_whitelist(self) -> Dict[str, List[str]]:
        """Get whitelist of allowed tables and columns"""
        whitelist = {}
        for table_name, table in self.tables.items():
            whitelist[table_name] = [col.name for col in table.columns]
        return whitelist
    
    def serialize_for_llm(self) -> str:
        """Serialize schema for LLM context injection"""
        schema_info = {
            "tables": {}
        }
        
        for table_name, table in self.tables.items():
            schema_info["tables"][table_name] = {
                "description": table.description,
                "columns": {
                    col.name: {
                        "type": col.type,
                        "description": col.description,
                        "nullable": col.nullable,
                        "primary_key": col.primary_key
                    }
                    for col in table.columns
                },
                "relationships": table.relationships
            }
        
        return json.dumps(schema_info, indent=2)
    
    def get_human_readable_schema(self) -> str:
        """Get human-readable schema description"""
        description = "Database Schema:\n\n"
        
        for table_name, table in self.tables.items():
            description += f"Table: {table_name}\n"
            description += f"Description: {table.description}\n"
            description += "Columns:\n"
            
            for col in table.columns:
                description += f"  - {col.name} ({col.type}): {col.description}\n"
                if col.primary_key:
                    description += "    [Primary Key]\n"
                if col.foreign_key:
                    description += f"    [Foreign Key to {col.foreign_key}]\n"
            
            if table.relationships:
                description += f"Relationships: {', '.join(table.relationships)}\n"
            
            description += "\n"
        
        return description

# Global schema registry instance
schema_registry = SchemaRegistry()
