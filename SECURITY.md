# Security Policy

Model profiles are descriptive metadata, not executable model packages.

- Treat model files, tokenizer assets, adapters, and conversion scripts as untrusted supply-chain inputs.
- Verify hashes and provenance from independent trusted channels before loading weights.
- Review licenses for weights, code, data, and documentation separately.
- Do not load untrusted models in processes with secrets or unrestricted network access.
- Memory estimates are not safety, performance, or compatibility guarantees.

Report vulnerabilities with the affected revision and reproducible details. Never attach credentials or proprietary model artifacts.
