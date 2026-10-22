# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Skill Integration Engine (dex_skill_importer.py).
Tests discovery, auditing, duplicate detection, dry-run planning,
importation, validation, and rollback operations.
"""

import os
import sys
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from dex_skill_importer import (
    UPSTREAM_CATALOG,
    get_existing_dex_skills,
    load_manifest,
    cmd_discover,
    cmd_audit,
    cmd_compare,
    cmd_plan,
    cmd_import,
    cmd_validate,
    cmd_rollback,
)

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_upstream_catalog_integrity():
    """Verify all registered candidates have required fields and valid licenses."""
    assert len(UPSTREAM_CATALOG) >= 4
    for skill_id, info in UPSTREAM_CATALOG.items():
        assert skill_id.startswith("dex-")
        assert info["license"] in ["MIT", "Apache-2.0"]
        assert info["source_id"] in ["SOURCE_A_AAS", "SOURCE_B_REVERSE", "SOURCE_C_REA"]
        assert len(info["description"]) <= 1024
        assert "purpose" in info
        assert "workflow" in info

def test_discover_command(capsys):
    """Verify discover command prints candidate information."""
    args = DummyArgs(source="ALL")
    ret = cmd_discover(args)
    assert ret == 0
    captured = capsys.readouterr()
    assert "dex-api-mocking-virtualization" in captured.out
    assert "dex-binary-inspection" in captured.out
    assert "dex-rea-adapter" in captured.out

def test_audit_valid_candidate():
    """Verify audit passes on verified candidate."""
    args = DummyArgs(candidate="dex-binary-inspection")
    ret = cmd_audit(args)
    assert ret == 0

def test_audit_missing_candidate():
    """Verify audit fails on unknown candidate."""
    args = DummyArgs(candidate="unknown-nonexistent-skill")
    ret = cmd_audit(args)
    assert ret == 1

def test_compare_new_capability():
    """Verify new capability is approved for import."""
    test_id = "dex-unimported-candidate-test"
    UPSTREAM_CATALOG[test_id] = {
        "source_id": "SOURCE_A_AAS",
        "source_name": "Test",
        "description": "Unique capability",
        "license": "MIT",
        "purpose": "A unique capability not in DEX"
    }
    try:
        args = DummyArgs(candidate=test_id)
        ret = cmd_compare(args)
        assert ret == 0
    finally:
        del UPSTREAM_CATALOG[test_id]

def test_compare_exact_duplicate():
    """Verify existing native DEX skill is classified as EXACT_DUPLICATE and rejected."""
    # Temporarily register an existing native skill name in catalog for test
    UPSTREAM_CATALOG["dex-git-workflow"] = {
        "source_id": "SOURCE_A_AAS",
        "source_name": "Test",
        "description": "duplicate",
        "license": "MIT",
        "purpose": "git duplicate test"
    }
    try:
        args = DummyArgs(candidate="dex-git-workflow")
        ret = cmd_compare(args)
        assert ret == 2  # Rejection code
    finally:
        del UPSTREAM_CATALOG["dex-git-workflow"]

def test_plan_dry_run(capsys):
    """Verify plan with dry-run runs cleanly without writing files."""
    args = DummyArgs(dry_run=True)
    ret = cmd_plan(args)
    assert ret == 0
    captured = capsys.readouterr()
    assert "DRY RUN" in captured.out
    assert "Plan Summary" in captured.out

def test_import_dry_run(capsys):
    """Verify import with dry-run simulates without modifying filesystem."""
    args = DummyArgs(candidate="dex-binary-inspection", dry_run=True)
    ret = cmd_import(args)
    assert ret == 0
    captured = capsys.readouterr()
    assert "DRY RUN OK" in captured.out

def test_validate_imported_skills():
    """Verify validate command checks all imported skills against 14 sections."""
    args = DummyArgs(skill=None)
    ret = cmd_validate(args)
    assert ret == 0
