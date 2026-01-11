#!/usr/bin/env python3
"""
Download Romansh training dataset from HuggingFace
Dataset: swiss-ai/apertus-posttrain-romansh (46.1k German-Romansh pairs)
"""

import os
import sys
from pathlib import Path

try:
    from datasets import load_dataset
    print("✅ Datasets library loaded")
except ImportError:
    print("❌ Error: datasets library not installed")
    print("Install with: pip install datasets")
    sys.exit(1)


def download_romansh_dataset(output_dir="./datasets/romansh"):
    """Download and save Romansh dataset."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("🇨🇭 Downloading Romansh Dataset from HuggingFace")
    print("=" * 60)
    print("📦 Dataset: swiss-ai/apertus-posttrain-romansh")
    print("📊 Size: 46,100 German-Romansh parallel sentences")
    print(f"📁 Output: {output_path.absolute()}")
    print("=" * 60)

    try:
        print("\n⏳ Downloading dataset... (this may take a few minutes)")
        dataset = load_dataset("swiss-ai/apertus-posttrain-romansh")

        print(f"✅ Dataset downloaded successfully!")
        print(f"\n📊 Dataset info:")
        print(f"   Splits: {list(dataset.keys())}")

        for split_name, split_data in dataset.items():
            print(f"   {split_name}: {len(split_data)} examples")

        # Display sample
        if 'train' in dataset:
            sample = dataset['train'][0]
            print(f"\n💡 Sample data:")
            for key, value in sample.items():
                if isinstance(value, str) and len(value) < 200:
                    print(f"   {key}: {value}")

        # Save dataset to disk
        print(f"\n💾 Saving dataset to {output_path}...")
        dataset.save_to_disk(str(output_path))

        print(f"✅ Dataset saved successfully!")
        print(f"\n📝 Usage:")
        print(f"   from datasets import load_from_disk")
        print(f"   dataset = load_from_disk('{output_path}')")

        return dataset

    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Romansh training dataset")
    parser.add_argument(
        "--output",
        default="./datasets/romansh",
        help="Output directory (default: ./datasets/romansh)"
    )

    args = parser.parse_args()

    dataset = download_romansh_dataset(args.output)

    if dataset:
        print("\n✅ All done! Dataset ready for fine-tuning.")
    else:
        print("\n❌ Download failed.")
        sys.exit(1)
