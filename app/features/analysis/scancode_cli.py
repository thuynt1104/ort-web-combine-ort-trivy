"""Run a ScanCode Toolkit license scan with the documented CLI.

This is ``scancode --license`` on the selected project directory, the same
command described in the ScanCode CLI reference. It walks every file under
that directory. ORT's ``scan --package-types PROJECT`` wrapper is not used.
"""
from __future__ import annotations

import asyncio
import shlex
import time
from pathlib import Path
from typing import Callable, Optional

from app.config import settings
from app.features.jobs.event_contract import EVENT_LOG, make_event
from app.features.jobs.log_stream import log_stream_hub

JSON_FILENAME = "scancode-license.json"
HTML_FILENAME = "scancode-license.html"

_HEARTBEAT_INTERVAL = 60
_READLINE_TIMEOUT = 60


def build_scancode_license_command(executable: str, target: str, output_dir: Path) -> list[str]:
    """Return the ScanCode license command for one project directory.

    ``--license`` scans only for licenses. ``--json-pp`` and ``--html`` are
    documented output formats. ``-v`` streams file-by-file progress to the job log.
    """
    return [
        executable,
        "--license",
        "--json-pp",
        str(output_dir / JSON_FILENAME),
        "--html",
        str(output_dir / HTML_FILENAME),
        "-v",
        str(target),
    ]


def _make_log_fn(job_id: str, log_file: Path):
    async def _fn(line: str) -> None:
        text = line if line.endswith("\n") else line + "\n"
        with log_file.open("a", encoding="utf-8") as out:
            out.write(text)
        await log_stream_hub.publish(job_id, make_event(EVENT_LOG, line=text))

    return _fn


async def run_scancode_license(
    job_id: str,
    target: str,
    output_dir: Path,
    log_file: Path,
    *,
    executable: str,
    on_process_start: Optional[Callable[[asyncio.subprocess.Process], None]] = None,
) -> int:
    """Scan ``target`` for licenses and write JSON plus HTML into ``output_dir``."""
    log_fn = _make_log_fn(job_id, log_file)
    output_dir.mkdir(parents=True, exist_ok=True)
    command = build_scancode_license_command(executable, target, output_dir)
    await log_fn("[scancode] $ " + " ".join(shlex.quote(part) for part in command))

    cwd = target if Path(target).is_dir() else None
    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    if on_process_start is not None:
        try:
            on_process_start(process)
        except Exception:
            pass

    start_time = time.monotonic()
    timeout_secs = settings.ort_job_timeout_seconds
    last_heartbeat = start_time
    assert process.stdout is not None

    while True:
        if time.monotonic() - start_time >= timeout_secs:
            await log_fn(f"[scancode] Exceeded timeout of {timeout_secs}s — killing process.")
            try:
                process.kill()
            except ProcessLookupError:
                pass
            return -1
        try:
            line = await asyncio.wait_for(process.stdout.readline(), timeout=_READLINE_TIMEOUT)
        except asyncio.TimeoutError:
            now = time.monotonic()
            if now - last_heartbeat >= _HEARTBEAT_INTERVAL:
                elapsed = int(now - start_time)
                await log_fn(
                    f"[scancode] still running... ({elapsed // 60}m {elapsed % 60}s elapsed)"
                )
                last_heartbeat = now
            continue
        if not line:
            break
        await log_fn(line.decode("utf-8", errors="replace"))
        last_heartbeat = time.monotonic()

    return await process.wait()
