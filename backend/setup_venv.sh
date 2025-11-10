#!/bin/bash

# Setup Virtual Environment Script for Coal Blending Optimizer Backend

echo "🚀 Setting up Python Virtual Environment..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Display Python version
echo "✅ Python version:"
python3 --version
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
echo "   This may take a few minutes..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ All dependencies installed"
echo ""

# Verify installation
echo "🔍 Verifying installation..."
python -c "
import fastapi
import boto3
import pulp
print('✅ Core packages verified')
" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Some packages may not be installed correctly"
else
    echo "✅ Installation verified successfully"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To start the backend server:"
echo "  1. Make sure virtual environment is activated:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the server:"
echo "     python main.py"
echo ""
echo "  3. Server will be available at:"
echo "     http://127.0.0.1:8000"
echo ""
echo "To deactivate virtual environment later:"
echo "  deactivate"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
