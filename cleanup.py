#!/usr/bin/env python3
"""
Project Cleanup Script

This script cleans up development artifacts and temporary files from the project.
It can be run manually or as part of a CI/CD pipeline.

Usage:
    python cleanup.py [--dry-run] [--verbose]
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Tuple


def find_pycache_dirs(root_path: Path) -> List[Path]:
    """Find all __pycache__ directories in the project (excluding .venv)."""
    pycache_dirs = []
    
    for dirpath, dirnames, _ in os.walk(root_path):
        # Skip .venv directory
        if '.venv' in Path(dirpath).parts:
            continue
            
        if '__pycache__' in dirnames:
            pycache_dirs.append(Path(dirpath) / '__pycache__')
    
    return pycache_dirs


def find_pyc_files(root_path: Path) -> List[Path]:
    """Find all .pyc files in the project (excluding .venv)."""
    pyc_files = []
    
    for dirpath, _, filenames in os.walk(root_path):
        # Skip .venv directory
        if '.venv' in Path(dirpath).parts:
            continue
            
        for filename in filenames:
            if filename.endswith('.pyc'):
                pyc_files.append(Path(dirpath) / filename)
    
    return pyc_files


def find_temp_files(root_path: Path) -> List[Path]:
    """Find temporary files that should be cleaned up."""
    temp_extensions = {'.tmp', '.bak', '.swp', '.DS_Store', '.log~'}
    temp_files = []
    
    for dirpath, _, filenames in os.walk(root_path):
        # Skip .venv directory
        if '.venv' in Path(dirpath).parts:
            continue
            
        for filename in filenames:
            if any(filename.endswith(ext) for ext in temp_extensions):
                temp_files.append(Path(dirpath) / filename)
    
    return temp_files


def clear_runtime_logs(root_path: Path) -> List[Path]:
    """Clear runtime log files but keep the directory structure."""
    log_dir = root_path / 'logs'
    cleared_files = []
    
    if log_dir.exists():
        for log_file in log_dir.glob('*.log'):
            if log_file.is_file():
                cleared_files.append(log_file)
    
    return cleared_files


def cleanup_project(root_path: Path, dry_run: bool = False, verbose: bool = False) -> Tuple[int, int]:
    """
    Clean up the project by removing development artifacts.
    
    Returns:
        Tuple of (files_removed, directories_removed)
    """
    files_removed = 0
    directories_removed = 0
    
    print("🧹 Starting project cleanup...")
    
    # Find items to clean
    pycache_dirs = find_pycache_dirs(root_path)
    pyc_files = find_pyc_files(root_path)
    temp_files = find_temp_files(root_path)
    log_files = clear_runtime_logs(root_path)
    
    # Remove __pycache__ directories
    for pycache_dir in pycache_dirs:
        if verbose or dry_run:
            print(f"  📁 {'[DRY RUN] ' if dry_run else ''}Removing directory: {pycache_dir}")
        
        if not dry_run:
            try:
                shutil.rmtree(pycache_dir)
                directories_removed += 1
            except Exception as e:
                print(f"  ❌ Error removing {pycache_dir}: {e}")
    
    # Remove .pyc files
    for pyc_file in pyc_files:
        if verbose or dry_run:
            print(f"  📄 {'[DRY RUN] ' if dry_run else ''}Removing file: {pyc_file}")
        
        if not dry_run:
            try:
                pyc_file.unlink()
                files_removed += 1
            except Exception as e:
                print(f"  ❌ Error removing {pyc_file}: {e}")
    
    # Remove temporary files
    for temp_file in temp_files:
        if verbose or dry_run:
            print(f"  🗑️ {'[DRY RUN] ' if dry_run else ''}Removing temp file: {temp_file}")
        
        if not dry_run:
            try:
                temp_file.unlink()
                files_removed += 1
            except Exception as e:
                print(f"  ❌ Error removing {temp_file}: {e}")
    
    # Clear log files
    for log_file in log_files:
        if verbose or dry_run:
            print(f"  📋 {'[DRY RUN] ' if dry_run else ''}Clearing log file: {log_file}")
        
        if not dry_run:
            try:
                log_file.write_text("")  # Clear content but keep file
                files_removed += 1
            except Exception as e:
                print(f"  ❌ Error clearing {log_file}: {e}")
    
    return files_removed, directories_removed


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Clean up project development artifacts")
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help="Show what would be cleaned without actually removing files"
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help="Show detailed output of what is being cleaned"
    )
    
    args = parser.parse_args()
    
    # Get project root (where this script is located)
    project_root = Path(__file__).parent.absolute()
    
    print(f"🌦️ Weather Dashboard Project Cleanup")
    print(f"📁 Project root: {project_root}")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be actually removed")
    
    try:
        files_removed, directories_removed = cleanup_project(
            project_root, 
            dry_run=args.dry_run, 
            verbose=args.verbose
        )
        
        if not args.dry_run:
            print(f"\n✅ Cleanup complete!")
            print(f"   📄 Files removed/cleared: {files_removed}")
            print(f"   📁 Directories removed: {directories_removed}")
        else:
            print(f"\n📋 Dry run complete - found items that would be cleaned:")
            print(f"   📄 Files to remove/clear: {files_removed}")
            print(f"   📁 Directories to remove: {directories_removed}")
            
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
