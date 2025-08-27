#!/bin/bash

# TalentScout Hiring Assistant Setup Script
# This script sets up the development environment

echo "🎯 Setting up TalentScout Hiring Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please add your Groq API key."
else
    echo "ℹ️ .env file already exists"
fi

# Check if Groq API key is set
if [ -f ".env" ]; then
    if grep -q "your_groq_api_key_here" .env; then
        echo "⚠️ WARNING: Please update your Groq API key in the .env file"
        echo "   You can get your API key from: https://console.groq.com/"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your Groq API key to the .env file"
echo "2. Run the application with: streamlit run main.py"
echo "3. Open http://localhost:8501 in your browser"
echo ""
echo "For help, check the README.md file"
