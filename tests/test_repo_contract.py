"""Tests for scripts/check_repo_contract.py (repository guardrail, not product behavior)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_repo_contract", ROOT / "scripts/check_repo_contract.py")
contract = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(contract)


def test_layer_rule_rejects_api_importing_repository():
    src = "from customer_search.repositories.customer_repository import InMemoryCustomerRepository\n"
    assert contract.layer_violations("api", src) == ["repositories"]


def test_layer_rule_rejects_upward_import():
    src = "import customer_search.services.search_service\n"
    assert contract.layer_violations("repositories", src) == ["services"]


def test_layer_rule_allows_documented_dependencies():
    src = "from customer_search.models.customer import Customer\n"
    assert contract.layer_violations("repositories", src) == []


def test_repository_contract_holds():
    assert contract.check_protected_files(ROOT) == []
    assert contract.check_layers(ROOT) == []
    assert contract.check_traceability(ROOT) == []
