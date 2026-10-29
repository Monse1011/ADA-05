#!/usr/bin/env python3
"""Repository contract checks for Customer Search (run by scripts/verify_repo.sh).

Checks:
1. Protected files (specification and historical ADA-05 evidence) are byte-identical
   to the approved versions. Changing one is a human decision: update its hash here
   in the same change, with the owner's approval.
2. Layer imports follow ARCHITECTURE.md: dependencies point down, and the API never
   reaches the repository directly.
3. Every FR/NFR ID in " REQUIREMENTS.md" appears in docs/TRACEABILITY.md.
"""

import ast
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The leading space in " REQUIREMENTS.md" is intentional and must not be "fixed".
PROTECTED_SHA256 = {
    " REQUIREMENTS.md": "cb0dc91f322b4faa75f5930138ef23fd16268dd5c2d757b18bce7d8706585c85",
    "SPEC.md": "e91b7932282ea461a91a0dd11eb02a1c47b8ba14035e68791d534e87f7feb8cf",
    "ARCHITECTURE.md": "280fbcac21a633def0d925c314e2187ba4f48e57b52604faf5206d5cf2ee7bb4",
    "TASKS.md": "47c86d7787bb0356d0f1d6db46afc68cb88f06476bc5d30267ed875a1c32291f",
    "docs/AGENT_REPORT.md": "6098beff4005ec8fb1a82e797146d16156c14e0926b49f2d6e517921c6369368",
    "docs/AI_USAGE_LOG.md": "0bf7785570d5bab151f8797da3370b13bcd1efe6c7df52ad1d80f37e2e718b8e",
}

# Allowed internal imports per layer (package under customer_search/).
ALLOWED_IMPORTS = {
    "models": set(),
    "validation": set(),
    "repositories": {"models"},
    "auth": {"models"},
    "services": {"models", "repositories", "validation", "auth"},
    "api": {"services", "models", "validation", "auth"},
}


def check_protected_files(root):
    errors = []
    for rel, expected in PROTECTED_SHA256.items():
        path = root / rel
        if not path.is_file():
            errors.append(f"protected file missing: {rel!r}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f"protected file modified: {rel!r} (needs owner approval + hash update)")
    return errors


def layer_violations(layer, source, filename="<source>"):
    """Return the internal layers imported by `source` that `layer` may not use."""
    bad = []
    for node in ast.walk(ast.parse(source, filename)):
        names = []
        if isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        elif isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        for name in names:
            parts = name.split(".")
            if parts[0] == "customer_search" and len(parts) > 1:
                target = parts[1]
                if target != layer and target not in ALLOWED_IMPORTS.get(layer, set()):
                    bad.append(target)
    return bad


def check_layers(root):
    errors = []
    pkg = root / "customer_search"
    for path in sorted(pkg.glob("*/*.py")):
        layer = path.parent.name
        if layer not in ALLOWED_IMPORTS:
            errors.append(f"unknown layer package: customer_search/{layer} (add it to ARCHITECTURE.md and this check)")
            continue
        for target in layer_violations(layer, path.read_text(), str(path)):
            errors.append(f"layer violation: {path.relative_to(root)} imports customer_search.{target}")
    return errors


def check_traceability(root):
    if not (root / " REQUIREMENTS.md").is_file():
        return []  # already reported by check_protected_files
    req = (root / " REQUIREMENTS.md").read_text()
    trace = (root / "docs/TRACEABILITY.md").read_text()
    ids = sorted(set(re.findall(r"\*\*((?:FR|NFR)-\d+):\*\*", req)))
    return [f"requirement {i} not traced in docs/TRACEABILITY.md" for i in ids if f"| {i} |" not in trace]


def main():
    errors = check_protected_files(ROOT) + check_layers(ROOT) + check_traceability(ROOT)
    for e in errors:
        print(f"CONTRACT FAIL: {e}")
    print("Repository contract: " + ("FAILED" if errors else "OK"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
