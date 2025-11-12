# ============================================================================
# DIRECTORY MANAGEMENT (FUNCTIONAL)
# ============================================================================
from pathlib import Path
from typing import Dict

def create_directory_structure(output_dir: Path) -> Dict[str, Path]:
    """Create and return all necessary directories"""
    directories = {
        'root': output_dir,
        'images': output_dir / "images",
        'metadata': output_dir / "metadata",
        'labeled': output_dir / "labeled",
        'logs': output_dir / "logs",
        'person': output_dir / "labeled" / "person",
        'no_person': output_dir / "labeled" / "no_person",
        'uncertain': output_dir / "labeled" / "uncertain"
    }
    
    for path in directories.values():
        path.mkdir(parents=True, exist_ok=True)
    
    return directories
