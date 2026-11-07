# Provider checklists

Consult current official docs before selecting versions/APIs. These are decision
and evidence checklists, not pinned installation recipes. Preserve the existing
package manager unless migration is requested.

## RevenueCat

Official sources: [Apple installation](https://www.revenuecat.com/docs/getting-started/installation/ios),
[configuration](https://www.revenuecat.com/docs/getting-started/configuring-sdk).

- Use a public platform SDK key; initialize once.
- Resolve offering, package/product, and entitlement IDs independently.
- Show returned localized prices and confirmed eligibility; handle empty offerings
  without inventing plans or prices.
- Grant access from active entitlements. Cancellation of auto-renewal does not
  necessarily end current access immediately.
- Handle pending, cancelled, failed, and restored purchases, offline state, and
  account changes. Follow the app's identity policy for login/logout.
- Verify offerings and CustomerInfo separately from purchase/restore. Distinguish
  local StoreKit, sandbox, and production evidence.

## Firebase / Crashlytics

Official sources: [Apple setup](https://firebase.google.com/docs/ios/setup),
[Crashlytics](https://firebase.google.com/docs/crashlytics/get-started?platform=ios),
[symbolication](https://firebase.google.com/docs/crashlytics/get-deobfuscated-reports?platform=ios).

- Add only requested products. Check target membership, resource name, build
  configuration, and bundle ID; avoid duplicate plist copy steps.
- Preserve existing initialization; do not configure the default app twice.
- Follow current Xcode/SDK symbol-upload build-script input guidance when using
  Crashlytics, and respect collection controls.
- A bundled plist/build/startup log is not proof of crash delivery. Verify a
  symbolicated test report separately.
- Only cause a test crash in an authorized disposable debug session. Follow
  documented debugger disconnect/relaunch steps when checking receipt.

## Mixpanel

Official source: [Swift SDK](https://docs.mixpanel.com/docs/tracking-methods/sdks/swift).

- Set the correct token and region. Review automatic events, persisted queues,
  and initialization against the app's consent policy.
- Keep bounded event construction behind the app's analytics interface; filter
  private/free-form payloads before dispatch.
- Define anonymous/identified, account-switch, and reset/logout behavior.
- Verify a permitted test event in the intended project's dashboard. An attempted
  send in debug logs does not prove receipt.
- Do not add session replay, profiles, or revenue forwarding implicitly.

## AppsFlyer

Official sources: [installation](https://dev.appsflyer.com/hc/docs/install-ios-sdk),
[integration](https://dev.appsflyer.com/hc/docs/integrate-ios-sdk),
[events](https://dev.appsflyer.com/hc/docs/in-app-events-ios).

- Supply Dev Key and numeric Apple App ID; strip a leading `id` if supplied.
- Choose standard/Strict using the project's requirements and current docs.
  Confirm actual package products/module names and available APIs; never assume
  Strict supports IDFA selectors.
- Wire initialization/start to lifecycle deliberately. Avoid duplicate starts
  from SwiftUI and AppDelegate paths.
- Apply collection policy before identifier access or deferred startup. Do not
  insert ATT/SKAN configuration speculatively.
- Use documented standard constants or explicit custom milestones. Verify one
  revenue owner and no duplicate purchase reporting.
- Build/launch proves wiring. Check vendor test-device/session/attribution flows
  on a real device before claiming end-to-end attribution.

## Build and report

Discover the actual installed Xcode, project/workspace, scheme, and simulator.
Use the repository's own commands. Example template:

```bash
xcodebuild -workspace <App>.xcworkspace -scheme <Scheme> \
  -destination 'platform=iOS Simulator,id=<available-simulator-id>' build
```

Use `-project` for a project-only app. Test changed business logic where warranted.
Without macOS/Xcode, inspect sources/configuration and leave build/runtime checks
explicitly unverified. Report changed paths, versions, checks, provider evidence,
missing configuration, and remaining device/dashboard validation. Redact values.
