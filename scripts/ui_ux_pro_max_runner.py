# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — UI/UX PRO MAX RUNNER & DETECTION BRIDGE (scripts/ui_ux_pro_max_runner.py)
Bridges DEX AI agents to the UI/UX Pro Max search engine.
Supports Option A (External Runtime detection) and Option B (Approved Local Vendored Runtime).
Guarantees non-hallucinatory output: reports explicit NOT INSTALLED status when runtime is absent.
"""

import os
import sys
import json
import subprocess
import argparse

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VENDORED_RUNTIME_DIR = os.path.join(ROOT_DIR, "integrations", "ui-ux-pro-max", "runtime")
VENDORED_SEARCH_SCRIPT = os.path.join(VENDORED_RUNTIME_DIR, "scripts", "search.py")

KNOWN_EXTERNAL_PATHS = [
    os.path.expanduser("~/.codex/skills/ui-ux-pro-max"),
    os.path.expanduser("~/.claude/skills/ui-ux-pro-max"),
    os.path.expanduser("~/.cursor/skills/ui-ux-pro-max"),
    os.path.expanduser("~/.gemini/antigravity/skills/ui-ux-pro-max"),
    os.path.expanduser("~/.agent/skills/ui-ux-pro-max"),
    os.path.expandvars("%USERPROFILE%\\.codex\\skills\\ui-ux-pro-max"),
    os.path.expandvars("%APPDATA%\\Claude\\skills\\ui-ux-pro-max"),
]

VALID_DOMAINS = [
    "style", "color", "chart", "landing", "product", "ux",
    "typography", "icons", "gsap", "react", "web", "google-fonts"
]

VALID_STACKS = [
    "react", "nextjs", "vue", "svelte", "astro", "swiftui",
    "react-native", "flutter", "nuxtjs", "nuxt-ui", "html-tailwind",
    "shadcn", "jetpack-compose", "threejs", "angular", "laravel",
    "javafx", "wpf", "winui", "avalonia", "uno", "uwp"
]

def detect_runtime() -> dict:
    """Detects available UI/UX Pro Max runtime across environment, global paths, and local vendored files."""
    # 1. Custom environment variable (highest precedence)
    env_path = os.environ.get("UI_UX_PRO_MAX_PATH")
    if env_path:
        search_py = os.path.join(env_path, "scripts", "search.py")
        if not os.path.isfile(search_py):
            search_py = os.path.join(env_path, "src", "ui-ux-pro-max", "scripts", "search.py")
        if os.path.isfile(search_py):
            return {
                "installed": True,
                "mode": "EXTERNAL_ENV",
                "search_script": os.path.abspath(search_py),
                "runtime_dir": os.path.abspath(env_path),
                "details": f"Found via UI_UX_PRO_MAX_PATH: {env_path}"
            }

    # 2. Known assistant global skill directories
    for p in KNOWN_EXTERNAL_PATHS:
        if os.path.isdir(p):
            search_py = os.path.join(p, "scripts", "search.py")
            if not os.path.isfile(search_py):
                search_py = os.path.join(p, "src", "ui-ux-pro-max", "scripts", "search.py")
            if os.path.isfile(search_py):
                return {
                    "installed": True,
                    "mode": "EXTERNAL_GLOBAL",
                    "search_script": os.path.abspath(search_py),
                    "runtime_dir": os.path.abspath(p),
                    "details": f"Found in global skill path: {p}"
                }

    # 3. Local approved vendored runtime (Option B fallback)
    if os.path.isfile(VENDORED_SEARCH_SCRIPT):
        return {
            "installed": True,
            "mode": "VENDORED_LOCAL",
            "search_script": os.path.abspath(VENDORED_SEARCH_SCRIPT),
            "runtime_dir": os.path.abspath(VENDORED_RUNTIME_DIR),
            "details": f"Found in DEX approved vendored runtime: {VENDORED_RUNTIME_DIR}"
        }

    # 4. Runtime completely absent
    return {
        "installed": False,
        "mode": "NOT_INSTALLED",
        "search_script": None,
        "runtime_dir": None,
        "details": "UI/UX Pro Max runtime not detected at standard locations, UI_UX_PRO_MAX_PATH, or local integrations directory."
    }

def is_runtime_installed() -> bool:
    """Returns True if any valid UI/UX Pro Max search engine is detected."""
    return detect_runtime()["installed"]

def search(
    query: str,
    domain: str = None,
    stack: str = None,
    design_system: bool = False,
    max_results: int = 3,
    json_output: bool = True,
    project_name: str = None,
    output_format: str = "markdown",
    variance: int = None,
    motion: int = None,
    density: int = None
) -> dict | str:
    """
    Executes search against real UI/UX Pro Max search engine.
    Returns parsed dictionary (if json_output=True) or formatted string.
    If runtime is NOT installed, returns a non-hallucinatory error structure.
    """
    rt = detect_runtime()
    if not rt["installed"]:
        err_msg = (
            "STATUS: NOT INSTALLED\n"
            "UI/UX Pro Max search engine is not installed or detected.\n"
            "To install upstream runtime, run:\n"
            "  git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git\n"
            "or set UI_UX_PRO_MAX_PATH environment variable."
        )
        if json_output:
            return {
                "status": "NOT_INSTALLED",
                "error": err_msg,
                "installed": False,
                "results": []
            }
        return err_msg

    search_script = rt["search_script"]
    cmd = [sys.executable, search_script, query]

    if domain:
        if domain not in VALID_DOMAINS:
            raise ValueError(f"Invalid domain '{domain}'. Must be one of: {', '.join(VALID_DOMAINS)}")
        cmd.extend(["--domain", domain])

    if stack:
        if stack not in VALID_STACKS:
            raise ValueError(f"Invalid stack '{stack}'. Must be one of: {', '.join(VALID_STACKS)}")
        cmd.extend(["--stack", stack])

    if design_system:
        cmd.append("--design-system")
        if project_name:
            cmd.extend(["--project-name", project_name])
        if output_format:
            cmd.extend(["--format", output_format])
        if variance is not None:
            cmd.extend(["--variance", str(variance)])
        if motion is not None:
            cmd.extend(["--motion", str(motion)])
        if density is not None:
            cmd.extend(["--density", str(density)])

    if json_output and not design_system:
        cmd.append("--json")
    elif not design_system:
        cmd.extend(["--max-results", str(max_results)])

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            timeout=30
        )
    except Exception as e:
        if json_output:
            return {"status": "EXECUTION_ERROR", "error": str(e), "results": []}
        return f"EXECUTION_ERROR: {e}"

    if proc.returncode != 0 and not proc.stdout.strip():
        err = proc.stderr.strip() or f"Process exited with code {proc.returncode}"
        if json_output:
            return {"status": "ERROR", "error": err, "results": []}
        return f"ERROR: {err}"

    stdout = proc.stdout.strip()
    if json_output and not design_system:
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {"status": "RAW_TEXT", "raw": stdout, "results": []}

    return stdout

def main():
    parser = argparse.ArgumentParser(description="DEX UI/UX Pro Max Bridge & Runner")
    parser.add_argument("query", nargs="?", default="", help="Design search query")
    parser.add_argument("--status", action="store_true", help="Check runtime installation status")
    parser.add_argument("--domain", "-d", choices=VALID_DOMAINS, help="Search domain")
    parser.add_argument("--stack", "-s", choices=VALID_STACKS, help="Target tech stack")
    parser.add_argument("--design-system", "-ds", action="store_true", help="Generate full design system")
    parser.add_argument("--project-name", "-p", help="Project name for design system")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="markdown", help="Design system format")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--max-results", "-n", type=int, default=3, help="Max results")

    args = parser.parse_args()

    if args.status:
        rt = detect_runtime()
        print("=== UI/UX PRO MAX RUNTIME STATUS ===")
        print(f"Installed    : {rt['installed']}")
        print(f"Mode         : {rt['mode']}")
        print(f"Search Script: {rt['search_script']}")
        print(f"Details      : {rt['details']}")
        sys.exit(0 if rt["installed"] else 1)

    if not args.query:
        parser.print_help()
        sys.exit(1)

    res = search(
        query=args.query,
        domain=args.domain,
        stack=args.stack,
        design_system=args.design_system,
        max_results=args.max_results,
        json_output=args.json,
        project_name=args.project_name,
        output_format=args.format
    )

    if isinstance(res, dict):
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(res)

if __name__ == "__main__":
    main()
