import json
import sys
from dataclasses import asdict
from typing import List, Optional

from qorex.models import Finding


def export_json(findings: List[Finding], output_path: Optional[str]) -> None:
    data = {
        "version": "0.1.0",
        "findings": [_serialize(f) for f in findings],
        "summary": {
            "total": len(findings),
            "critical": sum(1 for f in findings if f.risk_level.value == "critical"),
            "high": sum(1 for f in findings if f.risk_level.value == "high"),
        },
    }
    payload = json.dumps(data, indent=2)
    if output_path:
        with open(output_path, "w") as fh:
            fh.write(payload)
        from qorex.output.terminal import console
        console.print(f"[green]Report written to[/green] {output_path}")
    else:
        print(payload)


def _serialize(f: Finding) -> dict:
    d = asdict(f)
    d["risk_level"] = f.risk_level.value
    d["language"] = f.language.value
    return d
