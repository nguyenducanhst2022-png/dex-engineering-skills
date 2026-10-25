import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.evaluate_routing import simulate_route
scenarios=[
('A','Review Supabase multi tenant PostgreSQL RLS SELECT INSERT UPDATE DELETE isolation.','dex-postgres-rls-policy-verification','dex-supabase-storage-access-policies','PostgreSQL test instance'),
('B','Validate agent tool permission scopes and approval boundaries.','dex-agent-tool-permission-modeling','dex-agent-execution-budget-controls','Isolated fake tools'),
('C','Validate HLS DASH streaming manifest segment references and codecs.','dex-streaming-manifest-validation','dex-video-transcoding-ladders','Manifest fixtures'),
('D','Test chess UCI handshake stop ponder command ordering.','dex-chess-uci-protocol-compliance','dex-chess-search-pruning-evals','Chess engine binary'),
('E','Review C++ Rust FFI ownership and ABI error boundaries.','dex-cpp-rust-ffi-validation','dex-chess-nnue-evaluation-integration','C++ and Rust compilers'),
('F','Reproduce Windows per monitor DPI coordinate translation bug.','dex-win32-dpi-multi-monitor-layout','dex-windows-com-interop','Windows multi-monitor host'),
('G','Test Kubernetes secret delivery and credential rotation.','dex-kubernetes-secret-delivery','dex-terraform-module-contract-tests','Isolated Kubernetes cluster'),
('H','Critique premium dashboard hierarchy typography spacing and visual quality.','dex-design-critique-rubric','dex-email-template-rendering','Browser and screenshot fixtures'),
('I','Verify TypeScript ESM CommonJS dual publish exports declarations with package consumers.','dex-typescript-package-dual-publish','dex-react-render-profiling','Node and TypeScript'),
('J','Diagnose Next.js App Router data cache invalidation stale reads.','dex-nextjs-app-router-data-cache','dex-vue-composition-reusability','Next.js application'),
('K','Audit dependency provenance attestation subject digest build identity.','dex-dependency-provenance-attestation','dex-disclosure-coordinated-triage','Attestation verifier'),
('L','Review skill conflict precedence across overlapping domain workflows.','dex-skill-conflict-precedence','dex-skill-lifecycle-health-dashboard','Conflicting instruction fixtures'),
('M','Test agent shutdown cancellation checkpoint recovery without repeated effects.','dex-agent-shutdown-and-cancellation','dex-agent-reviewer-independence','Isolated agent harness'),
('N','Revalidate upstream skill provenance pinned commit before import and rollback.','dex-skill-provenance-revalidation','dex-skill-task-suitability-classifier','Git and importer sandbox'),
('O','Test skill crosshost fixture compatibility across coding agent hosts.','dex-skill-crosshost-fixture-tests','dex-skill-progressive-disclosure-metrics','Actual target agent hosts'),
('P','Report skill lifecycle health dashboard actual counts and release evidence.','dex-skill-lifecycle-health-dashboard','dex-skill-task-suitability-classifier','Catalog and evidence records')]
catalog=json.loads((ROOT/'manifests/dex-skills.json').read_text(encoding='utf-8'))['native_skills']
results=[]
for id,prompt,expected,forbidden,tools in scenarios:
 actual=simulate_route(prompt,catalog)
 results.append({'id':id,'task_input':prompt,'expected_skills':[expected],'forbidden_skills':[forbidden],'required_tools':tools,'execution_steps':['Run metadata route simulation','Compare selected and forbidden skills','Execute selected skill on isolated domain fixture when available'], 'expected_output':'Expected skill selected and forbidden skill absent','actual_output':actual,'routing_result':'PASS' if expected in actual and forbidden not in actual else 'FAIL','domain_test_result':'NOT_VERIFIED','limitations':'Lexical simulation tests discovery only; no agent or domain runtime executed.'})
(ROOT/'docs/audits/DEX_V9_ROUTING_FIXTURES.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print('v9 routing',sum(x['routing_result']=='PASS' for x in results),'/',len(results))

sys.exit(0 if all(x['routing_result']=='PASS' for x in results) else 1)
