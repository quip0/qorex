from typing import List
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

from qorex.models import Finding, RiskLevel

console = Console()

_RISK_COLORS = {
    RiskLevel.CRITICAL: "bold red",
    RiskLevel.HIGH: "bold yellow",
}


def render_findings(findings: List[Finding], scanned_path: str) -> None:
    console.print()
    console.print(f"[bold]qorex[/bold] — scanned [cyan]{scanned_path}[/cyan]")
    console.print()

    if not findings:
        console.print("[bold green]No quantum-vulnerable cryptography detected.[/bold green]")
        return

    table = Table(box=box.SIMPLE_HEAD, show_lines=False, expand=True)
    table.add_column("Risk", style="bold", width=10)
    table.add_column("Algorithm", width=12)
    table.add_column("File", overflow="fold")
    table.add_column("Line", width=6, justify="right")
    table.add_column("Match", overflow="fold")

    for f in sorted(findings, key=lambda x: (x.risk_level.value, x.file, x.line)):
        color = _RISK_COLORS[f.risk_level]
        table.add_row(
            Text(f.risk_level.value.upper(), style=color),
            f.algorithm,
            f.file,
            str(f.line),
            f.matched_text,
        )

    console.print(table)
    console.print(f"[bold]{len(findings)} finding(s)[/bold] — run with [cyan]--report json[/cyan] for full details and migration guidance.")
    console.print()
