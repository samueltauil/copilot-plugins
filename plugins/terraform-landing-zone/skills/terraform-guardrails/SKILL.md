---
name: terraform-guardrails
description: Azure landing zone Terraform guardrails — naming conventions, module patterns, policy compliance
---

Use this skill when authoring, editing, or reviewing Terraform for an Azure landing zone that governs a brownfield Azure estate.

# Azure landing zone context

This environment is managed by a small central infrastructure team. Guardrails are enforced through Terraform, Copilot review, and GitHub Actions so the team does not become a manual bottleneck.

## Stack

- Terraform `>= 1.9`
- `azurerm ~> 4.20`
- `azapi ~> 2.2`
- `random ~> 3.6`
- Remote state in Azure Storage authenticated via OIDC federation
- CI runs `fmt`, `validate`, `tflint`, `checkov`, and `terraform plan` on every PR
- A scheduled `drift.yml` workflow opens a GitHub Issue when `terraform plan -detailed-exitcode` reports drift

## Repository conventions

- Use one file per logical area: `main.tf`, `network.tf`, `storage.tf`, `imports.tf`, `variables.tf`, `outputs.tf`, `providers.tf`
- Read `providers.tf`, `variables.tf`, and the target file before editing
- Use `local.required_tags` for tags; do not inline literal tag maps unless preserving live brownfield values during import
- Approved regions: `eastus2`, `centralus`
- Naming must follow Microsoft CAF abbreviations such as `rg-`, `vnet-`, `snet-`, `nsg-`, `st`, `log-`, `kv-`, `pe-`
- For brownfield adoption, use `import {}` blocks in `imports.tf`, never the `terraform import` CLI

## Hard rules

- Never run `terraform apply` from CI or from an agent; PRs are plan-only
- Never remove the remote backend or switch to `backend "local"`
- Never introduce `public_network_access_enabled = true`, shared access keys, SAS tokens, connection strings, or inbound NSG rules allowing `0.0.0.0/0`
- If a request conflicts with the landing-zone policy below, follow the policy and explicitly flag the conflict

# Landing-zone policy

## Naming and regions

- **LZ-REG-01** Approved regions only: `eastus2`, `centralus`
- **LZ-NAME-01** Resource names must follow `<type-prefix>-<workload>-<env>[-<suffix>]` using Microsoft CAF abbreviations

## Required tags

- **LZ-TAG-01** Every taggable resource must include `environment`, `owner`, `cost-center`, `data-class`, `managed-by`, `repo`
- **LZ-TAG-02** `data-class` must be one of `public`, `internal`, `confidential`, `phi`
- **LZ-TAG-03** `managed-by` must equal `terraform`
- **LZ-TAG-04** Prefer tags from shared `local.required_tags`; flag inline literal tag maps as a smell

## Network exposure

- **LZ-NET-01** No resource may set `public_network_access_enabled = true`
- **LZ-NET-02** PaaS data services must be accessed via `azurerm_private_endpoint` on `snet-privateendpoints`
- **LZ-NET-03** Storage accounts must set `network_rules.default_action = "Deny"`
- **LZ-NET-04** NSG rules must not allow `0.0.0.0/0` or `*` inbound on ports 22, 3389, or other management-plane ports
- **LZ-NET-05** Public IPs are disallowed except on approved ingress/egress constructs such as Azure Firewall, App Gateway, or Front Door

## Identity and secrets

- **LZ-ID-01** Storage accounts must set `shared_access_key_enabled = false` and rely on Entra ID with `storage_use_azuread = true`
- **LZ-ID-02** Do not store access keys, connection strings, SAS tokens, or passwords in code, variables, outputs, or `locals`; use Key Vault references or federated identity
- **LZ-ID-03** Every compute resource must have a system- or user-assigned managed identity

## Encryption and TLS

- **LZ-SEC-01** Set `min_tls_version = "TLS1_2"` on storage, App Service, SQL, and other TLS-exposed resources
- **LZ-SEC-02** Storage must set `https_traffic_only_enabled = true` and `allow_nested_items_to_be_public = false`

## SKUs and tiers

- **LZ-SKU-01** Storage must use `account_tier = "Standard"`; production replication must be `ZRS`, `GZRS`, or `RAGZRS`; `LRS` is non-prod only
- **LZ-SKU-02** Approved general-compute VM sizes are `Standard_D2s_v5`, `Standard_D4s_v5`, `Standard_D8s_v5` unless justified

## Observability

- **LZ-OBS-01** Every resource supporting diagnostic settings must have an `azurerm_monitor_diagnostic_setting` pointing to the platform `azurerm_log_analytics_workspace`

## Terraform hygiene

- **LZ-TF-01** Pin all providers with `~>` constraints
- **LZ-TF-02** No `terraform apply` in CI on PRs; PRs run `plan` only
- **LZ-TF-03** Remote state only; flag removal of `backend "azurerm"` or addition of `backend "local"`
- **LZ-TF-04** Prefer `moved {}` blocks for renames and `import {}` blocks for brownfield adoption
- **LZ-TF-05** New `resource` blocks in `imports.tf` must be paired with matching `import {}` blocks and produce a zero-diff plan

# Working style

1. Make the smallest compliant Terraform change.
2. Cite the relevant `LZ-*` rule IDs in review comments, remediation notes, or summaries.
3. Run `terraform fmt` on touched files.
4. Summarize changes as a one-line PR title plus a bulleted body that references the landing-zone rules satisfied.

## Review comment format

> **`<RULE-ID>`** — <one-line problem>  
> *Fix:* <smallest concrete change, ideally as a code suggestion>
