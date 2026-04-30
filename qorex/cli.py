import click
from qorex import __version__
from qorex.scanner.coordinator import scan_path
from qorex.output.terminal import render_findings
from qorex.report.json_report import export_json


@click.group()
@click.version_option(version=__version__, prog_name="qorex")
def main():
    """Qorex — quantum-vulnerability scanner for cryptographic code."""



@main.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("--report", "report_format", type=click.Choice(["json"]), default=None, help="Export findings as structured report.")
@click.option("--output", "-o", default=None, help="Output file for report (defaults to stdout).")
def scan(path, report_format, output):
    """Scan PATH for quantum-vulnerable cryptography."""
    findings = scan_path(path)
    render_findings(findings, path)
    if report_format == "json":
        export_json(findings, output)


@main.command()
def tui():
    """Launch the interactive terminal UI."""
    from qorex.tui import run
    run()
