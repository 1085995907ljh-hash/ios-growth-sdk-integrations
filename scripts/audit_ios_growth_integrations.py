#!/usr/bin/env python3
"""Read-only iOS SDK inventory. Print locations/counts, never file contents."""

import argparse
import os
from pathlib import Path
import re


SKIP_DIRS = {
    ".git", ".build", ".swiftpm", ".venv", "venv", "__pycache__",
    "node_modules", "Pods", "Carthage", "DerivedData", "build", "dist",
    ".codex", ".claude", ".agents", ".cursor",
}
PROVIDERS = {
    "RevenueCat": re.compile(r"\b(?:RevenueCat|Purchases)\b"),
    "Firebase": re.compile(r"\b(?:Firebase\w*|GoogleService)\b"),
    "Mixpanel": re.compile(r"\bMixpanel\b", re.IGNORECASE),
    "AppsFlyer": re.compile(r"\bAppsFlyer\w*\b", re.IGNORECASE),
}
ENTRY = re.compile(r"@main\b|UIApplicationDelegateAdaptor|UIApplicationDelegate\b")
PAID = re.compile(r"paywall|entitlement|subscription|restore|purchase", re.IGNORECASE)
EVENT = re.compile(r"\b(?:track|analytics|logEvent|identify|consent|optOut)\b", re.IGNORECASE)
MAX_SOURCE_BYTES = 2 * 1024 * 1024


def inventory(root):
    """Scan authored source/config locations, skipping symlinks/generated trees."""
    result = {
        "xcode_projects": [], "workspaces": [], "package_manifests": [],
        "configuration_files": [], "entry_points": [], "purchase_locations": [],
        "analytics_locations": [], "providers": {name: [] for name in PROVIDERS},
        "skipped_files": 0,
    }
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS
                         and not name.startswith(".")
                         and not (Path(parent) / name).is_symlink())
        for name in sorted(files):
            path = Path(parent) / name
            if path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            if name == "project.pbxproj" and path.parent.suffix == ".xcodeproj":
                result["xcode_projects"].append(path.parent.relative_to(root).as_posix())
            if name == "contents.xcworkspacedata" and path.parent.suffix == ".xcworkspace":
                result["workspaces"].append(path.parent.relative_to(root).as_posix())
            if name in {"Package.swift", "Package.resolved", "Podfile", "Cartfile"}:
                result["package_manifests"].append(relative)
            if (name == "GoogleService-Info.plist" or path.suffix == ".xcconfig"
                    or name.startswith(".env") or "secrets" in name.lower()):
                result["configuration_files"].append(relative)
                continue
            if path.suffix not in {".swift", ".m", ".mm"} and name != "project.pbxproj":
                continue
            try:
                with path.open("rb") as source:
                    content = source.read(MAX_SOURCE_BYTES + 1)
                if len(content) > MAX_SOURCE_BYTES:
                    result["skipped_files"] += 1
                    continue
                content = content.decode("utf-8", errors="replace")
            except OSError:
                result["skipped_files"] += 1
                continue
            for provider, pattern in PROVIDERS.items():
                count = len(pattern.findall(content))
                if count:
                    result["providers"][provider].append((relative, count))
            if path.suffix in {".swift", ".m", ".mm"}:
                for key, pattern in (("entry_points", ENTRY), ("purchase_locations", PAID),
                                     ("analytics_locations", EVENT)):
                    if pattern.search(content):
                        result[key].append(relative)
    return result


def display(result):
    print("iOS growth SDK inventory (heuristic; paths/counts only)")
    print("Paths are relative to the repository. Review paths before sharing.")
    for key in ("xcode_projects", "workspaces", "package_manifests", "configuration_files",
                "entry_points", "purchase_locations", "analytics_locations"):
        print("\n" + key.replace("_", " ").title() + ":")
        for path in result[key]:
            print("  " + ascii(path))  # Escape control characters in filenames.
        if not result[key]:
            print("  none detected")
    print("\nProvider symbol locations (not proof of runtime integration):")
    for provider, matches in result["providers"].items():
        print("  " + provider + ":")
        for path, count in matches:
            print("    " + ascii(path) + " (" + str(count) + " matches)")
        if not matches:
            print("    none detected")
    print("\nUnreadable/oversized source files skipped: " + str(result["skipped_files"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="App repository (default: current directory)")
    root = Path(parser.parse_args().root).expanduser().resolve()
    if not root.is_dir():
        parser.error("The repository must be an existing directory.")
    if not os.access(root, os.R_OK | os.X_OK):
        parser.error("The repository is not readable.")
    display(inventory(root))


if __name__ == "__main__":
    main()
