# -*- coding: utf-8 -*-
import os
from pathlib import Path

base = Path("scripts/polyglot/tests/fixtures")

fixtures = {
    "python": {
        "app.py": "def main():\n    return 42\n\nif __name__ == '__main__':\n    print(main())\n"
    },
    "typescript": {
        "tsconfig.json": "{\n  \"compilerOptions\": {\"target\": \"ES2022\"}\n}\n",
        "app.ts": "export const answer: number = 42;\n"
    },
    "javascript": {
        "package.json": "{\n  \"name\": \"js-fixture\",\n  \"version\": \"1.0.0\"\n}\n",
        "index.js": "module.exports = 42;\n"
    },
    "powershell": {
        "script.ps1": "Write-Output 42\n"
    },
    "bash": {
        "script.sh": "#!/usr/bin/env bash\necho 42\n"
    },
    "rust": {
        "Cargo.toml": "[package]\nname = \"rust_fixture\"\nversion = \"0.1.0\"\nedition = \"2021\"\n",
        "src/main.rs": "fn main() {\n    println!(\"42\");\n}\n"
    },
    "go": {
        "go.mod": "module go_fixture\n\ngo 1.22\n",
        "main.go": "package main\n\nimport \"fmt\"\n\nfunc main() {\n\tfmt.Println(42)\n}\n"
    },
    "cpp": {
        "CMakeLists.txt": "cmake_minimum_required(VERSION 3.20)\nproject(cpp_fixture)\nadd_executable(main main.cpp)\n",
        "main.cpp": "#include <iostream>\nint main() { std::cout << 42 << std::endl; return 0; }\n"
    },
    "csharp": {
        "App.csproj": "<Project Sdk=\"Microsoft.NET.Sdk\">\n  <PropertyGroup>\n    <OutputType>Exe</OutputType>\n    <TargetFramework>net8.0</TargetFramework>\n  </PropertyGroup>\n</Project>\n",
        "Program.cs": "using System;\nclass Program { static void Main() => Console.WriteLine(42); }\n"
    },
    "java": {
        "pom.xml": "<project xmlns=\"http://maven.apache.org/POM/4.0.0\"><modelVersion>4.0.0</modelVersion><groupId>com.dex</groupId><artifactId>fixture</artifactId><version>1.0</version></project>\n",
        "App.java": "public class App { public static void main(String[] args) { System.out.println(42); } }\n"
    },
    "php": {
        "composer.json": "{\n  \"name\": \"dex/php-fixture\"\n}\n",
        "index.php": "<?php\necho 42 . PHP_EOL;\n"
    }
}

for lang, files in fixtures.items():
    lang_dir = base / lang
    for rel_path, content in files.items():
        file_path = lang_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

print("All 11 polyglot fixtures created successfully.")
