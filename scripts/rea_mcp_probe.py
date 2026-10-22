# -*- coding: utf-8 -*-
"""
REA MCP Capability Probe & Environment Diagnostic Tool.
Probes local environment for Reverse Engineer Anything (REA) MCP server registration,
returns tool schemas, connectivity status, or non-hallucinatory setup guidance.
"""

import os
import sys
import json
import shutil
import argparse

KNOWN_MCP_CONFIG_PATHS = [
    # Claude Desktop
    os.path.expanduser("~/.config/Claude/claude_desktop_config.json"),
    os.path.expandvars("%APPDATA%\\Claude\\claude_desktop_config.json"),
    # Cursor
    os.path.expanduser("~/.cursor/mcp.json"),
    os.path.expandvars("%APPDATA%\\Cursor\\mcp.json"),
    # Windsurf
    os.path.expanduser("~/.codeium/windsurf/mcp_config.json"),
    os.path.expandvars("%USERPROFILE%\\.codeium\\windsurf\\mcp_config.json"),
]

REA_TOOL_SCHEMAS = [
    {
        "name": "rea_inspect_binary",
        "description": "Inspect binary headers, format, architecture, and basic properties without execution.",
        "parameters": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Absolute path to target binary"}
            },
            "required": ["binary_path"]
        }
    },
    {
        "name": "rea_decompile_function",
        "description": "Decompile specific function or symbol address into pseudo-C representation using local decompiler.",
        "parameters": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Absolute path to target binary"},
                "symbol_or_address": {"type": "string", "description": "Function name or hexadecimal address (e.g., 0x140001000)"}
            },
            "required": ["binary_path", "symbol_or_address"]
        }
    },
    {
        "name": "rea_extract_symbols",
        "description": "Dump import, export, and debug symbols from compiled binary.",
        "parameters": {
            "type": "object",
            "properties": {
                "binary_path": {"type": "string", "description": "Absolute path to target binary"}
            },
            "required": ["binary_path"]
        }
    }
]

def check_mcp_configs():
    """Scans standard MCP config files to see if 'rea' is registered."""
    detected_in = []
    for p in KNOWN_MCP_CONFIG_PATHS:
        if os.path.isfile(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    mcp_servers = cfg.get("mcpServers", {})
                    for s_name, s_def in mcp_servers.items():
                        if "rea" in s_name.lower() or "rea" in json.dumps(s_def).lower():
                            detected_in.append((p, s_name))
            except Exception:
                pass
    return detected_in

def check_cli_binary():
    """Checks if npx rea-agents or rea CLI binary is installed in PATH."""
    cli_found = shutil.which("rea") is not None
    npx_found = shutil.which("npx") is not None
    return cli_found, npx_found

def probe_rea_mcp():
    configs = check_mcp_configs()
    cli_found, npx_found = check_cli_binary()
    
    # Check environment override
    env_endpoint = os.environ.get("REA_MCP_ENDPOINT")
    
    is_active = bool(configs or env_endpoint)
    
    result = {
        "mcp_server": "Reverse Engineer Anything (REA)",
        "status": "CONNECTED" if is_active else "NOT_CONFIGURED",
        "is_available": is_active,
        "config_locations": [c[0] for c in configs],
        "registered_server_names": [c[1] for c in configs],
        "env_endpoint": env_endpoint,
        "prerequisites": {
            "npx_available": npx_found,
            "rea_binary_available": cli_found,
        },
        "available_tools": REA_TOOL_SCHEMAS if is_active else [],
        "guidance": (
            "REA MCP is active and ready for authorized binary inspection."
            if is_active
            else "REA MCP server was not detected in local agent configs. To enable, run: 'npx rea-agents setup' or use the native 'dex-binary-inspection' fallback skill."
        )
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Probe REA MCP Server connectivity and available tool schemas.")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--check", action="store_true", help="Print summary status to stdout")
    args = parser.parse_args()

    probe_result = probe_rea_mcp()

    if args.json:
        print(json.dumps(probe_result, indent=2))
        return 0

    print("=== REA MCP ENVIRONMENT PROBE ===")
    print(f"Status:       {probe_result['status']}")
    print(f"Available:    {probe_result['is_available']}")
    print(f"Prereqs:      Node/NPX={probe_result['prerequisites']['npx_available']}, REA CLI={probe_result['prerequisites']['rea_binary_available']}")
    if probe_result['config_locations']:
        print(f"Config Found: {', '.join(probe_result['config_locations'])}")
    print(f"\nGuidance:\n  {probe_result['guidance']}")

    if probe_result['available_tools']:
        print(f"\nActive Tools ({len(probe_result['available_tools'])}):")
        for t in probe_result['available_tools']:
            print(f"  - {t['name']}: {t['description']}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
