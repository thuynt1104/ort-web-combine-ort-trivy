from pathlib import Path

from app.features.analysis.scancode_cli import build_scancode_license_command


def test_license_command_matches_scancode_cli() -> None:
    output_dir = Path("/tmp/job-artifacts")
    command = build_scancode_license_command(
        "/venv/bin/scancode",
        "/work/demo-app",
        output_dir,
    )
    assert command == [
        "/venv/bin/scancode",
        "--license",
        "--json-pp",
        str(output_dir / "scancode-license.json"),
        "--html",
        str(output_dir / "scancode-license.html"),
        "-v",
        "/work/demo-app",
    ]
