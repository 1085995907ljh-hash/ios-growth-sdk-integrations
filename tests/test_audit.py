import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_ios_growth_integrations.py"
SPEC = importlib.util.spec_from_file_location("audit", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="growth audit ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_multiple_projects_and_package_app(self):
        self.write("First App/First.xcodeproj/project.pbxproj", "FirebaseCore")
        self.write("Second/Second.xcodeproj/project.pbxproj", "AppsFlyerLib")
        self.write("Shared/Package.swift", "// package")
        self.write("Sources/Entry.swift", "import RevenueCat\n@main struct App {}")
        found = AUDIT.inventory(self.root)
        self.assertEqual(len(found["xcode_projects"]), 2)
        self.assertEqual(found["entry_points"], ["Sources/Entry.swift"])
        self.assertEqual(found["package_manifests"], ["Shared/Package.swift"])

    def test_no_source_config_or_absolute_root_in_output_and_no_writes(self):
        marker = "private-fixture-value-do-not-output"
        self.write("App.swift", 'import Mixpanel\nlet token = "' + marker + '"')
        self.write("GoogleService-Info.plist", marker)
        self.write(".env", marker)
        self.write("Private.xcconfig", marker)
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root)],
                                text=True, capture_output=True, check=True)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertNotIn(str(self.root), result.stdout + result.stderr)
        self.assertIn("Mixpanel", result.stdout)
        self.assertIn("GoogleService-Info.plist", result.stdout)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_skips_generated_and_agent_directories(self):
        for directory in ("Pods", "node_modules", ".git", ".agents/skills", "DerivedData"):
            self.write(directory + "/Example.swift", "import RevenueCat")
        self.assertEqual(AUDIT.inventory(self.root)["providers"]["RevenueCat"], [])

    def test_skips_symlink_files_and_directories(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "Outside.swift"
            target.write_text("import AppsFlyerLib", encoding="utf-8")
            try:
                (self.root / "Linked.swift").symlink_to(target)
                (self.root / "LinkedDir").symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("Symlink creation unavailable on this host")
            self.assertEqual(AUDIT.inventory(self.root)["providers"]["AppsFlyer"], [])

    def test_oversized_source(self):
        self.write("Large.swift", "x" * (AUDIT.MAX_SOURCE_BYTES + 1))
        self.assertEqual(AUDIT.inventory(self.root)["skipped_files"], 1)

    def test_invalid_path(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root / "missing")],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("existing directory", result.stderr)

    def test_control_characters_in_paths_are_escaped(self):
        if sys.platform == "win32":
            self.skipTest("Windows disallows this filename")
        self.write("App\nmisleading-output.swift", "import Mixpanel")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            AUDIT.display(AUDIT.inventory(self.root))
        self.assertIn("App\\nmisleading-output.swift", output.getvalue())
        self.assertNotIn("App\nmisleading-output.swift", output.getvalue())


if __name__ == "__main__":
    unittest.main()
