# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Language Adapters Registry
Exports base adapter and all 11 language implementations.
"""

from .base import BaseAdapter
from .python_adapter import PythonAdapter
from .typescript_adapter import TypeScriptAdapter
from .javascript_adapter import JavaScriptAdapter
from .powershell_adapter import PowerShellAdapter
from .bash_adapter import BashAdapter
from .rust_adapter import RustAdapter
from .go_adapter import GoAdapter
from .cpp_adapter import CppAdapter
from .csharp_adapter import CSharpAdapter
from .java_adapter import JavaAdapter
from .php_adapter import PhpAdapter

ALL_ADAPTERS = [
    PythonAdapter,
    TypeScriptAdapter,
    JavaScriptAdapter,
    PowerShellAdapter,
    BashAdapter,
    RustAdapter,
    GoAdapter,
    CppAdapter,
    CSharpAdapter,
    JavaAdapter,
    PhpAdapter,
]

__all__ = [
    "BaseAdapter",
    "PythonAdapter",
    "TypeScriptAdapter",
    "JavaScriptAdapter",
    "PowerShellAdapter",
    "BashAdapter",
    "RustAdapter",
    "GoAdapter",
    "CppAdapter",
    "CSharpAdapter",
    "JavaAdapter",
    "PhpAdapter",
    "ALL_ADAPTERS",
]
