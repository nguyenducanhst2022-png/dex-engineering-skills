# v9 routing evaluation
Existing lexical simulator: 40 legacy scenarios, reported F1 0.927, precision 92.50%, recall 92.92%. Its permissive PASS criterion accepts partial expected selections; see DEX_V9_ROUTING_RAW.txt.

Added 16 A?P fixtures with task input, expected and forbidden selection, tools, execution steps, expected/actual output and limitations. Strict result: 15 PASS, 1 FAIL. Scenario N selected existing upstream-sync/license/import skills but missed the expected provenance-revalidation specialist. The evaluator exits nonzero for that failure. See DEX_V9_ROUTING_FIXTURES.json.

This is metadata-based lexical simulation, not observation of the master agent choosing and executing skills. Domain executions and independent held-out semantic evaluations remain NOT_VERIFIED. The failing case is retained rather than tuning the expected answer to inflate the score.
