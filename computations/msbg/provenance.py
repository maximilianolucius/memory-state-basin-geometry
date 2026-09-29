"""Environment capture, deterministic seeding, hashing and run manifests."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

__all__ = ["environment", "sha256_file", "write_manifest", "set_seed", "RunRecorder"]

SEED = 20260929  # fixed project-wide seed (COMPUTE_AGENT_INITIAL_PROMPT.md: "fix random seeds")


def set_seed(seed: int = SEED) -> np.random.Generator:
    return np.random.default_rng(seed)


def _pkg(name):
    try:
        mod = __import__(name)
        return getattr(mod, "__version__", "unknown")
    except Exception:
        return None


def environment() -> dict:
    env = {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "packages": {n: _pkg(n) for n in ("numpy", "scipy", "mpmath", "sympy", "flint", "matplotlib")},
        "numpy_blas": None,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seed": SEED,
    }
    try:
        cfg = np.__config__.show(mode="dicts")  # numpy >= 2
        env["numpy_blas"] = cfg.get("Build Dependencies", {}).get("blas", {})
    except Exception:
        pass
    try:
        env["git_commit"] = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
        env["git_branch"] = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        env["git_dirty"] = bool(
            subprocess.check_output(["git", "status", "--porcelain"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        env["git_commit"] = None
    return env


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(path, payload: dict, artifacts=()) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "task": "TASK-0001",
        "environment": environment(),
        "payload": payload,
        "artifacts": [
            {"path": str(a), "sha256": sha256_file(a), "bytes": os.path.getsize(a)}
            for a in artifacts
            if os.path.exists(a)
        ],
    }
    path.write_text(json.dumps(doc, indent=2, default=_jsonable))
    return path


def _jsonable(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


class RunRecorder:
    """Collects a stage's results and writes ``data/`` + ``manifests/`` artifacts."""

    def __init__(self, stage: str, root: str | Path = "."):
        self.stage = stage
        self.root = Path(root)
        self.results: dict = {}
        self.artifacts: list = []
        self.t0 = time.time()

    def add(self, key, value):
        self.results[key] = value
        return value

    def save_npz(self, name, **arrays):
        p = self.root / "data" / f"{self.stage}_{name}.npz"
        p.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(p, **arrays)
        self.artifacts.append(p)
        return p

    def save_json(self, name, obj):
        p = self.root / "data" / f"{self.stage}_{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, indent=2, default=_jsonable))
        self.artifacts.append(p)
        return p

    def finish(self):
        self.results["wall_seconds"] = round(time.time() - self.t0, 3)
        return write_manifest(
            self.root / "manifests" / f"{self.stage}_manifest.json",
            self.results,
            self.artifacts,
        )
