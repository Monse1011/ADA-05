"""Input validation component for customer search queries."""


class SearchInputValidator:
    """Validates and sanitizes customer search inputs."""

    def sanitize_query(self, query: str) -> str:
        """Strip leading and trailing whitespace; full validation rules in T-04."""
        if query is None:
            return ""
        return query.strip()
