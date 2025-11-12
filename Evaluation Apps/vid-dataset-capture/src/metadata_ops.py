# ============================================================================
# METADATA OPERATIONS (FUNCTIONAL)
# ============================================================================
from datetime import datetime
import json
from pathlib import Path
from typing import List, Dict
from data_structures import Sample


def save_metadata(sample: Sample, metadata_dir: Path) -> Path:
    """Save sample metadata to JSON file"""
    timestamp_str = sample.timestamp.strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{sample.camera_id}_{timestamp_str}.json"
    filepath = metadata_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(sample.to_dict(), f, indent=2)
    
    return filepath


def load_metadata(filepath: Path) -> Dict:
    """Load metadata from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def get_unlabeled_metadata_files(metadata_dir: Path) -> List[Path]:
    """Get all metadata files that haven't been labeled yet"""
    metadata_files = sorted(metadata_dir.glob("*.json"))
    return [f for f in metadata_files if load_metadata(f).get('label') is None]


def update_metadata_label(metadata_file: Path, label: str) -> Dict:
    """Update metadata file with label"""
    metadata = load_metadata(metadata_file)
    metadata['label'] = label
    metadata['labeled_at'] = datetime.now().isoformat()
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata
