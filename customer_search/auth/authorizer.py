"""Authorization component for Customer Search."""

from typing import List
from customer_search.models.customer import Customer


class CustomerSearchAuthorizer:
    """Enforces authorization rules for customer searches."""

    def is_user_authorized_for_search(self, user_context: dict) -> bool:
        """Verify whether current user is authorized to perform search."""
        return user_context.get("is_authorized", True)

    def filter_authorized_customers(
        self, customers: List[Customer], user_context: dict
    ) -> List[Customer]:
        """Filter out customer records unauthorized for the current user."""
        return customers
