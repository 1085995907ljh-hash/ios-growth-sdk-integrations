# iOS Growth SDK Integrations

A portable [Agent Skill](https://agentskills.io/specification) for integrating
**RevenueCat, Firebase / Crashlytics, Mixpanel, and AppsFlyer** into native iOS
Swift and SwiftUI apps. Use one provider or the complete stack.

Works with Codex and other coding agents that load the Agent Skills format.
No proprietary MCP server or paid agent plugin is required. Your app still needs
the relevant provider accounts/configuration; building iOS requires macOS/Xcode.
Installing the skill does not install the four SDKs.

## Install

With the [Skills CLI](https://github.com/vercel-labs/skills), select your agent:

```bash
npx skills add 1085995907ljh-hash/ios-growth-sdk-integrations --skill ios-growth-sdk-integrations
```

For a global Codex installation:

```bash
npx skills add 1085995907ljh-hash/ios-growth-sdk-integrations --skill ios-growth-sdk-integrations -a codex -g
```

For Claude Code, choose `-a claude-code`. Select other supported agents in the CLI.
Follow the CLI's current Node.js requirements.

### Manual download

Download the ZIP via GitHub's **Code → Download ZIP**, or clone:

```bash
git clone https://github.com/1085995907ljh-hash/ios-growth-sdk-integrations.git
```

Copy the extracted folder, named `ios-growth-sdk-integrations`, to the agent's
skill directory. Keep `SKILL.md`, `references/`, `scripts/`, and `agents/`
together. Review changes before replacing an existing custom skill.

- Codex: `~/.agents/skills/ios-growth-sdk-integrations/` for user scope, or
  `.agents/skills/ios-growth-sdk-integrations/` in a project. Existing setups may
  also use `~/.codex/skills/`; follow your installed client's guidance.
- Claude Code: `~/.claude/skills/ios-growth-sdk-integrations/` or a project's
  `.claude/skills/ios-growth-sdk-integrations/`.
- Other agents: use the tool's documented location. The tool must support skill
  discovery or be explicitly instructed to read the local `SKILL.md`.

Reload the agent/start a new session if the skill is not discovered.

## Use

In Codex:

```text
Use $ios-growth-sdk-integrations to audit this iOS app and integrate RevenueCat,
Crashlytics, Mixpanel, and AppsFlyer. Keep config ignored by Git and identify
missing inputs before implementing dependent steps.
```

Other examples:

```text
Use the ios-growth-sdk-integrations skill to add only Mixpanel. Keep our EU
region and existing consent flow.

Use the ios-growth-sdk-integrations skill to debug empty RevenueCat offerings
and verify restore without changing our subscription products.

Use the ios-growth-sdk-integrations skill to swap authorized test configuration
for production configuration and report remaining release checks.
```

中文调用示例：

```text
使用 $ios-growth-sdk-integrations 检查这个 iOS 项目，接入 RevenueCat、
Firebase Crashlytics、Mixpanel 和 AppsFlyer。先读产品文档，设计必要埋点，
配置放在不提交 Git 的本地文件里，说明已验证和未验证的部分。
```

## Coverage

| Provider | Focus |
| --- | --- |
| RevenueCat | Offerings, purchases, restore, entitlements |
| Firebase | Requested products, plist/target, Crashlytics symbols |
| Mixpanel | Funnels, bounded properties, region and identity |
| AppsFlyer | Attribution, lifecycle, marketing milestones, revenue ownership |

Includes missing-input dialogue, event planning, consent-aware integration,
configuration replacement, and evidence-based handoffs. A successful build is
distinguished from provider receipt and real-device validation.

## Optional local audit

From the skill folder:

```bash
python3 scripts/audit_ios_growth_integrations.py /path/to/your/app
```

Requires **Python 3.9+**, without third-party Python packages. On Windows, use
`py -3` if that is your interpreter command. A Bash wrapper remains for existing
callers and requires Bash plus `python3`.

The helper reads authored sources and reports relative paths/symbol counts, not
source lines/config values. It does not modify files, invoke Git/Xcode, contact
providers, or upload anything. It skips symlinks, generated dependencies, and
oversized sources. This is a heuristic inventory, not a credential scanner or
proof of correct configuration. File paths can be sensitive; review before sharing.

## Development and limits

```bash
python3 -m unittest discover -s tests -v
```

Tests cover helper output privacy and inventory behavior. They do not establish
SDK delivery, purchases, consent compliance, or release readiness. Read the
linked official provider docs for current APIs. Never put real keys, service
plists, or customer data in issues/PRs.

An independent community skill, not an official SDK or endorsement by OpenAI,
Apple, or the providers. MIT licensed; see [LICENSE](LICENSE).
