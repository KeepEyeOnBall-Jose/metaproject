#!/usr/bin/env python3
"""
Demo script to showcase the new 3D concept cloud visualization.
This starts the servers and provides instructions for viewing the enhanced interface.
"""
import subprocess
import time
import os


def demo_concept_cloud():
    """Start servers and demonstrate the 3D concept cloud."""
    frontend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "frontend"
    )
    backend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "backend"
    )
    venv_python = os.path.join(backend_dir, "venv", "bin", "python")

    print("🎨 Starting Enhanced 3D Concept Cloud Demo")
    print("=" * 50)
    print()
    print("✨ NEW FEATURES:")
    print("  • Floating 3D bubbles instead of static text")
    print("  • Organic clustering algorithm for natural distribution")
    print("  • Animated floating motion with gentle rotations")
    print("  • Interactive hover effects with color changes")
    print("  • Distorted materials for a more dynamic appearance")
    print("  • Inner glow effects for depth perception")
    print("  • Gradient background with fog effects")
    print("  • Real-time UI overlay with statistics")
    print("  • Smooth category selection with visual feedback")
    print()

    # Start backend server
    print("🔧 Starting backend server...")
    backend_process = subprocess.Popen(
        [
            venv_python,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
            "--reload",
        ],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Start frontend server
    print("🎭 Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for servers to start
    print("⏳ Warming up servers...")
    time.sleep(8)

    print()
    print("🎯 DEMO READY!")
    print("=" * 50)
    print("🌐 Open your browser to: http://0.0.0.0:5173")
    print()
    print("🎮 INTERACTIONS:")
    print("  • Click on any floating bubble to filter questions")
    print("  • Hover over bubbles to see color changes")
    print("  • Watch the organic floating animations")
    print("  • Notice how bubble sizes represent question counts")
    print("  • Check the UI overlay for real-time statistics")
    print()
    print("📊 VISUAL FEATURES:")
    print("  • Gradient background (purple to blue)")
    print("  • Atmospheric fog for depth")
    print("  • Multiple light sources for realistic shading")
    print("  • Distorted materials that react to movement")
    print("  • Smooth text labels above each bubble")
    print("  • Question counts displayed below bubbles")
    print()
    print("🔄 Press Ctrl+C to stop the demo")

    try:
        # Keep running until user interrupts
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print("🛑 Shutting down demo...")

    # Clean up processes
    print("🧹 Cleaning up servers...")
    backend_process.terminate()
    frontend_process.terminate()
    backend_process.wait()
    frontend_process.wait()
    print("✅ Demo completed!")


if __name__ == "__main__":
    demo_concept_cloud()
