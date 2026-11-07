# Gathering inputs

Inspect the app before asking. Read identifiers from authorized files/screenshots
locally without echoing values. Continue work independent of missing credentials.

## RevenueCat

Start with the public platform SDK key and intended entitlement/offering. Infer
product/package identifiers from supplied catalog evidence. Ask about plans,
trials, free access, and restore entry points only when product docs do not decide
them. Display names and dashboard REST IDs are not necessarily SDK identifiers.
Never request a secret RevenueCat API key for client SDK initialization.

## Firebase

Request the service plist for the target/environment and the specific Firebase
products. Compare its bundle ID locally. Do not invent a plist. A mismatch blocks
that configuration. Crashlytics does not imply Firebase Analytics.

## Mixpanel

Request token and data region; honor existing residency requirements. Use US only
when confirmed. Determine anonymous tracking, consent, login, account switching,
and logout behavior. Do not introduce email addresses as analytics IDs by default.

## AppsFlyer

Request Dev Key and Apple App ID. Read bundle ID from Xcode; remove a leading `id`
from the Apple App ID. Determine standard/Strict requirements. If advertising
identifiers or tracking are in scope, clarify collection policy first; do not
bypass consent or add ATT automatically. Decide who owns purchase revenue.

## Storage

Follow authorized conventions. Otherwise prefer ignored local config and a
tracked placeholder example. Confirm ignore rules before staging. Keep real
service plists/project identifiers out of public examples. Never embed server or
admin credentials, or ask users to put credentials in public issues/shared logs.

## Handoff example

"The app builds and launches with the requested SDKs. Sandbox offerings and
restore were verified. Mixpanel receipt and real-device attribution remain
unverified. Configuration stays in ignored local config; committed examples use
placeholders."

Use this form only when each claim has evidence. Name missing inputs without
repeating supplied values.
