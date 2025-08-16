#!/usr/bin/env bash
set -euo pipefail

# BUas Data Science & AI BBQ Menu Generator
# One script to rule them all: install, generate, and display

echo "BUas Data Science & AI BBQ Menu Generator"
echo "========================================"
echo "Setting up your AI-powered dinner party menu..."
echo ""

# Ensure Python and pip are available
command -v python3 >/dev/null 2>&1 || { echo "Python 3 not found"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip and install build tooling
echo "Installing build dependencies..."
python3 -m pip install --upgrade pip build > /dev/null 2>&1

# Build wheel
echo "Building package..."
pushd python >/dev/null
python3 -m build -w > /dev/null 2>&1
popd >/dev/null

# Install the wheel with all AI dependencies
echo "Installing AI dependencies (this may take a few minutes)..."
pip install --upgrade --force-reinstall ./python/dist/*.whl > /dev/null 2>&1

echo ""
echo "Generating AI images and displaying menu..."
echo "This may take several minutes on first run as AI models download..."
echo ""

# Generate images and display menu with AI-generated ASCII art
buas-menu "$(pwd)/menu/dishes.yaml" --menu-md "$(pwd)/menu/menu.md" --with-ai-images --ascii-width 60 --ascii-height 30

echo ""
echo "Done! Images saved in ./generated_images/"
echo "Re-run this script anytime to see the menu again."