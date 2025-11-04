#!/usr/bin/env python3
"""
Browser console error monitoring and feedback loop.
This script runs the application, captures browser console errors,
analyzes them, and provides fixes.
"""
import subprocess
import time
import json
import sys
import os
from typing import List, Dict, Any


class ConsoleErrorMonitor:
    """Monitors browser console for errors and provides fixes."""

    def __init__(self):
        self.frontend_dir = os.path.join(
            os.path.dirname(__file__), "question-interface", "frontend"
        )
        self.backend_dir = os.path.join(
            os.path.dirname(__file__), "question-interface", "backend"
        )
        self.venv_python = os.path.join(self.backend_dir, "venv", "bin", "python")
        self.errors_found = []
        self.warnings_found = []

    def start_servers(self):
        """Start both frontend and backend servers."""
        print("🚀 Starting servers for console monitoring...")

        # Start backend server
        self.backend_process = subprocess.Popen(
            [
                self.venv_python,
                "-m",
                "uvicorn",
                "main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload",
            ],
            cwd=self.backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Start frontend server
        self.frontend_process = subprocess.Popen(
            ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"],
            cwd=self.frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for servers to start
        print("⏳ Waiting for servers to initialize...")
        time.sleep(10)

    def stop_servers(self):
        """Stop the running servers."""
        print("🛑 Stopping servers...")
        if hasattr(self, "backend_process"):
            self.backend_process.terminate()
            self.backend_process.wait()
        if hasattr(self, "frontend_process"):
            self.frontend_process.terminate()
            self.frontend_process.wait()

    def analyze_console_logs(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze console logs for errors and warnings."""
        analysis = {
            "errors": [],
            "warnings": [],
            "network_errors": [],
            "react_errors": [],
            "threejs_errors": [],
            "cors_errors": [],
            "summary": {},
        }

        for log in logs:
            message = log.get("text", "").lower()
            level = log.get("level", "info")

            # Categorize errors
            if "failed to load resource" in message or "net::err_" in message:
                analysis["network_errors"].append(log)
            elif "access-control-allow-origin" in message or "cors" in message:
                analysis["cors_errors"].append(log)
            elif "react is not defined" in message or "react." in message:
                analysis["react_errors"].append(log)
            elif "three.js" in message or "webgl" in message or "three" in message:
                analysis["threejs_errors"].append(log)

            # General categorization
            if level == "error":
                analysis["errors"].append(log)
            elif level == "warning":
                analysis["warnings"].append(log)

        # Generate summary
        analysis["summary"] = {
            "total_errors": len(analysis["errors"]),
            "total_warnings": len(analysis["warnings"]),
            "network_errors": len(analysis["network_errors"]),
            "react_errors": len(analysis["react_errors"]),
            "threejs_errors": len(analysis["threejs_errors"]),
            "cors_errors": len(analysis["cors_errors"]),
            "is_clean": len(analysis["errors"]) == 0,
        }

        return analysis

    def generate_fixes(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific fixes for identified issues."""
        fixes = []

        # CORS fixes
        if analysis["summary"]["cors_errors"] > 0:
            fixes.append(
                {
                    "type": "cors",
                    "severity": "high",
                    "description": "CORS policy blocking requests",
                    "solution": "Update CORS middleware configuration in backend/main.py",
                    "code_changes": [
                        'Change allow_origins from specific hosts to ["*"]',
                        "Set allow_credentials=False when using wildcard origins",
                    ],
                }
            )

        # React fixes
        if analysis["summary"]["react_errors"] > 0:
            fixes.append(
                {
                    "type": "react",
                    "severity": "high",
                    "description": "React not properly imported or configured",
                    "solution": "Add React import and check Vite configuration",
                    "code_changes": [
                        'Add: import React from "react"; to component files',
                        "Ensure @vitejs/plugin-react is configured in vite.config.js",
                    ],
                }
            )

        # Network fixes
        if analysis["summary"]["network_errors"] > 0:
            fixes.append(
                {
                    "type": "network",
                    "severity": "medium",
                    "description": "Failed to load resources or API calls failing",
                    "solution": "Check server status and API endpoints",
                    "code_changes": [
                        "Verify backend server is running on correct port",
                        "Check API endpoint URLs in frontend code",
                        "Ensure SSL certificates are valid for HTTPS",
                    ],
                }
            )

        # Three.js fixes
        if analysis["summary"]["threejs_errors"] > 0:
            fixes.append(
                {
                    "type": "threejs",
                    "severity": "medium",
                    "description": "Three.js/WebGL rendering issues",
                    "solution": "Check Three.js imports and canvas setup",
                    "code_changes": [
                        "Verify @react-three/fiber and @react-three/drei are installed",
                        "Check Canvas component props and children",
                        "Ensure WebGL context is available",
                    ],
                }
            )

        return fixes

    def run_console_monitoring_test(self) -> Dict[str, Any]:
        """Run the console monitoring test using Playwright."""
        print("🔍 Running browser console monitoring...")

        # Create a temporary test file for console monitoring
        test_content = """
import { test, expect } from '@playwright/test';

test('monitor console for errors', async ({ page }) => {
  const logs = [];

  // Capture all console messages
  page.on('console', msg => {
    logs.push({
      level: msg.type(),
      text: msg.text(),
      location: msg.location(),
      args: msg.args().map(arg => arg.toString()).join(' ')
    });
    // Also log to console for debugging
    console.log(`[${msg.type().toUpperCase()}] ${msg.text()}`);
  });

  // Navigate to the application
  await page.goto('http://0.0.0.0:5173');

  // Wait for the page to load and interact
  await page.waitForTimeout(5000);

  // Try to interact with the 3D cloud
  const canvas = page.locator('canvas');
  if (await canvas.isVisible()) {
    await canvas.click({ position: { x: 100, y: 100 } });
    await page.waitForTimeout(2000);
  }

  // Try to load questions
  const questions = page.locator('li');
  await questions.first().waitFor({ timeout: 10000 });

  // Wait a bit more for any async errors
  await page.waitForTimeout(3000);

  // Output logs as JSON for the Python script to capture
  console.log('CONSOLE_LOGS_START');
  console.log(JSON.stringify(logs));
  console.log('CONSOLE_LOGS_END');
});
"""

        test_file = os.path.join(self.frontend_dir, "tests", "console-monitor.spec.js")
        with open(test_file, "w") as f:
            f.write(test_content)

        try:
            # Run Playwright test to capture console logs
            result = subprocess.run(
                [
                    "npx",
                    "playwright",
                    "test",
                    "console-monitor.spec.js",
                    "--reporter=json",
                ],
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
            )

            # Extract console logs from the output
            output_lines = result.stdout.split("\n")
            logs_started = False
            console_logs = []

            for line in output_lines:
                if "CONSOLE_LOGS_START" in line:
                    logs_started = True
                    continue
                elif "CONSOLE_LOGS_END" in line:
                    break
                elif logs_started:
                    try:
                        log_data = json.loads(line.strip())
                        if isinstance(log_data, list):
                            console_logs.extend(log_data)
                    except:
                        continue

            # Analyze the logs
            analysis = self.analyze_console_logs(console_logs)
            fixes = self.generate_fixes(analysis)

            return {
                "success": result.returncode == 0,
                "analysis": analysis,
                "fixes": fixes,
                "raw_logs": console_logs,
            }

        finally:
            # Clean up test file
            if os.path.exists(test_file):
                os.remove(test_file)

    def report_findings(self, results: Dict[str, Any]):
        """Report the findings and suggested fixes."""
        print("\n" + "=" * 60)
        print("🔍 BROWSER CONSOLE ANALYSIS REPORT")
        print("=" * 60)

        analysis = results["analysis"]
        summary = analysis["summary"]

        print(f"\n📊 SUMMARY:")
        print(f"   Errors: {summary['total_errors']}")
        print(f"   Warnings: {summary['total_warnings']}")
        print(f"   Network Errors: {summary['network_errors']}")
        print(f"   React Errors: {summary['react_errors']}")
        print(f"   Three.js Errors: {summary['threejs_errors']}")
        print(f"   CORS Errors: {summary['cors_errors']}")

        if summary["is_clean"]:
            print("\n✅ CONSOLE IS CLEAN - No errors detected!")
            # But still show warnings if any
            if summary["total_warnings"] > 0:
                print(f"\n⚠️  However, {summary['total_warnings']} warnings were found:")
                for warning in analysis["warnings"][:10]:  # Show first 10 warnings
                    print(f"   ⚠️  {warning.get('text', 'Unknown warning')}")
                if len(analysis["warnings"]) > 10:
                    print(f"   ... and {len(analysis['warnings']) - 10} more warnings")
            return

        print(f"\n🚨 ISSUES FOUND:")

        # Show specific errors
        for error in analysis["errors"][:5]:  # Show first 5 errors
            print(f"   ❌ {error.get('text', 'Unknown error')}")

        if len(analysis["errors"]) > 5:
            print(f"   ... and {len(analysis['errors']) - 5} more errors")

        # Show fixes
        fixes = results["fixes"]
        if fixes:
            print(f"\n🔧 SUGGESTED FIXES:")
            for i, fix in enumerate(fixes, 1):
                print(f"\n   {i}. {fix['description']} ({fix['severity']} priority)")
                print(f"      Solution: {fix['solution']}")
                for change in fix["code_changes"]:
                    print(f"      • {change}")
        else:
            print("\n🤔 No automatic fixes available for these issues.")

    def run_feedback_loop(self):
        """Run the complete feedback loop."""
        try:
            self.start_servers()
            results = self.run_console_monitoring_test()
            self.report_findings(results)

            if not results["analysis"]["summary"]["is_clean"]:
                print(f"\n💡 Next steps:")
                print(f"   1. Review the errors above")
                print(f"   2. Apply the suggested fixes")
                print(f"   3. Run this script again to verify")
                return False
            else:
                print(f"\n🎉 All console checks passed!")
                return True

        finally:
            self.stop_servers()


def main():
    """Main entry point."""
    monitor = ConsoleErrorMonitor()
    success = monitor.run_feedback_loop()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
