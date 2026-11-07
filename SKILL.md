---
name: ios-growth-sdk-integrations
description: Integrate, audit, debug, or replace configuration for RevenueCat subscriptions, Firebase and Crashlytics, Mixpanel analytics, and AppsFlyer attribution in native iOS Swift or SwiftUI apps. Use for one provider or the full growth stack, event planning, sandbox validation, and production configuration swaps.
license: MIT
metadata:
  version: "1.0.0"
---

# iOS Growth SDK Integrations

Help an existing iOS app measure activation, sell subscriptions, diagnose crashes,
and attribute acquisition. Support only requested providers. Installing this skill
does not install SDKs or configure vendor accounts.

## Boundaries

- Read repository instructions, product requirements, existing integration code,
  dependencies, and Git status first. Preserve the app's architecture, deployment
  target, event contracts, identity model, and consent controls.
- Use official SDKs. Before selecting versions or APIs, consult current official
  documentation linked in [provider-checklists.md](references/provider-checklists.md).
  Do not upgrade unrelated dependencies. Identify unverified APIs if docs are unavailable.
- Reuse existing authorization to store configuration. If unspecified, prefer an
  ignored local config and tracked placeholder example. Never publish real project
  keys, tokens, service plists, or account data; do not echo configuration values.
  Client SDK configuration differs from privileged server/admin credentials;
  never embed server credentials in an app.
- Keep purchases and entitlements separate from analytics. Reuse the app's local
  facade where practical so UI views do not depend directly on four SDKs.
- Apply the app's consent and collection policy to initialization, queued events,
  automatic collection, identity changes, and logout. Do not add ATT prompts,
  advertising identifiers, or session replay by default.
- Do not send photos, files, paths, raw user text, prompts/responses, receipts,
  arbitrary provider payloads, or other private content to general analytics.
- Local implementation does not authorize account creation, dashboard mutation,
  purchases, deployment, or release. Obtain missing authorization for the specific
  external action while continuing independent local work.

## Audit

Locate entry points, targets/schemes, bundle IDs, paywall/restore flows,
entitlements, identity, consent controls, and dependency versions. An optional
read-only helper reports relative file paths and symbol counts, not source lines
or config values:

```bash
python3 <skill-directory>/scripts/audit_ios_growth_integrations.py <app-repository>
```

Resolve `<skill-directory>` from this skill's installation location. The helper
requires Python 3.9+. It does not prove initialization, target membership, or
event delivery; inspect relevant files locally afterward.

## Inputs and product decisions

Read [integration-dialogue.md](references/integration-dialogue.md) when collecting
inputs. Infer identifiers from authorized files or supplied screenshots. Ask only
for missing inputs or decisions that materially change the result.

| Provider | Inputs | Role |
| --- | --- | --- |
| RevenueCat | Public SDK key, entitlement/offering identifiers, product decisions | Purchase, restore, subscription access |
| Firebase | Environment's service plist and requested Firebase products | Requested capabilities such as Crashlytics |
| Mixpanel | Project token, region, identity/collection policy | Product funnels and retention |
| AppsFlyer | Dev Key, numeric Apple App ID, attribution scope | Acquisition and marketing milestones |

Do not assume US residency, a paid tier named Pro, trial availability, or a login
requirement. Missing credentials can leave a provider explicitly unconfigured
while its local boundary is implemented. Never fabricate configuration values.

## Event ownership

Use [mvp-event-taxonomy.md](references/mvp-event-taxonomy.md) to derive a small
event plan from the app's first-value journey. Record name, trigger, allowed
properties, destination, consent requirement, and deduplication. Preserve existing
event names unless a migration is requested.

Mixpanel normally owns product behavior; AppsFlyer owns attribution milestones.
Only add Firebase Analytics if requested. Assign one owner for revenue delivery
(client, RevenueCat integration, or server) to avoid duplicate purchase revenue.

## Implement requested providers

Read the relevant sections of [provider-checklists.md](references/provider-checklists.md).

- **RevenueCat:** initialize once, fetch offerings, display returned localized
  prices/eligibility, implement purchase/restore, and derive access from active
  entitlements. Handle cancellation, pending transactions, empty offerings,
  offline state, and account changes without false success.
- **Firebase:** add only requested products and the correct target's service
  plist once. Match bundle IDs, preserve existing initialization, and configure
  symbol upload for Crashlytics when requested.
- **Mixpanel:** route events to the chosen region through the app's analytics
  boundary. Define anonymous/identified and logout behavior. Apply consent to
  automatic collection and initialization as well as explicit events.
- **AppsFlyer:** normalize `id123` to `123`. Choose standard or Strict deliberately;
  wire lifecycle startup without duplicate starts. Follow identifier and consent
  requirements, and never assume Strict exposes IDFA APIs. Emit agreed milestones.

Enable diagnostic logging only in development. Avoid logging content or config
values. Check behavior against the installed SDK version.

## Verification and handoff

Run checks proportionate to the change. Use focused tests for changed entitlement
logic, privacy filtering, identity transitions, or revenue deduplication. Discover
the app's actual workspace/project, scheme, Xcode, and available simulator; do not
hardcode a developer's Xcode path or device model.

Distinguish:

1. **Local wiring:** configuration loading, build, and launch evidence.
2. **Provider delivery:** returned offerings, sandbox purchase/restore, received
   events, or a Crashlytics test report observed in the appropriate dashboard.
3. **Release checks:** production environment, consent/identity flows, symbols,
   real-device attribution, and account/dashboard prerequisites.

A build alone is not end-to-end verification. Purchases require appropriate
StoreKit/sandbox setup; attribution generally needs a real test device. Before a
test crash, confirm an authorized disposable debug session. Report evidence,
blockers, and checks not run without exposing configuration values.

## Configuration replacement

Preserve the integration design when swapping test/production configuration.
Verify target/environment and RevenueCat identifiers, replace only authorized
configuration, then rerun affected checks. Report file locations and validation
results, not values. A swap alone does not establish production readiness.
