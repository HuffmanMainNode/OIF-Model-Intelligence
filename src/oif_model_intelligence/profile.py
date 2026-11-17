"""Validate model cards and estimate weight memory requirements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED = ("id", "name", "architecture", "parameter_count", "weight_bits", "licenses")


def validate_model(model: Any) -> list[str]:
    if not isinstance(model, dict):
        return ["model profile must be an object"]
    errors = [f"missing field: {field}" for field in REQUIRED if field not in model]
    if errors:
        return errors
    if not isinstance(model["parameter_count"], int) or model["parameter_count"] <= 0:
        errors.append("parameter_count must be a positive integer")
    if model["weight_bits"] not in (2, 3, 4, 8, 16, 32):
        errors.append("weight_bits must be one of 2, 3, 4, 8, 16, 32")
    if not isinstance(model["licenses"], dict):
        errors.append("licenses must be an object with separate component terms")
    else:
        for key in ("weights", "code", "training_data"):
            if key not in model["licenses"]:
                errors.append(f"licenses.{key} must be stated (use 'unknown' if not known)")
    return errors


def estimate_weight_memory_gib(parameter_count: int, weight_bits: int) -> float:
    if parameter_count <= 0 or weight_bits <= 0:
        raise ValueError("parameter_count and weight_bits must be positive")
    return parameter_count * weight_bits / 8 / (1024 ** 3)


def assess_fit(model: dict[str, Any], available_memory_gib: float, headroom: float = 1.25) -> dict[str, Any]:
    if available_memory_gib <= 0 or headroom < 1:
        raise ValueError("available memory must be positive and headroom must be >= 1")
    required = estimate_weight_memory_gib(model["parameter_count"], model["weight_bits"])
    budget = available_memory_gib / headroom
    return {
        "model_id": model["id"],
        "weight_memory_estimate_gib": round(required, 3),
        "available_memory_gib": available_memory_gib,
        "headroom_factor": headroom,
        "weight_only_fit": required <= budget,
        "warning": "Weight-only estimate; excludes KV cache, activations, runtime overhead, and fragmentation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate model weight memory fit.")
    parser.add_argument("profile", type=Path)
    parser.add_argument("--memory-gib", type=float, required=True)
    args = parser.parse_args()
    model = json.loads(args.profile.read_text(encoding="utf-8"))
    errors = validate_model(model)
    if errors:
        parser.error("; ".join(errors))
    print(json.dumps(assess_fit(model, args.memory_gib), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
