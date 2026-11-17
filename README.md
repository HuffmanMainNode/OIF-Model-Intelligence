# OIF Model Intelligence

**Model metadata, licensing clarity, and hardware-fit estimation for local and open-weight AI.**

This repository provides a model-card normalizer and transparent hardware-fit estimator. It helps compare declared model requirements with a local hardware profile. It does not download models, run inference, verify publisher claims, or declare a model open source based on weights alone.

## Implemented

- Model metadata validation with architecture, parameter count, weight format, and license fields.
- Separate license dimensions for code, weights, training data, and documentation.
- Rough memory estimation from parameter count and bits per parameter.
- Hardware-fit classification with configurable memory headroom.
- CLI report and tests.

## Quick start

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
oif-model-fit examples/model-profile.json
```

No external service or runtime dependency is required.

## Important interpretation

The estimate covers weight storage only. Real inference memory also includes activations, KV cache, runtime overhead, context length, batching, and backend-specific allocations. The result is a screening estimate, not a compatibility guarantee or benchmark.

A model may have open weights but restrictive terms, unavailable training data, or non-open training code. Inspect each license component independently before redistribution or commercial use.

## Scope

This repository owns model metadata and local resource estimation. Cognitive behavior and reasoning evaluation belong in [OIF-Cognitive-Systems](https://github.com/HuffmanMainNode/OIF-Cognitive-Systems); cross-resource discovery contracts belong in [Open-Intelligence-Fabric](https://github.com/HuffmanMainNode/Open-Intelligence-Fabric).
