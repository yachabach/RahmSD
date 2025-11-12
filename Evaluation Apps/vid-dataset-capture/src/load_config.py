# ============================================================================
# CONFIGURATION LOADING (FUNCTIONAL)
# ============================================================================
from data_structures import CameraConfig
from pathlib import Path
from typing import Dict, List
import json

def load_config_file(config_path: str) -> Dict:
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)


def parse_camera_configs(config_data: Dict) -> List[CameraConfig]:
    """Parse camera configurations from config dict"""
    return [CameraConfig(**cam) for cam in config_data['cameras']]