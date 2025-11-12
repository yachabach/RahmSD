"""
Thermal Image Data Collection App - Hybrid Functional/OOP Approach
Uses functions for pure operations, classes for stateful objects
"""

import sys
import argparse
from pathlib import Path
from logger_setup import setup_logging
from dir_mgr import create_directory_structure
from load_config import load_config_file, parse_camera_configs
from collect_sample import collect_from_all_cameras
from stats import calculate_collection_stats, print_stats
from label_dataset import label_batch

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Thermal Data Collector')
    parser.add_argument('--config', type=str, required=True, help='Config JSON path')
    parser.add_argument('--output-dir', type=str, default='thermal_data', help='Output directory')
    parser.add_argument('--label', action='store_true', help='Run labeling mode')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    # Setup
    output_dir = Path(args.output_dir)
    directories = create_directory_structure(output_dir)
    logger = setup_logging(directories['logs'])
    
    # Load config
    config_data = load_config_file(args.config)
    camera_configs = parse_camera_configs(config_data)
    
    try:
        if args.stats:
            stats = calculate_collection_stats(directories)
            print_stats(stats)
            
        elif args.label:
            label_batch(directories, batch_size=100)
            
        else:
            successful, failed = collect_from_all_cameras(
                camera_configs,
                directories,
                config_data.get('login')
            )
            sys.exit(0 if successful > 0 else 1)
            
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
