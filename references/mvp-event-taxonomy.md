# MVP event planning

Choose the smallest set that answers actual product questions. These are
examples, not a required catalog. Preserve existing names; otherwise `snake_case`
is a reasonable default.

| Question | Example events | Properties |
| --- | --- | --- |
| Does onboarding reach first value? | `onboarding_completed`, `core_action_completed`, `first_value_shown` | stable flow/source IDs |
| Where does work fail? | `input_failed`, `core_action_failed`, `save_failed` | bounded error category, duration bucket |
| Does the result help? | `result_viewed`, `item_saved`, `item_shared` | count or count bucket |
| Does the user return? | `library_opened`, `history_item_opened` | source, environment |
| Does paid access work? | `paywall_viewed`, `purchase_started`, `purchase_completed`, `purchase_cancelled`, `purchase_failed`, `restore_completed` | offering/product ID, bounded outcome |

Define each event's trigger, destination, allowed properties, consent state, and
deduplication. A tap is not completion. Pending/cancelled purchases are not sales.
A restored transaction or refreshed entitlement is not a new sale.

## Properties

- Use stable IDs and bounded categories rather than raw errors/user text.
- Prefer duration/count buckets where exact values do not serve a defined metric.
- Include environment/version and entitlement state when useful.
- Exclude filenames, paths, media metadata, contact details, raw text, prompts,
  responses, receipts, and arbitrary SDK payloads.
- Treat campaign/source fields as potentially sensitive. Select intentionally;
  never copy the whole attribution payload to another provider.

## Attribution and revenue

Keep AppsFlyer milestones minimal: onboarding, first core action, paywall, and
confirmed purchase when needed. Check current docs for standard event constants.
Label custom events explicitly; do not invent `af_*` names and call them standard.

Assign one revenue owner: client, RevenueCat integration, or server. For multiple
reporters, verify documented deduplication at the transaction boundary. Do not
put receipt/transaction payloads into general analytics properties by default.
Separate a purchase outcome event from monetary reporting; use documented
revenue/currency fields when revenue reporting is requested.

## App-specific mapping

- Media: input is capture/import; first value may be a useful preview or export.
- Utility: input is a form/file; first value is a successful scan/conversion.
- Content: first value may be reading, saving, or sharing relevant content.
- AI: first value is a usable result, not just starting inference.

Do not automatically collect all examples or rename existing app events.
