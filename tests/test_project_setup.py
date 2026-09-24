"""Tests for verifying T-01: Project setup and architectural layer connectivity."""

import pytest
from customer_search.models.customer import Customer, CustomerSearchResult
from customer_search.repositories.customer_repository import (
    ICustomerRepository,
    InMemoryCustomerRepository,
)
from customer_search.validation.validator import SearchInputValidator
from customer_search.auth.authorizer import CustomerSearchAuthorizer
from customer_search.services.search_service import CustomerSearchService
from customer_search.api.controller import CustomerSearchController


def test_models_instantiation():
    """Verify customer domain model and search result DTO can be instantiated."""
    customer = Customer(customer_id="cust-1", name="Jane Doe", email="jane@example.com")
    assert customer.customer_id == "cust-1"
    assert customer.name == "Jane Doe"
    assert customer.email == "jane@example.com"

    result_dto = CustomerSearchResult(
        customer_id="cust-1", name="Jane Doe", email="jane@example.com"
    )
    assert result_dto.customer_id == "cust-1"
    assert result_dto.name == "Jane Doe"
    assert result_dto.email == "jane@example.com"


def test_repository_interface_and_implementation():
    """Verify repository layer adheres to interface contract."""
    customers = [Customer(customer_id="1", name="Alice", email="alice@example.com")]
    repo = InMemoryCustomerRepository(customers)
    assert isinstance(repo, ICustomerRepository)
    assert repo.search_customers("Alice") == customers


def test_validation_and_auth_components():
    """Verify validation and authorization components instantiate and execute."""
    validator = SearchInputValidator()
    assert validator.sanitize_query("  john  ") == "john"

    authorizer = CustomerSearchAuthorizer()
    assert authorizer.is_user_authorized_for_search({"is_authorized": True}) is True


def test_layers_wiring_and_controller_reference():
    """Verify layered architecture wiring from Controller to Repository."""
    customer = Customer(customer_id="100", name="Bob Smith", email="bob@example.com")
    repo = InMemoryCustomerRepository([customer])
    validator = SearchInputValidator()
    authorizer = CustomerSearchAuthorizer()
    service = CustomerSearchService(repository=repo, validator=validator, authorizer=authorizer)
    controller = CustomerSearchController(search_service=service)

    # Verify query handling and response structure defined in ARCHITECTURE.md
    response = controller.handle_search_request({"q": "Bob"})
    assert "results" in response
    assert len(response["results"]) == 1
    assert response["results"][0] == {
        "customerId": "100",
        "name": "Bob Smith",
        "email": "bob@example.com",
    }
