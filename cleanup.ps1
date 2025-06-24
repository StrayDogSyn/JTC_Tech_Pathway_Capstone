# Weather Dashboard Project Cleanup Script
# ========================================
#
# This PowerShell script cleans up development artifacts and temporary files
# from the Weather Dashboard project.
#
# Usage:
#   .\cleanup.ps1 [-DryRun] [-Verbose]
#
# Parameters:
#   -DryRun   : Show what would be cleaned without actually removing files
#   -Verbose  : Show detailed output of what is being cleaned

param(
    [switch]$DryRun,
    [switch]$Verbose
)

function Write-Status {
    param($Message, $Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Action {
    param($Message, $Color = "Cyan")
    if ($Verbose -or $DryRun) {
        $prefix = if ($DryRun) { "[DRY RUN] " } else { "" }
        Write-Host "  $prefix$Message" -ForegroundColor $Color
    }
}

function Remove-PyCache {
    param($ProjectRoot)
    
    $removed = 0
    $pycacheDirs = Get-ChildItem -Path $ProjectRoot -Recurse -Directory -Name "__pycache__" | 
                   Where-Object { $_ -notlike "*\.venv\*" }
    
    foreach ($dir in $pycacheDirs) {
        $fullPath = Join-Path $ProjectRoot $dir
        Write-Action "Removing directory: $fullPath" "Yellow"
        
        if (-not $DryRun) {
            try {
                Remove-Item -Path $fullPath -Recurse -Force
                $removed++
            }
            catch {
                Write-Status "  ❌ Error removing $fullPath`: $_" "Red"
            }
        } else {
            $removed++
        }
    }
    
    return $removed
}

function Remove-PycFiles {
    param($ProjectRoot)
    
    $removed = 0
    $pycFiles = Get-ChildItem -Path $ProjectRoot -Recurse -File -Filter "*.pyc" | 
                Where-Object { $_.FullName -notlike "*\.venv\*" }
    
    foreach ($file in $pycFiles) {
        Write-Action "Removing file: $($file.FullName)" "Yellow"
        
        if (-not $DryRun) {
            try {
                Remove-Item -Path $file.FullName -Force
                $removed++
            }
            catch {
                Write-Status "  ❌ Error removing $($file.FullName)`: $_" "Red"
            }
        } else {
            $removed++
        }
    }
    
    return $removed
}

function Remove-TempFiles {
    param($ProjectRoot)
    
    $removed = 0
    $tempExtensions = @("*.tmp", "*.bak", "*.swp", ".DS_Store", "*.log~")
    
    foreach ($pattern in $tempExtensions) {
        $tempFiles = Get-ChildItem -Path $ProjectRoot -Recurse -File -Filter $pattern | 
                     Where-Object { $_.FullName -notlike "*\.venv\*" }
        
        foreach ($file in $tempFiles) {
            Write-Action "Removing temp file: $($file.FullName)" "Yellow"
            
            if (-not $DryRun) {
                try {
                    Remove-Item -Path $file.FullName -Force
                    $removed++
                }
                catch {
                    Write-Status "  ❌ Error removing $($file.FullName)`: $_" "Red"
                }
            } else {
                $removed++
            }
        }
    }
    
    return $removed
}

function Clear-RuntimeLogs {
    param($ProjectRoot)
    
    $cleared = 0
    $logDir = Join-Path $ProjectRoot "logs"
    
    if (Test-Path $logDir) {
        $logFiles = Get-ChildItem -Path $logDir -Filter "*.log" -File
        
        foreach ($file in $logFiles) {
            Write-Action "Clearing log file: $($file.FullName)" "Yellow"
            
            if (-not $DryRun) {
                try {
                    Clear-Content -Path $file.FullName
                    $cleared++
                }
                catch {
                    Write-Status "  ❌ Error clearing $($file.FullName)`: $_" "Red"
                }
            } else {
                $cleared++
            }
        }
    }
    
    return $cleared
}

# Main script execution
$projectRoot = $PSScriptRoot

Write-Status "🌦️ Weather Dashboard Project Cleanup" "Cyan"
Write-Status "📁 Project root: $projectRoot" "Gray"

if ($DryRun) {
    Write-Status "🔍 DRY RUN MODE - No files will be actually removed" "Yellow"
}

Write-Status ""
Write-Status "🧹 Starting project cleanup..." "Green"

try {
    # Perform cleanup operations
    $dirsRemoved = Remove-PyCache -ProjectRoot $projectRoot
    $pycFilesRemoved = Remove-PycFiles -ProjectRoot $projectRoot
    $tempFilesRemoved = Remove-TempFiles -ProjectRoot $projectRoot
    $logsCleared = Clear-RuntimeLogs -ProjectRoot $projectRoot
    
    $totalFiles = $pycFilesRemoved + $tempFilesRemoved + $logsCleared
    
    Write-Status ""
    if (-not $DryRun) {
        Write-Status "✅ Cleanup complete!" "Green"
        Write-Status "   📄 Files removed/cleared: $totalFiles" "Gray"
        Write-Status "   📁 Directories removed: $dirsRemoved" "Gray"
    } else {
        Write-Status "📋 Dry run complete - found items that would be cleaned:" "Yellow"
        Write-Status "   📄 Files to remove/clear: $totalFiles" "Gray"
        Write-Status "   📁 Directories to remove: $dirsRemoved" "Gray"
    }
}
catch {
    Write-Status "❌ Error during cleanup: $_" "Red"
    exit 1
}
