# Setup: Enterprise / org-wide deployment

Use enterprise-managed Copilot settings to roll out this marketplace and selected plugins across your organization.

> 📖 Official docs: [Plugin marketplaces](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) · [Plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) · [Managing policies for Copilot in your organization](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies)

## Recommended deployment model

Enterprise-managed plugin standards use a `.github-private` repository as the centralized governance source. An enterprise owner selects the organization that owns this repository, and settings in it apply to all users on the enterprise's Copilot plan across CLI, VS Code (1.122+), and cloud agent.

### Setup steps

1. **Create the `.github-private` repository** in one of your enterprise's organizations. You can use the [governance template](https://github.com/docs/custom-agents-template) or create one from scratch. Choose **Internal** visibility to grant read access to all enterprise members, or **Private** to manually control access.

2. **Select the repository as your governance source** in your enterprise settings:
   - Navigate to your enterprise on GitHub.com
   - Click **AI controls** → **Agents** tab
   - In the **Configuration source** section, select the organization that contains your `.github-private` repository

   > ⚠️ **Important:** This step is required and often missed. Creating the `.github-private` repository alone is not enough — you must explicitly select the owning organization as the configuration source in your enterprise's AI controls. Without this, the settings file will not be read and no policies will be applied. See [Selecting your repository as your source of governance](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/create-github-private-repo#selecting-your-repository-as-your-source-of-governance).

3. **Create `copilot/managed-settings.json`** in the repository (the preferred path). The legacy path `.github/copilot/settings.json` is also supported.

4. **Commit and push** to the default branch. Settings are applied automatically within about one hour, or immediately after client restart or sign-in.

> 📖 Official docs: [Creating a `.github-private` repository](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/create-github-private-repo) · [About enterprise-managed plugin standards](https://docs.github.com/en/copilot/concepts/agents/about-enterprise-plugin-standards)

## Baseline configuration

Create `copilot/managed-settings.json` with:

```json
{
  "extraKnownMarketplaces": {
    "custom-copilot-plugins": {
      "source": {
        "source": "github",
        "repo": "samueltauil/copilot-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-review-standards@custom-copilot-plugins": true,
    "git-workflow@custom-copilot-plugins": true,
    "testing-toolkit@custom-copilot-plugins": true
  }
}
```

This makes the `custom-copilot-plugins` marketplace known to managed clients and automatically installs the listed plugins.

## What this applies to

Plugin standards apply to all users on the enterprise's Copilot plan across:

- **Copilot CLI and Copilot cloud agent** — see [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- **VS Code 1.122+** — see [Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins)

Users must be on a supported client version for standards to take effect. When a user authenticates, the client reads the `managed-settings.json` configuration and applies the policies automatically.

## Lock down marketplaces with `strictKnownMarketplaces`

Use `strictKnownMarketplaces` when you want users to install plugins only from approved marketplaces.

Example:

```json
{
  "extraKnownMarketplaces": {
    "custom-copilot-plugins": {
      "source": {
        "source": "github",
        "repo": "samueltauil/copilot-plugins"
      }
    }
  },
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "samueltauil/copilot-plugins"
    }
  ],
  "enabledPlugins": {
    "code-review-standards@custom-copilot-plugins": true,
    "git-workflow@custom-copilot-plugins": true,
    "testing-toolkit@custom-copilot-plugins": true
  }
}
```

When `strictKnownMarketplaces` is set, users are limited to the marketplaces you explicitly approve. This is useful for governance, supply-chain control, and standardization.

## Security hardening with `permissions.disableBypassPermissionsMode`

Bypass mode (also known as "YOLO mode") lets an agent run commands, access files, and fetch URLs without asking the user for approval. While useful for individual productivity, it may not be appropriate in regulated or tightly controlled environments where a human should review each action before it executes.

Enterprise admins can disable bypass mode across all managed clients by adding `disableBypassPermissionsMode` to managed settings:

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}
```

### What this blocks

When set to `"disable"`, users cannot turn on bypass mode in either client:

**Copilot CLI:**
- `--yolo` and `--allow-all` flags are blocked
- `--allow-all-tools`, `--allow-all-paths`, and `--allow-all-urls` flags are blocked
- `/yolo` and `/allow-all` slash commands are blocked

**VS Code:**
- The global auto-approve setting (`chat.tools.global.autoApprove`) is turned off and cannot be re-enabled

Users can still approve individual tool calls, file accesses, and URL fetches one at a time — only the blanket "approve everything" modes are disabled.

### When to use this

- **Regulated environments** where audit trails require explicit human approval of each action
- **Shared development infrastructure** where agents running unreviewed commands could affect other users
- **Security-sensitive codebases** where you want to prevent accidental execution of destructive operations
- **Onboarding** where newer developers should review what the agent is doing

### Combining with marketplace restrictions

For maximum control, combine bypass mode restrictions with strict marketplace controls so that users can only install approved plugins _and_ must approve each action those plugins trigger:

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  },
  "extraKnownMarketplaces": {
    "custom-copilot-plugins": {
      "source": {
        "source": "github",
        "repo": "samueltauil/copilot-plugins"
      }
    }
  },
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "samueltauil/copilot-plugins"
    }
  ],
  "enabledPlugins": {
    "code-review-standards@custom-copilot-plugins": true,
    "git-workflow@custom-copilot-plugins": true
  }
}
```

> 📖 Official docs: [Disabling bypass mode for your enterprise](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/configure-enterprise-managed-settings#disabling-bypass-mode-for-your-enterprise) · [Enterprise managed settings reference](https://docs.github.com/en/copilot/reference/enterprise-managed-settings-reference)

## Deployment methods

All three methods use the same `managed-settings.json` schema. They differ in where the file lives and how it reaches the client. Settings are applied in order of precedence: MDM > server-managed > file-based > user-level.

| Method | Where the file lives | Best for |
|--------|---------------------|----------|
| **Server-managed** | `.github-private` repo → `copilot/managed-settings.json` | Most orgs — no device management needed, uses GitHub's built-in distribution |
| **MDM-managed** | Deployed via Jamf, Intune, or Group Policy | Orgs already using MDM for device-level enforcement (macOS/Windows) |
| **File-based** | Placed on disk via config management (Ansible, Chef, etc.) | Containers, Codespaces, Linux, or any environment without MDM or server access |

Settings apply within ~1 hour or immediately after client restart.

> 📖 Official docs: [Configuring enterprise-managed settings](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/configure-enterprise-managed-settings#choosing-a-deployment-method)

## Rollout recommendations

1. Start with `extraKnownMarketplaces` + a small `enabledPlugins` set to validate the flow.
2. Add `strictKnownMarketplaces` when you're ready to lock installation to approved sources only.
3. Add `permissions.disableBypassPermissionsMode` for regulated or security-sensitive environments.
4. Use the same plugin names across CLI, VS Code, and cloud-agent settings for consistency.
