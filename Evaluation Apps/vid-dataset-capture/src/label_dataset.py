# ============================================================================
# INTERACTIVE LABELING (FUNCTIONAL)
# ============================================================================
import logging
from pathlib import Path
from typing import Dict, List, Optional
import json
from metadata_ops import load_metadata, update_metadata_label, get_unlabeled_metadata_files
from gen_training_dataset import generate_training_dataset

logger = logging.getLogger(__name__)

def label_sample_interactive(metadata_file: Path) -> Optional[str]:
    """
    Interactively label a single sample
    
    Returns:
        Label string or None if skipped/quit
    """
    metadata = load_metadata(metadata_file)
    
    print(f"\n{'='*60}")
    print(f"Camera: {metadata['camera_id']}")
    print(f"Time: {metadata['timestamp']}")
    print(f"Fields: {json.dumps(metadata['fields'], indent=2)}")
    print(f"Image: {metadata['image_filename']}")
    print(f"{'='*60}")
    
    while True:
        choice = input("Label (p=person, n=no_person, u=uncertain, s=skip, q=quit): ").lower()
        if choice in ['p', 'n', 'u', 's', 'q']:
            break
        print("Invalid input")
    
    if choice == 'q':
        return 'quit'
    if choice == 's':
        return None
    
    label_map = {'p': 'person', 'n': 'no_person', 'u': 'uncertain'}
    return label_map[choice]


def label_batch(directories: Dict[str, Path], batch_size: int = 50):
    """Label a batch of samples"""
    import shutil
    
    unlabeled = get_unlabeled_metadata_files(directories['metadata'])
    
    if not unlabeled:
        logger.info("No unlabeled data found!")
        return
    
    logger.info(f"Found {len(unlabeled)} unlabeled samples")
    
    for i, metadata_file in enumerate(unlabeled[:batch_size], 1):
        print(f"\nSample {i}/{min(batch_size, len(unlabeled))}")
        
        label = label_sample_interactive(metadata_file)
        
        if label == 'quit':
            break
        if label is None:
            continue
        
        # Update metadata
        metadata = update_metadata_label(metadata_file, label)
        
        # Copy image to labeled directory
        src_img = Path(metadata['image_path'])
        dst_img = directories[label] / src_img.name
        shutil.copy(src_img, dst_img)
        
        logger.info(f"Labeled as '{label}': {src_img.name}")
    
    # Generate dataset
    dataset_path = directories['root'] / "training_dataset.csv"
    generate_training_dataset(directories['metadata'], directories['labeled'], dataset_path)