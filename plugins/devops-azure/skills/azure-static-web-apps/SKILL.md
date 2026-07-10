---
name: Azure Static Web Apps deployment
description: Use this skill when you need to create, deploy, validate, or troubleshoot Azure Static Web Apps with GitHub Actions and Azure integrations.
---

# Azure Static Web Apps deployment

## Use this skill when
- You are setting up or maintaining an Azure Static Web Apps deployment pipeline.
- A frontend app needs preview environments, custom domains, authentication, or an API backend.
- You need to debug build, routing, or environment configuration issues before release.

## Gather deployment inputs first
1. Identify the app framework, build output folder, package manager, and Node/runtime version.
2. Confirm whether the app includes an Azure Functions API or another backend.
3. Capture the target Azure region, resource group, repo, branch strategy, and environment secrets.

## Provisioning guidance
- Create the Static Web App resource with the correct subscription, region, and deployment source.
- Use GitHub Actions integration when you want automated preview and production deployments.
- Store the deployment token, app settings, and environment secrets in GitHub securely.
- Keep environment-specific values out of client-side bundles unless they are intentionally public.

## GitHub Actions expectations
- Trigger preview environments on pull requests and production deployments on the protected main branch.
- Cache dependencies and pin action versions to reduce build variability.
- Fail the workflow when install, build, test, or artifact path validation fails.
- Publish logs that clearly show the detected app location, output folder, and API location.

## Routing and frontend configuration
- Maintain `staticwebapp.config.json` for routes, navigation fallback, headers, and auth behavior.
- Verify SPA fallback does not mask real 404s for asset requests.
- Add security headers, cache-control, and role-based route protection where needed.
- Test rewrites, redirects, and localized routes in both preview and production environments.

## API backend integration
- Keep API and frontend contracts versioned together when the backend lives in the same app.
- Validate function auth level, CORS behavior, and environment variables for the API.
- Use staging data or safe mocks for preview environments if production dependencies are restricted.
- Confirm cold-start or timeout behavior on workflows that call the backend.

## Custom domains and authentication
- Verify DNS records, certificate provisioning, and domain ownership before cutover.
- Test login flows for each configured provider and role assignment path.
- Check callback URLs, logout URLs, and protected route behavior in every environment.
- Document the rollback path if domain or identity configuration fails after deployment.

## Troubleshooting checklist
- Confirm the workflow used the expected app and API directories.
- Check for runtime mismatches, missing environment variables, or unsupported build steps.
- Inspect generated files for base path, asset URLs, and client-side routing assumptions.
- Compare preview versus production settings when bugs reproduce in only one environment.

## Deliverable format
- Summarize resource setup, workflow triggers, and configuration files.
- Call out domain, auth, and backend dependencies.
- List preflight checks and post-deploy validation steps.
- End with exact fixes or deployment commands to apply.
