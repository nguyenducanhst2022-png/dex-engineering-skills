# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Adapter Registry
Manages adapter lifecycle, resolution, and dispatch.
"""

from typing import Dict, Optional, List
from ..adapters.base import BaseAdapter
from ..adapters import ALL_ADAPTERS

class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, BaseAdapter] = {}
        self._initialize_adapters()

    def _initialize_adapters(self):
        for adapter_cls in ALL_ADAPTERS:
            adapter = adapter_cls()
            self._adapters[adapter.language] = adapter

    def get_adapter(self, language: str) -> Optional[BaseAdapter]:
        """Lookup adapter by canonical language name or alias."""
        norm = language.strip().lower()
        aliases = {
            "py": "python",
            "ts": "typescript",
            "js": "javascript",
            "ps": "powershell",
            "pwsh": "powershell",
            "sh": "bash",
            "shell": "bash",
            "rs": "rust",
            "golang": "go",
            "c++": "cpp",
            "cs": "csharp",
            "dotnet": "csharp",
        }
        canonical = aliases.get(norm, norm)
        return self._adapters.get(canonical)

    def list_languages(self) -> List[str]:
        return sorted(list(self._adapters.keys()))

    def get_all_adapters(self) -> List[BaseAdapter]:
        return list(self._adapters.values())

# Global registry singleton
REGISTRY = AdapterRegistry()
