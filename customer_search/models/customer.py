"""Customer domain and DTO models placeholders for Customer Search."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """Customer entity representation."""

    customer_id: str
    name: str
    email: str


@dataclass
class CustomerSearchResult:
    """DTO representing a single customer search result."""

    customer_id: str
    name: str
    email: str
