# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Language & Toolchain Detector
Scans project directories for language markers, package managers, and toolchains.
Calculates confidence scores (0.0 to 1.0) and probes runtime availability.
"""

import os
import shutil
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

# Language definitions with primary markers and extension patterns
LANGUAGE_MARKERS: Dict[str, Dict[str, Any]] = {
    "python": {
        "primary": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile", "poetry.lock"],
        "extensions": [".py", ".pyi"],
        "tools": ["python", "python3", "pytest"],
    },
    "typescript": {
        "primary": ["tsconfig.json"],
        "extensions": [".ts", ".tsx"],
        "tools": ["tsc", "npx", "node"],
    },
    "javascript": {
        "primary": ["package.json"],
        "extensions": [".js", ".mjs", ".cjs", ".jsx"],
        "tools": ["node", "npm", "yarn", "pnpm"],
    },
    "powershell": {
        "primary": ["PSScriptAnalyzerSettings.psd1"],
        "extensions": [".ps1", ".psm1", ".psd1"],
        "tools": ["pwsh", "powershell"],
    },
    "bash": {
        "primary": [".shellcheckrc"],
        "extensions": [".sh", ".bash"],
        "tools": ["bash", "sh"],
    },
    "rust": {
        "primary": ["Cargo.toml", "Cargo.lock"],
        "extensions": [".rs"],
        "tools": ["cargo", "rustc"],
    },
    "go": {
        "primary": ["go.mod", "go.sum"],
        "extensions": [".go"],
        "tools": ["go"],
    },
    "cpp": {
        "primary": ["CMakeLists.txt", "conanfile.txt", "vcpkg.json"],
        "extensions": [".cpp", ".hpp", ".cc", ".cxx", ".h"],
        "tools": ["cmake", "g++", "clang++", "ninja"],
    },
    "csharp": {
        "primary": ["global.json"],
        "extensions": [".csproj", ".sln", ".cs"],
        "tools": ["dotnet"],
    },
    "java": {
        "primary": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "extensions": [".java"],
        "tools": ["mvn", "gradle", "javac", "java"],
    },
    "php": {
        "primary": ["composer.json", "composer.lock"],
        "extensions": [".php"],
        "tools": ["php", "composer"],
    },
}

def probe_tool(tool_name: str) -> Dict[str, Any]:
    """
    Probe the presence and version of a tool on the host system.
    Handles Windows script extensions (.cmd, .bat).
    """
    resolved = None
    if platform.system() == "Windows":
        for ext in ["", ".cmd", ".exe", ".bat"]:
            candidate = f"{tool_name}{ext}" if ext else tool_name
            found = shutil.which(candidate)
            if found:
                resolved = found
                break
    else:
        resolved = shutil.which(tool_name)

    if not resolved:
        return {
            "tool": tool_name,
            "available": False,
            "path": None,
            "version": None,
        }

    # Attempt to query version with timeout
    version_str = None
    for flag in ["--version", "-version", "-v", "version"]:
        try:
            proc = subprocess.run(
                [resolved, flag],
                capture_output=True,
                text=True,
                timeout=3,
                shell=False
            )
            raw = (proc.stdout or proc.stderr).strip()
            if raw:
                # First non-empty line
                first_line = raw.splitlines()[0].strip()
                if len(first_line) < 80:
                    version_str = first_line
                    break
        except Exception:
            continue

    return {
        "tool": tool_name,
        "available": True,
        "path": resolved,
        "version": version_str or "detected",
    }

def detect_languages(target_dir: str = ".") -> List[Dict[str, Any]]:
    """
    Scan target_dir and detect languages with confidence scores.
    Returns list of dicts sorted descending by confidence score.
    """
    target = Path(target_dir).resolve()
    if not target.exists() or not target.is_dir():
        return []

    # Gather files (depth up to 2 for performance)
    files_in_dir = set()
    extensions_in_dir = set()

    for item in os.listdir(target):
        item_path = target / item
        if item_path.is_file():
            files_in_dir.add(item)
            extensions_in_dir.add(item_path.suffix.lower())
        elif item_path.is_dir() and item not in [".git", "node_modules", "target", ".venv", "venv", "__pycache__", "build", "dist"]:
            try:
                for sub in os.listdir(item_path):
                    sub_path = item_path / sub
                    if sub_path.is_file():
                        files_in_dir.add(sub)
                        extensions_in_dir.add(sub_path.suffix.lower())
            except Exception:
                pass

    results = []

    for lang, markers in LANGUAGE_MARKERS.items():
        confidence = 0.0
        found_markers = []

        # Check primary marker files (strong signal)
        for primary in markers["primary"]:
            if primary in files_in_dir:
                confidence += 0.70
                found_markers.append(primary)

        # Check file extensions (moderate signal)
        for ext in markers["extensions"]:
            if ext in extensions_in_dir:
                confidence += 0.25
                found_markers.append(f"*{ext}")
                break

        # Check if package.json has typescript dependency
        if lang == "typescript" and "package.json" in files_in_dir:
            pkg_path = target / "package.json"
            try:
                with open(pkg_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if '"typescript"' in content:
                        confidence += 0.50
                        found_markers.append("package.json[typescript]")
            except Exception:
                pass

        # Disambiguate JS vs TS if TS markers present
        if lang == "javascript" and "tsconfig.json" in files_in_dir:
            confidence = min(confidence, 0.40)

        # Cap confidence at 1.0
        final_conf = min(round(confidence, 2), 1.0)
        if final_conf > 0.0:
            results.append({
                "language": lang,
                "confidence": final_conf,
                "markers_found": list(set(found_markers)),
            })

    # Sort descending by confidence
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results
