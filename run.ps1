Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  📈 Nifty 50 Spatial-Temporal Vision Sandbox Setup  " -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

$RepoUrl = "https://github.com/CHAMANRANA/candlestick-pattern-classifier.git"
$DirName = "candlestick-pattern-classifier"

# Clone the repo if it doesn't exist locally, or pull updates if it does
if (-Not (Test-Path -Path $DirName)) {
    Write-Host ">> Downloading application core..." -ForegroundColor Yellow
    git clone $RepoUrl
} else {
    Write-Host ">> Application found locally. Pulling latest updates..." -ForegroundColor Yellow
    Set-Location -Path $DirName
    git pull
    Set-Location -Path ..
}

# Enter the project directory
Set-Location -Path $DirName

# Init virtual environment
if (-Not (Test-Path -Path "venv")) {
    Write-Host ">> Creating isolated virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host ">> Virtual environment created." -ForegroundColor Green
}

# Activate environment and install dependencies
Write-Host ">> Activating venv and installing required packages..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip | Out-Null
pip install -r requirements.txt

# Launch web dashboard
Write-Host ">> Booting Streamlit interface..." -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Cyan

streamlit run app.py