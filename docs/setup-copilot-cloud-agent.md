# Setup: Copilot cloud agent

Use repository Copilot settings to make plugins available automatically in the Copilot cloud agent (coding agent).

> 📖 Official docs: [Finding and installing plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) · [Plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)

## Configure the repository

Add this file to your repository at `.github/copilot/settings.json`:

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
    "PLUGIN-NAME@copilot-plugins": true
  }
}
```

## How it works

- The Copilot cloud agent reads the repository's Copilot settings when it starts a session for that repository.
- Any plugins listed in `enabledPlugins` are automatically installed for that session.
- Agents, skills, hooks, and other supported plugin assets are then available to the cloud agent without any manual install step.

## Example

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
    "sdlc-agents@copilot-plugins": true,
    "code-review-standards@copilot-plugins": true
  }
}
```

## Operational notes

- Commit the settings file to the repository so new cloud-agent sessions can read it at startup.
- Existing sessions may need to be restarted to pick up changes.
- You can enable one plugin or many plugins in the same repository settings file.
