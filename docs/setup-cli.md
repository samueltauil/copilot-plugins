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
copilot plugin marketplace browse custom-copilot-plugins
```

## Install a plugin

```bash
copilot plugin install PLUGIN-NAME@custom-copilot-plugins
```

For example:

```bash
copilot plugin install sdlc-agents@custom-copilot-plugins
copilot plugin install git-workflow@custom-copilot-plugins
copilot plugin install testing-toolkit@custom-copilot-plugins
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
    "sdlc-agents@custom-copilot-plugins": true,
    "git-workflow@custom-copilot-plugins": true
  }
}
```

Or per-repository in `.github/copilot/settings.json`:

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
    "sdlc-agents@custom-copilot-plugins": true
  }
}
```

## Troubleshooting

### `Marketplace "copilot-plugins" already registered` or `Plugin "..." not found in marketplace "copilot-plugins"`

This marketplace used to be named `copilot-plugins`, the same name GitHub's own marketplace ([`github/copilot-plugins`](https://github.com/github/copilot-plugins)) uses. The CLI identifies marketplaces by that name, so the two could not be registered together and installs went to GitHub's marketplace instead. The marketplace is now named `custom-copilot-plugins`.

Check what you have registered:

```bash
copilot plugin marketplace list
```

- If you see `copilot-plugins (GitHub: github/copilot-plugins)`, that is GitHub's marketplace. Keep it, then add this one with `copilot plugin marketplace add samueltauil/copilot-plugins` and install plugins as `PLUGIN-NAME@custom-copilot-plugins`.
- If you see `copilot-plugins (GitHub: samueltauil/copilot-plugins)`, you registered this marketplace under its old name. Remove it and add it again, then reinstall your plugins with the new name:

  ```bash
  copilot plugin marketplace remove copilot-plugins --force   # --force also uninstalls plugins installed from it
  copilot plugin marketplace add samueltauil/copilot-plugins
  copilot plugin install PLUGIN-NAME@custom-copilot-plugins
  ```

Update any `enabledPlugins` or `extraKnownMarketplaces` entries in your settings files to use `custom-copilot-plugins` too.
