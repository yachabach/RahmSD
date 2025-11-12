# ============================================================================
# DATA STRUCTURES
# ============================================================================
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

@dataclass
class CameraConfig:
    """Configuration for a single camera"""
    camera_id: str
    url: str
    video_selector: str = '.video-control'
    field_selectors: Dict[str, str] = None
    wait_time: int = 5
    
    def __post_init__(self):
        if self.field_selectors is None:
            self.field_selectors = {}


@dataclass
class Sample:
    """Captured sample data"""
    timestamp: datetime
    camera_id: str
    url: str
    image_filename: str
    image_path: Path
    fields: Dict
    label: Optional[str] = None
    labeled_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'camera_id': self.camera_id,
            'url': self.url,
            'image_filename': self.image_filename,
            'image_path': str(self.image_path),
            'fields': self.fields,
            'label': self.label,
            'labeled_at': self.labeled_at.isoformat() if self.labeled_at else None
        }

