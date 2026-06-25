#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

REPO_URL="https://github.com/CHAMANRANA/candlestick-pattern-classifier.git"
DIR_NAME="candlestick-pattern-classifier"

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}  📈 Nifty 50 Spatial-Temporal Vision Sandbox Setup  ${NC}"
echo -e "${BLUE}======================================================${NC}"

# Check if git is installed on the user's machine
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is not installed. Please install Git and try again.${NC}"
    exit 1
fi

# Clone the repo if it doesn't exist locally, or pull updates if it does
if [ ! -d "$DIR_NAME" ]; then
    echo -e "${YELLOW}>> Downloading application core...${NC}"
    git clone $REPO_URL
else
    echo -e "${YELLOW}>> Application found locally. Pulling latest updates...${NC}"
    cd $DIR_NAME && git pull && cd ..
fi

# Enter the project directory
cd $DIR_NAME || exit

# Init virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}>> Creating isolated virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}>> Virtual environment created.${NC}"
fi

# Activate environment and install dependencies
echo -e "${YELLOW}>> Activating venv and installing required packages...${NC}"
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# Launch web dashboard
echo -e "${GREEN}>> Booting Streamlit interface...${NC}"
echo -e "${BLUE}======================================================${NC}"

streamlit run app.py