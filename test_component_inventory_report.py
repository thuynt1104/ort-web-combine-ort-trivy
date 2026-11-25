from pathlib import Path

from openpyxl import load_workbook

from app.features.analysis.component_inventory_csv import generate_component_inventory_report


def test_inventory_report_is_named_excel_workbook(tmp_path: Path) -> None:
    output_dir = tmp_path / "artifacts"
    output_dir.mkdir()
    (output_dir / "component-inventory.csv").write_text("old\n", encoding="utf-8")
    (output_dir / "analyzer-result.yml").write_text(
        """
repository:
  vcs:
    path: "samples/demo-app"
analyzer:
  result:
    packages:
      - id: "Maven:com.example:log4j-core:2.14.1"
        declared_licenses_processed:
          spdx_expression: "Apache-2.0"
        homepage_url: "https://logging.apache.org/log4j/2.x/"
      - id: "NPM::left-pad:1.3.0"
        declared_licenses:
          - "MIT"
        homepage_url: "https://github.com/left-pad/left-pad"
""",
        encoding="utf-8",
    )

    report_path = generate_component_inventory_report(output_dir, project_name="demo app")

    assert report_path == output_dir / "demo app_report.xlsx"
    assert report_path is not None and report_path.exists()
    assert not (output_dir / "component-inventory.csv").exists()

    sheet = load_workbook(report_path).active
    assert sheet is not None
    rows = list(sheet.iter_rows(values_only=True))
    assert rows[0] == ("No", "Component name", "Version", "License", "Homepage")
    assert rows[1] == (1, "left-pad", "1.3.0", "MIT", "https://github.com/left-pad/left-pad")
    assert rows[2] == (2, "log4j-core", "2.14.1", "Apache-2.0", "https://logging.apache.org/log4j/2.x/")
