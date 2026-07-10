# Setup: Copilot CLI

## Prerequisites

- GitHub Copilot CLI installed and authenticated
- A Copilot Business or Enterprise license

> 📖 Official docs: [Finding and installing plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) · [Plugin marketplaces](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)

## Add the marketplace

```bash
copilot plugin marketplace add samueltauil/copilot-plugins
```

Or in an interactive session:

```
/plugin marketplace add samueltauil/copilot-plugins
```

## Browse available plugins

```bash
copilot plugin marketplace browse copilot-plugins
```

## Install a plugin

```bash
copilot plugin install PLUGIN-NAME@copilot-plugins
```

For example:

```bash
copilot plugin install sdlc-agents@copilot-plugins
copilot plugin install git-workflow@copilot-plugins
copilot plugin install testing-toolkit@copilot-plugins
```

## Verify installation

```bash
copilot plugin list
```

Start an interactive session and check that agents and skills loaded:

```
/agent
/skills list
```

## Manage plugins

```bash
copilot plugin update PLUGIN-NAME      # Update to latest version
copilot plugin update --all            # Update all plugins
copilot plugin disable PLUGIN-NAME    # Temporarily disable
copilot plugin enable PLUGIN-NAME     # Re-enable
copilot plugin uninstall PLUGIN-NAME  # Remove completely
```

## Declarative installation (settings.json)

Instead of installing imperatively, you can declare plugins in `~/.copilot/settings.json`:

```json
{
  "enabledPlugins": {
    "sdlc-agents@copilot-plugins": true,
    "git-workflow@copilot-plugins": true
  }
}
```

Or per-repository in `.github/copilot/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "copilot-plugins": {
      "source": {
        "source": "github",
        "repo": "samueltauil/copilot-plugins"
      }
    }
  },
  "enabledPlugins": {
    "sdlc-agents@copilot-plugins": true
  }
}
```
