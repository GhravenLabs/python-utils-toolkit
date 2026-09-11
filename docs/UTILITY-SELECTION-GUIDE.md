# Utility Selection Guide

Use this guide when deciding whether a helper belongs in the toolkit.

## Good fit

- Reusable across automation, agent, or CLI projects.
- Small enough to understand without a framework.
- Testable with deterministic unit tests.
- Safer than ad-hoc copies in multiple repos.

## Poor fit

- One-off project glue.
- Large framework abstractions.
- Helpers that hide network, file, or security behavior without clear naming.
- Code that needs secrets or service-specific credentials to test.

## Before adding a utility

- Add or update tests.
- Add a README example if the helper is public.
- Add changelog notes when behavior changes.
- Keep error handling explicit and Windows-friendly where possible.

