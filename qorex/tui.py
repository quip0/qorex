from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, DataTable, Input, Label, Static

from qorex import __version__
from qorex.models import Finding, RiskLevel
from qorex.scanner.coordinator import scan_path


# ── ASCII banner ──────────────────────────────────────────────────────────────

BANNER = """\
 ██████╗  ██████╗ ██████╗ ███████╗██╗  ██╗
██╔═══██╗██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
██║   ██║██║   ██║██████╔╝█████╗   ╚███╔╝
██║▄▄ ██║██║   ██║██╔══██╗██╔══╝   ██╔██╗
╚██████╔╝╚██████╔╝██║  ██║███████╗██╔╝ ██╗
 ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"""

TAGLINE = "Quantum-Vulnerability Scanner  ◈  NIST PQC Migration Guidance"

RISK_ICON = {RiskLevel.CRITICAL: "●", RiskLevel.HIGH: "◆"}
RISK_LABEL = {RiskLevel.CRITICAL: "CRITICAL", RiskLevel.HIGH: "HIGH"}


# ── Custom widgets ────────────────────────────────────────────────────────────

class QorexBanner(Static):
    DEFAULT_CSS = ""

    def render(self) -> str:
        return f"[bold bright_magenta]{BANNER}[/]\n[dim cyan]{TAGLINE}[/]  [dim]v{__version__}[/]"


class ScanBar(Horizontal):
    DEFAULT_CSS = ""


class FindingsPanel(Vertical):
    DEFAULT_CSS = ""


class DetailPanel(VerticalScroll):
    DEFAULT_CSS = ""


class StatusBar(Static):
    DEFAULT_CSS = ""

    def set_status(self, msg: str, style: str = "dim") -> None:
        self.update(f"[{style}]{msg}[/]")


# ── Main App ──────────────────────────────────────────────────────────────────

