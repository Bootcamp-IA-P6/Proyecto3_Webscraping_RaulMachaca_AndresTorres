"""Pydantic models for GAME.es scraped data validation."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class RelatedProduct(BaseModel):
    """Model for related products data."""
    name: str = Field(..., description="Product name")
    price: str = Field(..., description="Product price string")


class GameProduct(BaseModel):
    """Main model for scraped GAME.es product."""
    title: str = Field(..., description="Main product title")
    price: str = Field(..., description="Main product price")
    ratings_count: str = Field(..., description="Number of ratings")
    related_products: List[RelatedProduct] = Field(default_factory=list)
    scraped_at: datetime = Field(default_factory=datetime.now)
