"""Repositories package for Customer Search."""

from customer_search.repositories.customer_repository import (
    ICustomerRepository,
    InMemoryCustomerRepository,
)

__all__ = ["ICustomerRepository", "InMemoryCustomerRepository"]
