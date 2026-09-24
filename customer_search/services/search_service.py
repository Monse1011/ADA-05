"""Customer Search application service."""

from typing import List, Optional
from customer_search.models.customer import CustomerSearchResult
from customer_search.repositories.customer_repository import ICustomerRepository
from customer_search.validation.validator import SearchInputValidator
from customer_search.auth.authorizer import CustomerSearchAuthorizer


class CustomerSearchService:
    """Application service orchestrating customer search flow."""

    def __init__(
        self,
        repository: ICustomerRepository,
        validator: Optional[SearchInputValidator] = None,
        authorizer: Optional[CustomerSearchAuthorizer] = None,
    ):
        self._repository = repository
        self._validator = validator or SearchInputValidator()
        self._authorizer = authorizer or CustomerSearchAuthorizer()

    def search(self, query: str, user_context: Optional[dict] = None) -> List[CustomerSearchResult]:
        """Perform customer search; full search and relevance logic implemented in T-03."""
        user_ctx = user_context or {"is_authorized": True}
        clean_query = self._validator.sanitize_query(query)
        if not clean_query:
            return []

        raw_customers = self._repository.search_customers(clean_query)
        authorized = self._authorizer.filter_authorized_customers(raw_customers, user_ctx)

        return [
            CustomerSearchResult(
                customer_id=c.customer_id,
                name=c.name,
                email=c.email,
            )
            for c in authorized
        ]