class QorexApp(App):
    TITLE = "Qorex"

    CSS = """
    Screen {
        background: #0a0a14;
        color: #d4d4f0;
        layers: base overlay;
    }

    /* ── Banner ─────────────────────────────────────── */
    QorexBanner {
        height: 9;
        padding: 1 4;
        background: #0a0a14;
        border-bottom: solid #1e1e40;
        color: #a855f7;
        text-style: bold;
        content-align: left middle;
    }

    /* ── Scan bar ────────────────────────────────────── */
    ScanBar {
        height: 3;
        padding: 0 2;
        background: #0d0d1e;
        border-bottom: solid #1e1e40;
        align: left middle;
    }

    ScanBar Label {
        color: #6366f1;
        width: 8;
        content-align: left middle;
        padding: 0 1;
    }

    ScanBar Input {
        width: 1fr;
        border: tall #1e1e40;
        background: #070710;
        color: #e2e8f0;
        padding: 0 1;
    }

    ScanBar Input:focus {
        border: tall #7c3aed;
    }

    ScanBar Button {
        width: 14;
        margin: 0 0 0 1;
        background: #4c1d95;
        color: #e9d5ff;
        border: none;
        text-style: bold;
    }

    ScanBar Button:hover {
        background: #6d28d9;
        color: #ffffff;
    }

    ScanBar Button:focus {
        border: tall #a855f7;
    }

    ScanBar Button.-loading {
        background: #1e1e40;
        color: #6366f1;
    }

    /* ── Main content split ──────────────────────────── */
    #main {
        height: 1fr;
    }

    /* ── Findings panel ──────────────────────────────── */
    FindingsPanel {
        width: 58%;
        border-right: solid #1e1e40;
    }

    #findings-title {
        height: 2;
        padding: 0 2;
        background: #0d0d1e;
        border-bottom: solid #1e1e40;
        color: #6366f1;
        text-style: bold;
        content-align: left middle;
    }

    DataTable {
        height: 1fr;
        background: #0a0a14;
        color: #d4d4f0;
        border: none;
        scrollbar-background: #0a0a14;
        scrollbar-color: #2d2d5e;
        scrollbar-color-hover: #6366f1;
    }

    DataTable > .datatable--header {
        background: #0d0d1e;
        color: #6366f1;
        text-style: bold;
    }

    DataTable > .datatable--cursor {
        background: #1e1245;
        color: #e2e8f0;
    }

    DataTable > .datatable--hover {
        background: #13132a;
    }

    /* ── Detail panel ────────────────────────────────── */
    DetailPanel {
        width: 42%;
        padding: 0;
        background: #0a0a14;
        scrollbar-background: #0a0a14;
        scrollbar-color: #2d2d5e;
        scrollbar-color-hover: #6366f1;
    }

    #detail-title {
        height: 2;
        padding: 0 2;
        background: #0d0d1e;
        border-bottom: solid #1e1e40;
        color: #06b6d4;
        text-style: bold;
        content-align: left middle;
        dock: top;
    }

    #detail-content {
        padding: 1 2;
    }

    /* ── Status bar ──────────────────────────────────── */
    StatusBar {
        height: 1;
        padding: 0 2;
        background: #070710;
        border-top: solid #1e1e40;
        color: #475569;
        content-align: left middle;
    }
    """

    BINDINGS = [
        Binding("s", "scan", "Scan", show=True),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("ctrl+o", "focus_path", "Path", show=True),
        Binding("escape", "clear_detail", "Clear", show=False),
        Binding("q", "quit", "Quit", show=True),
    ]

    _findings: reactive[List[Finding]] = reactive([], recompose=False)
    _selected: reactive[Optional[Finding]] = reactive(None)
    _scanning: reactive[bool] = reactive(False)

    # ── Compose ───────────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield QorexBanner()

        with ScanBar():
            yield Label("◈ PATH")
            yield Input(placeholder="./project  or  /absolute/path", id="path-input")
            yield Button("⬡  SCAN", id="scan-btn", variant="primary")

        with Horizontal(id="main"):
            with FindingsPanel():
                yield Static("◈ FINDINGS", id="findings-title")
                yield DataTable(id="findings-table", cursor_type="row", zebra_stripes=True)

            with DetailPanel(id="detail-panel"):
                yield Static("◈ DETAIL", id="detail-title")
                yield Static(self._empty_detail(), id="detail-content")

        yield StatusBar("  [s] scan  ·  [j/k] navigate  ·  [ctrl+o] focus path  ·  [q] quit", id="status-bar")

    # ── Mount ─────────────────────────────────────────────────────────────────

    def on_mount(self) -> None:
        table = self.query_one("#findings-table", DataTable)
        table.add_column("  ", width=2, key="icon")
        table.add_column("RISK", width=10, key="risk")
        table.add_column("ALGORITHM", width=12, key="algo")
        table.add_column("FILE", key="file")
        table.add_column("LINE", width=6, key="line")
        self.query_one("#path-input", Input).focus()

    # ── Actions ───────────────────────────────────────────────────────────────

    def action_scan(self) -> None:
        if not self._scanning:
            self._start_scan()

    def action_cursor_down(self) -> None:
        self.query_one("#findings-table", DataTable).action_scroll_down()

    def action_cursor_up(self) -> None:
        self.query_one("#findings-table", DataTable).action_scroll_up()

    def action_focus_path(self) -> None:
        self.query_one("#path-input", Input).focus()

    def action_clear_detail(self) -> None:
        self._selected = None
        self._update_detail(None)

    # ── Event handlers ────────────────────────────────────────────────────────

    @on(Button.Pressed, "#scan-btn")
    def on_scan_button(self) -> None:
        self._start_scan()

    @on(Input.Submitted, "#path-input")
    def on_path_submitted(self) -> None:
        self._start_scan()

    @on(DataTable.RowSelected, "#findings-table")
    def on_row_selected(self, event: DataTable.RowSelected) -> None:
        idx = event.cursor_row
        if 0 <= idx < len(self._findings):
            self._selected = self._findings[idx]
            self._update_detail(self._selected)

    # ── Scan logic ────────────────────────────────────────────────────────────

    def _start_scan(self) -> None:
        if self._scanning:
            return
        path_str = self.query_one("#path-input", Input).value.strip() or "."
        path = Path(path_str).expanduser().resolve()
        if not path.exists():
            self._set_status(f"✗  Path not found: {path}", "bold red")
            return
        self._run_scan(str(path))

    @work(thread=True)
    def _run_scan(self, path: str) -> None:
        self.call_from_thread(self._set_scanning, True)
        self.call_from_thread(self._set_status, f"⟳  Scanning {path} …", "yellow")
        try:
            findings = scan_path(path)
        except Exception as exc:
            self.call_from_thread(self._set_status, f"✗  Error: {exc}", "bold red")
            self.call_from_thread(self._set_scanning, False)
            return
        self.call_from_thread(self._apply_findings, findings, path)

    def _apply_findings(self, findings: List[Finding], path: str) -> None:
        self._findings = findings
        self._selected = None
        self._rebuild_table(findings)
        self._update_detail(None)
        self._set_scanning(False)

        n_crit = sum(1 for f in findings if f.risk_level == RiskLevel.CRITICAL)
        n_high = sum(1 for f in findings if f.risk_level == RiskLevel.HIGH)
        title = self.query_one("#findings-title", Static)

        if not findings:
            title.update("[bold bright_green]◈ FINDINGS[/]  [dim]— no vulnerabilities detected[/]")
            self._set_status(f"✓  Scan complete: {path}  ·  clean", "bold green")
        else:
            parts = []
            if n_crit:
                parts.append(f"[bold red]{n_crit} critical[/]")
            if n_high:
                parts.append(f"[bold yellow]{n_high} high[/]")
            title.update(f"[bold #6366f1]◈ FINDINGS[/]  [dim]—[/]  {' · '.join(parts)}")
            self._set_status(
                f"✓  Scan complete: {path}  ·  {len(findings)} finding(s)",
                "dim",
            )

    def _rebuild_table(self, findings: List[Finding]) -> None:
        table = self.query_one("#findings-table", DataTable)
        table.clear()
        sorted_findings = sorted(findings, key=lambda f: (f.risk_level.value, f.file, f.line))
        self._findings = sorted_findings

        for f in sorted_findings:
            if f.risk_level == RiskLevel.CRITICAL:
                icon = "[bold red]●[/]"
                risk_cell = "[bold red]CRITICAL[/]"
            else:
                icon = "[bold yellow]◆[/]"
                risk_cell = "[bold yellow]HIGH[/]"

            short_file = self._shorten_path(f.file)
            table.add_row(icon, risk_cell, f"[cyan]{f.algorithm}[/]", short_file, str(f.line))

    # ── Detail rendering ──────────────────────────────────────────────────────

    def _update_detail(self, finding: Optional[Finding]) -> None:
        content = self.query_one("#detail-content", Static)
        content.update(self._render_detail(finding))

    def _render_detail(self, f: Optional[Finding]) -> str:
        if f is None:
            return self._empty_detail()

        if f.risk_level == RiskLevel.CRITICAL:
            risk_color = "bold red"
            risk_bar = "[red]" + "█" * 10 + "[/]"
        else:
            risk_color = "bold yellow"
            risk_bar = "[yellow]" + "█" * 6 + "[/][dim]" + "░" * 4 + "[/]"

        short_file = self._shorten_path(f.file)

        return (
            f"[{risk_color}]{RISK_ICON[f.risk_level]}  {RISK_LABEL[f.risk_level]}[/]\n"
            f"[dim]{'─' * 34}[/]\n\n"
            f"[bold #6366f1]ALGORITHM[/]\n"
            f"  [cyan]{f.algorithm}[/]\n\n"
            f"[bold #6366f1]LOCATION[/]\n"
            f"  [dim]{short_file}[/]  :[bold]{f.line}[/]\n\n"
            f"[bold #6366f1]RISK SEVERITY[/]\n"
            f"  {risk_bar}\n\n"
            f"[bold #6366f1]EXPLANATION[/]\n"
            + self._wrap(f.explanation, 34) + "\n\n"
            f"[bold #6366f1]MIGRATION PATH[/]\n"
            + self._wrap(f.migration_note, 34) + "\n\n"
            f"[bold #6366f1]NIST REPLACEMENT[/]\n"
            f"  [bold bright_green]{f.replacement_algorithm}[/]\n"
        )

    def _empty_detail(self) -> str:
        return (
            "\n\n\n"
            "[dim]  Select a finding to view[/]\n"
            "[dim]  explanation and migration[/]\n"
            "[dim]  guidance.[/]\n\n\n"
            "[dim]  ↑ ↓  or  j k  to navigate[/]\n"
            "[dim]  Enter to select[/]"
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _set_scanning(self, scanning: bool) -> None:
        self._scanning = scanning
        btn = self.query_one("#scan-btn", Button)
        if scanning:
            btn.label = "⟳  SCANNING"
            btn.add_class("-loading")
        else:
            btn.label = "⬡  SCAN"
            btn.remove_class("-loading")

    def _set_status(self, msg: str, style: str = "dim") -> None:
        self.query_one("#status-bar", StatusBar).set_status(msg, style)

    @staticmethod
    def _shorten_path(path: str, max_len: int = 38) -> str:
        p = Path(path)
        parts = p.parts
        if len(str(path)) <= max_len:
            return path
        if len(parts) > 3:
            return str(Path("…") / Path(*parts[-3:]))
        return path

    @staticmethod
    def _wrap(text: str, width: int) -> str:
        words = text.split()
        lines, current = [], []
        length = 0
        for word in words:
            if length + len(word) + 1 > width and current:
                lines.append("  " + " ".join(current))
                current, length = [word], len(word)
            else:
                current.append(word)
                length += len(word) + 1
        if current:
            lines.append("  " + " ".join(current))
        return "\n".join(lines)


def run() -> None:
    QorexApp().run()
