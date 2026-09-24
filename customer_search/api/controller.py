"""Customer Search API controller handling HTTP-level request and response."""

from typing import Any, Dict, Optional
from customer_search.services.search_service import CustomerSearchService


class CustomerSearchController:
    """Controller implementing GET /api/customers/search?q={query}."""

    def __init__(self, search_service: CustomerSearchService):
        self._search_service = search_service

    def handle_search_request(
        self, query_params: Dict[str, Any], user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle incoming search request and format API response."""
        q = query_params.get("q", "")
        results = self._search_service.search(query=q, user_context=user_context)

        return {
            "results": [
                {
                    "customerId": r.customer_id,
                    "name": r.name,
                    "email": r.email,
                }
                for r in results
            ]
        }
