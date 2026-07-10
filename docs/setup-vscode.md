# Setup: VS Code

## Prerequisites

- Visual Studio Code 1.122 or later
- GitHub Copilot and GitHub Copilot Chat enabled for your account
- A Copilot Business or Enterprise license

> 📖 Official docs: [Finding and installing plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) · [Plugin marketplaces](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)

## Important note

VS Code plugin support requires `chat.plugins.enabled` to be managed at the organization level. If you do not see plugin settings or marketplace actions, contact your Copilot admin and ask them to enable `chat.plugins.enabled`.

## Enable plugin support

1. Open **Settings** in VS Code.
2. Search for `chat.plugins.enabled`.
3. Confirm that the setting is enabled for your organization.

If your admin asks you to verify it in JSON-managed settings, the relevant flag is:

```json
{
  "chat.plugins.enabled": true
}
```

## Add the marketplace

### Option 1: Command Palette

1. Open the Command Palette.
2. Run **Copilot: Add Plugin Marketplace**.
3. Enter:

```text
samueltauil/copilot-plugins
```

### Option 2: Managed settings

If your organization manages marketplaces through Copilot settings, add:

```json
{
  "extraKnownMarketplaces": {
    "copilot-plugins": {
      "source": {
        "source": "github",
        "repo": "samueltauil/copilot-plugins"
      }
    }
  }
}
```

## Install plugins

After the marketplace is available:

1. Open Copilot Chat.
2. Open the plugin marketplace or plugin management UI.
3. Browse the `copilot-plugins` marketplace.
4. Install the plugins you want, such as:
   - `sdlc-agents`
   - `git-workflow`
   - `testing-toolkit`

## Verify agents and skills

After installation:

1. Open a new Copilot Chat session.
2. Check the chat agent picker and confirm plugin-provided agents appear.
3. Start a task that matches one of the installed plugins and confirm the related skills appear or are invoked in chat.

If the new agents or skills do not appear right away, reload the VS Code window and open a fresh chat session.

## Notes

- Marketplace and plugin settings can be managed centrally by your organization.
- Organization-managed settings are the preferred deployment model for teams using VS Code at scale.
- The same marketplace can also be enabled for the Copilot CLI and Copilot cloud agent using Copilot settings files.
