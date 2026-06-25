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

# Use explicit paths to the venv executables to bypass ExecutionPolicy issues
$VenvPython = ".\venv\Scripts\python.exe"

Write-Host ">> Upgrading pip..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip | Out-Null

Write-Host ">> Installing required packages..." -ForegroundColor Yellow
Write-Host ">> Please Be Patient..." -ForegroundColor Red
& $VenvPython -m pip install -r requirements.txt

# Launch web dashboard
Write-Host ">> Booting Streamlit interface..." -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Cyan

& $VenvPython -m streamlit run app.py