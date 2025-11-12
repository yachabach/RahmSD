# ============================================================================
# STATISTICS (FUNCTIONAL)
# ============================================================================
from pathlib import Path
from typing import Dict

def calculate_collection_stats(directories: Dict[str, Path]) -> Dict:
    """Calculate statistics about collected data"""
    total_images = len(list(directories['images'].glob("*.png")))
    
    labeled_counts = {
        'person': len(list(directories['person'].glob("*.png"))),
        'no_person': len(list(directories['no_person'].glob("*.png"))),
        'uncertain': len(list(directories['uncertain'].glob("*.png")))
    }
    
    total_labeled = sum(labeled_counts.values())
    
    return {
        'total_samples': total_images,
        'total_labeled': total_labeled,
        'unlabeled': total_images - total_labeled,
        'label_breakdown': labeled_counts
    }


def print_stats(stats: Dict):
    """Pretty print statistics"""
    print("\n" + "="*60)
    print("COLLECTION STATISTICS")
    print("="*60)
    print(f"Total samples collected: {stats['total_samples']}")
    print(f"Total labeled: {stats['total_labeled']}")
    print(f"Unlabeled: {stats['unlabeled']}")
    print("\nLabel breakdown:")
    for label, count in stats['label_breakdown'].items():
        print(f"  {label}: {count}")
    print("="*60)

