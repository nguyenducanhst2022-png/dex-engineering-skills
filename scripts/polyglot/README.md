# DEX Polyglot Script Engine v8.0.0

A production-grade, multi-language developer automation and testing subsystem for the DEX Engineering Skills Framework. Supports **11 programming languages**: Python, TypeScript, JavaScript, PowerShell, Bash, Rust, Go, C++, C#, Java, and PHP.

## Architecture

```
scripts/polyglot/
├── core/                  # Core runtime components
│   ├── detector.py        # Language marker detection & confidence scoring
│   ├── executor.py        # Safe subprocess execution (shell=False, 512KB cap, timeouts)
│   ├── security.py        # Secret redaction, path traversal & command safety
│   ├── result_schema.py   # Standard JSON execution contract (v1.0.0)
│   ├── registry.py        # Dynamic adapter registration & dispatch
│   ├── reporting.py       # Terminal, JSON, and Markdown formatters
│   └── generator.py       # Code & companion test scaffolding
├── adapters/              # 11 language-specific lifecycle adapters
│   ├── base.py            # Abstract BaseAdapter
│   ├── python_adapter.py  # Python (pytest, ruff, mypy)
│   ├── typescript_adapter.py # TypeScript (tsc, eslint, vitest)
│   ├── javascript_adapter.py # JavaScript (node, npm, eslint)
│   ├── powershell_adapter.py # PowerShell (Pester, PSScriptAnalyzer)
│   ├── bash_adapter.py    # Bash / POSIX (shellcheck, bats)
│   ├── rust_adapter.py    # Rust (cargo test, clippy, check)
│   ├── go_adapter.py      # Go (go test, vet, govulncheck)
│   ├── cpp_adapter.py     # C++ (CMake, CTest, clang-tidy)
│   ├── csharp_adapter.py  # C# (.NET SDK, dotnet test, format)
│   ├── java_adapter.py    # Java (Maven / Gradle, checkstyle)
│   └── php_adapter.py     # PHP (Composer, phpunit, phpstan)
├── wrappers/              # Native shell wrappers
│   ├── dex.ps1            # Windows PowerShell wrapper
│   ├── dex.bat            # Windows Batch wrapper
│   └── dex.sh             # Linux / macOS Bash wrapper
├── schemas/
│   └── result.schema.json # JSON schema for execution results
├── tests/                 # Unit & integration test suite
│   ├── fixtures/          # 11 language fixtures
│   └── ...
└── dex.py                 # Main CLI entrypoint
```

## Quick Start

### Cross-Platform CLI
```powershell
# Windows PowerShell
.\scripts\polyglot\wrappers\dex.ps1 status
.\scripts\polyglot\wrappers\dex.ps1 doctor
.\scripts\polyglot\wrappers\dex.ps1 test --lang python

# Unix / macOS
./scripts/polyglot/wrappers/dex.sh status
./scripts/polyglot/wrappers/dex.sh doctor

# Direct Python
python scripts/polyglot/dex.py status -f json
```

### Supported Lifecycle Commands
- `status`: Show supported languages, host availability, and workspace markers.
- `doctor`: Comprehensive healthcheck across all 11 toolchains.
- `detect`: Scan directory for language markers with confidence scoring.
- `lint`: Run linter for target language.
- `typecheck`: Run static typechecker.
- `build`: Compile or package project.
- `test`: Run test suite with optional `--filter`.
- `audit`: Scan for known dependency vulnerabilities.
- `benchmark`: Run performance benchmarks.
- `generate`: Scaffold verified starter code and companion tests.

### Safety Guarantees
1. **Subprocess Isolation**: All commands execute with `shell=False` and explicit argument lists.
2. **Buffer Limits**: `stdout` and `stderr` are strictly capped at 512 KB to prevent memory exhaustion.
3. **Timeouts**: Every subprocess execution has a hard timeout limit (default: 60s).
4. **Secret Sanitization**: AWS keys, GitHub tokens, private keys, and passwords are automatically redacted from all outputs.
5. **Path Traversal Protection**: Execution directory (`cwd`) is validated against directory traversal attacks.
6. **Toolchain Availability**: When a tool is missing on the host, the engine gracefully returns `TOOL_NOT_AVAILABLE` with verified installation commands without crashing.
