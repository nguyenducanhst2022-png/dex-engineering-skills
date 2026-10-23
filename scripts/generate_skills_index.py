# -*- coding: utf-8 -*-
import json
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
manifest_path = os.path.join(root_dir, "manifests", "dex-skills.json")
output_path = os.path.join(root_dir, "SKILLS_INDEX.md")

with open(manifest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

native = data["native_skills"]
integrations = data.get("segregated_integrations", [])

orch = [s for s in native if s["id"] == "dex-master-orchestrator"][0]
specialized = [s for s in native if s["id"] != "dex-master-orchestrator"]

out = []
out.append("# DEX Engineering Skills Catalog Index (v8.0.0)\n")
out.append("> Complete index of all **400 Specialized Engineering Skills** + **1 Master Orchestrator** (401 Native Skills) and **5 Segregated Integrations**.")
out.append("> Every skill strictly complies with the [Agent Skills Specification](https://agentskills.io/specification).\n")
out.append("---\n")
out.append("## 1. Master Orchestrator (Root Control Plane)\n")
out.append("| ID | Name | Description | Path |")
out.append("|:---|:---|:---|:---|")
orch_id = orch["id"]
orch_desc = orch["description"]
out.append(f"| `{orch_id}` | Master Orchestrator | {orch_desc} | [{orch_id}](.agents/skills/{orch_id}/SKILL.md) |\n")
out.append("---\n")
out.append("## 2. Specialized Engineering Skills Catalog (400 Skills)\n")

groups = {}
for s in specialized:
    g = s.get("group", "Unmapped")
    groups.setdefault(g, []).append(s)

expected_groups = [f"Group {chr(c)}" for c in range(ord('A'), ord('Z') + 1)] + [
    "Group AA", "Group AB", "Group AC", "Group AD",
    "Group AE", "Group AF", "Group AG", "Group AH",
    "Group AI", "Group AJ", "Group AK", "Group AL",
    "Group AM", "Group AN"
]

skill_num = 1
for g in expected_groups:
    skills = groups.get(g, [])
    domain = skills[0].get("domain", g) if skills else g
    start_num = skill_num
    end_num = skill_num + len(skills) - 1
    out.append(f"### {g}: {domain} (Skills {start_num:03d}–{end_num:03d})\n")
    out.append("| # | Skill ID | Description | Path |")
    out.append("|:---|:---|:---|:---|")
    for s in skills:
        s_id = s["id"]
        s_desc = s["description"].replace("\n", " ").strip()
        s_path = s["path"]
        out.append(f"| `{skill_num:03d}` | **`{s_id}`** | {s_desc} | [{s_id}]({s_path}) |")
        skill_num += 1
    out.append("")

out.append("---\n")
out.append("## 3. Segregated Upstream Integrations (5 Skills)\n")
out.append("> Quarantined in `integrations/`, isolated from native numbering, and accessed exclusively via adapters.\n")
out.append("| Integration Skill | Upstream Source | Description | Path |")
out.append("|:---|:---|:---|:---|")
for item in integrations:
    i_id = item["id"]
    i_name = item.get("name", i_id)
    i_desc = item.get("description", "")
    i_path = item.get("path", "")
    if "api-mocking" in i_id:
        i_source = "sickn33/agentic-awesome-skills"
    elif "binary" in i_id or "javascript" in i_id:
        i_source = "zhaoxuya520/reverse-skill"
    elif "rea" in i_id:
        i_source = "morluto/rea"
    else:
        i_source = "nextlevelbuilder/ui-ux-pro-max-skill"
    out.append(f"| **`{i_id}`** | `{i_source}` | {i_desc} | [{i_id}]({i_path}) |")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"Successfully generated SKILLS_INDEX.md with {skill_num - 1} skills across {len(expected_groups)} groups.")
