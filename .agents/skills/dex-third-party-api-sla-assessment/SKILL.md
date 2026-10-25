---
name: dex-third-party-api-sla-assessment
description: "Assess a third-party API dependency and fallback strategy."
---

# dex-third-party-api-sla-assessment

## 1. Purpose & Scope
Dependency reliability only; avoid inferring guaranteed reliability from a status page.

## 2. When to Use
- Before adding a new vendor API to checkout, payments, auth, messaging, or search paths.
- When an existing provider misses latency targets, returns elevated 429/5xx, or changes rate limits and deprecation policy.
- During renewal or tier change to validate whether the contracted SLA supports the product SLO.

## 3. When NOT to Use
- When the dependency is first-party or self-hosted infrastructure under direct operational control.
- When the task is functional integration or SDK wiring without reliability, quota, or failover implications.
- When no fallback, cache, queue, or degraded mode is feasible and the decision is already forced.

## 4. Prerequisites & Input Context
- **Contract inputs:** MSA/SLA excerpt, support tier, RTO/RPO claims, scheduled maintenance windows, rate-limit and quota tables, deprecation notice period.
- **Technical inputs:** Endpoint inventory with criticality, traffic shape (RPS, burst, geographic mix), caller timeout and retry policy, client telemetry for 14-30 days.
- **Business inputs:** Revenue or activation impact per minute of outage, acceptable degraded behavior, data residency constraints, escalation contacts and on-call path.

## 5. Core Concepts & Taxonomy
- **Contractual SLA vs observed SLO:** Contract defines credits and exclusions; observed availability and p50/p95/p99 latency define what users actually experience.
- **Success denominator:** Count every caller attempt including timeouts and client-side cancellations, not only provider-acknowledged requests.
- **Measurement window and exclusions:** Align monthly versus rolling windows and subtract only documented maintenance; provider-reported uptime is not ground truth.
- **Correlated failure budget:** Retries, failover, and cache must fit inside the end-to-end caller deadline and assume the backup path may degrade simultaneously.

## 6. Step-by-Step Execution Workflow
1. Inventory the dependency surface: list endpoints, auth method, quota headers, webhook callbacks, and classify each as critical, degradable, or deferrable.
2. Extract the commercial terms into a comparison table: stated availability, exclusions, credit remedy, support response time, rate limits, and termination rights.
3. Build a baseline from caller-side telemetry: compute availability by endpoint, p50/p95/p99 latency by region and hour, timeout rate, 429 rate, and retry amplification factor.
4. Run controlled failure fixtures in staging with a recorded cassette or sandbox: hard timeout, 429 with Retry-After, 500 burst, malformed payload, and slow-drip response exceeding caller deadline.
5. Validate the fallback design under load: verify cache TTL and staleness flag, queued-write replay idempotency, read-only degraded mode, and secondary provider switch with DNS or config flag.
6. Document findings, residual risks, and owners in a decision record before changing production wiring.

## 7. Concrete Examples
A 99.9% monthly SLA allows ~43 minutes of downtime per month and typically excludes beta endpoints, client errors, and upstream ISP issues.

```yaml
dependency: payments-authorize
contract_sla: 99.9% monthly, excl. scheduled maintenance
observed_30d:
  availability: 99.94%
  p95_latency_ms: 820
  timeout_rate: 0.18%
  rate_limit_429_rate: 0.42%
caller_budget:
  deadline_ms: 1200
  retries: 1 with 300ms backoff + jitter
  fallback: cached risk-score + queued capture, stale flag shown
verdict: accept with bounded fallback; alert on p95 > 1000ms for 10m
```

Check commands:

```bash
curl -sS -o /dev/null -w "code=%{http_code} time=%{time_total}s\n" https://api.vendor.example/v1/health
curl -sS -D headers.txt https://api.vendor.example/v1/authorize -H "Authorization: Bearer $VENDOR_TOKEN" | head -n 20
grep -i "ratelimit\|retry-after\|x-quota" headers.txt || echo "QUOTA_HEADERS_MISSING"
test -f scripts/slo_baseline.py && python3 scripts/slo_baseline.py --input telemetry/caller_logs.jsonl --window 30d --percentiles 50,95,99 || echo "TOOL_NOT_AVAILABLE: scripts/slo_baseline.py (if present; otherwise report TOOL_NOT_AVAILABLE)"
k6 run load/vendor-fallback-test.js --vus 20 --duration 5m
```

