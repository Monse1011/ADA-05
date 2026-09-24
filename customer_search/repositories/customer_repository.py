"""Customer repository abstraction and implementation."""

from abc import ABC, abstractmethod
from typing import List
from customer_search.models.customer import Customer


class ICustomerRepository(ABC):
    """Interface for customer data access."""

    @abstractmethod
    def search_customers(self, query: str) -> List[Customer]:
        """Search customers by query matching name or email."""
        raise NotImplementedError


class InMemoryCustomerRepository(ICustomerRepository):
    """In-memory customer repository implementation for data access."""

    def __init__(self, customers: List[Customer] = None):
        self._customers: List[Customer] = customers or []

    def search_customers(self, query: str) -> List[Customer]:
        """Baseline stub to be expanded in T-03."""
        return list(self._customers)
