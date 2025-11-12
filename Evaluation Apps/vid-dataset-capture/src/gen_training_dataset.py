# ============================================================================
# DATASET GENERATION (FUNCTIONAL)
# ============================================================================
import logging
from pathlib import Path
import pandas as pd
from metadata_ops import load_metadata

logger = logging.getLogger(__name__)

def generate_training_dataset(metadata_dir: Path, labeled_dir: Path, output_path: Path):
    """Generate CSV dataset from labeled samples"""
    metadata_files = metadata_dir.glob("*.json")
    labeled_samples = []
    
    for metadata_file in metadata_files:
        metadata = load_metadata(metadata_file)
        
        if metadata.get('label'):
            row = {
                'timestamp': metadata['timestamp'],
                'camera_id': metadata['camera_id'],
                'image_path': str(labeled_dir / metadata['label'] / Path(metadata['image_path']).name),
                'label': metadata['label'],
                'labeled_at': metadata['labeled_at']
            }
            
            # Flatten field values
            for field_name, field_value in metadata.get('fields', {}).items():
                row[f'field_{field_name}'] = field_value
            
            labeled_samples.append(row)
    
    if labeled_samples:
        df = pd.DataFrame(labeled_samples)
        df.to_csv(output_path, index=False)
        logger.info(f"Training dataset: {output_path} ({len(labeled_samples)} samples)")
        logger.info(f"Label distribution:\n{df['label'].value_counts()}")
    else:
        logger.warning("No labeled samples found")