## 8. Anti-Patterns & Common Traps
- Treating a green status page as proof the SLO is met without caller-side measurement.
- Adding unbounded retries that amplify a provider incident into caller exhaustion and quota burn.
- Caching error responses or serving stale priced inventory without an explicit staleness indicator.
- Assuming failover is instant while DNS TTL, connection pools, and warmup keep traffic pinned to the failing endpoint.
- Ignoring `Retry-After` and quota headers, then hard-coding sleep intervals that violate provider policy.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Availability and p95/p99 are computed from caller logs with stated window, denominator, and exclusion handling.
- QG-02: Timeout, 429, and 5xx fixtures have recorded expected versus actual behavior and fallback outcome.
- QG-03: Fallback path is exercised end-to-end with measured switchover time and data-loss or staleness bound.
- QG-04: Escalation owner, vendor ticket path, and rollback flag are named; open uncertainties are listed explicitly.

## 10. Security & Safety Boundaries
- Use sandbox keys and synthetic customer records; never replay production PII through vendor staging endpoints.
- Keep credentials out of logs and shell history; load tokens from environment or secret store only.
- Run load and chaos fixtures against staging or a recorded double first; cap production probes to documented synthetic checks.
- Review outbound payloads for over-collection before enabling fallback logging.

## 11. Platform Adapters
- **HTTP clients:** Enforce connect timeout, read timeout, and deadline propagation; log `Retry-After`, `X-RateLimit-Remaining`, and `X-Request-Id` on every call.
- **Queues and workers:** Persist vendor writes with idempotency keys so replay after outage does not double-charge or double-send.
- **Observability:** Emit `vendor.request.{success,timeout,rate_limited,server_error}` counters and latency histograms labeled by endpoint and region.
- **Tooling fallback:** If a checker is unavailable, record it as TOOL_NOT_AVAILABLE and mark dependent assertions as NOT_VERIFIED.

## 12. Deliverables & Output Artifacts
1. SLA assessment memo with contract-vs-observed table, latency and error baseline, and accept/mitigate/reject recommendation.
2. Fallback runbook: trigger conditions, switch procedure, rollback flag, verification query, and customer communication template.
3. Reproduction pack: fixture scripts, k6 or curl transcripts, baseline query, and raw output excerpts with versions and timestamps.
4. Risk register: unresolved gaps, monitoring TODOs, renewal negotiation points, and named owners.

## 13. Related & Complementary Skills
- [`dex-api-circuit-breaker-verification`](.agents/skills/dex-api-circuit-breaker-verification/SKILL.md) - Verifies breaker thresholds and half-open recovery around the assessed vendor endpoint.
- [`dex-rate-limiting-quotas`](.agents/skills/dex-rate-limiting-quotas/SKILL.md) - Designs client-side throttling to stay within the provider quota found during assessment.
- [`dex-production-monitoring`](.agents/skills/dex-production-monitoring/SKILL.md) - Turns the baseline SLOs into alerts and dashboards for ongoing vendor tracking.
- [`dex-third-party-attribution`](.agents/skills/dex-third-party-attribution/SKILL.md) - Captures license and attribution obligations when the vendor SDK is bundled.

## 14. Realistic Usage Example
A checkout team depends on a fraud-scoring API with a claimed 99.95% SLA but sees intermittent 1.8s stalls at peak. Assessment of 30 days of caller logs shows 99.91% availability and p95 of 940ms against a 1100ms checkout deadline. Staging fixtures confirm the client retried twice without honoring `Retry-After`, doubling 429s. The fix limits retries to one with jittered backoff, adds a 6-hour cached score with a visible review flag, and queues edge cases for manual review. Switchover drill completes in 47 seconds with no duplicate charges, and the vendor tier is renegotiated to include a 60-day deprecation notice.
