#!/usr/bin/env python3
"""
TraductAL Startup Check System
Verifies that all required models are downloaded before starting the application.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")

try:
    from huggingface_hub import snapshot_download, hf_hub_download
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("⚠️  Warning: huggingface_hub not available. Install with: pip install huggingface_hub")


class ModelChecker:
    """Check and download required models for TraductAL."""

    def __init__(self):
        self.cache_dir = os.path.expanduser("~/.cache/huggingface/hub")

        # Model definitions: (name, model_id, approximate_size_gb, required)
        self.models = [
            ("NLLB-200-1.3B", "facebook/nllb-200-1.3B", 5.0, True),
            ("Apertus-8B", "swiss-ai/Apertus-8B-2509", 16.0, True),
            ("Whisper-base", "openai/whisper-base", 0.3, False),  # Optional
        ]

        # TTS models are downloaded on-demand by tts_engine.py
        self.tts_note = "MMS-TTS models (~500MB each) download on first use per language"

    def get_model_path(self, model_id: str) -> Optional[Path]:
        """Get the local path for a model if it exists."""
        # Convert model_id to cache format: models--facebook--nllb-200-1.3B
        model_cache_name = "models--" + model_id.replace("/", "--")
        model_path = Path(self.cache_dir) / model_cache_name

        if model_path.exists():
            # Check if model has actual files (not just empty directory)
            snapshots_dir = model_path / "snapshots"
            if snapshots_dir.exists() and any(snapshots_dir.iterdir()):
                return model_path

        return None

    def check_model_exists(self, model_id: str) -> bool:
        """Check if a model is already downloaded."""
        return self.get_model_path(model_id) is not None

    def check_all_models(self) -> Tuple[List[dict], List[dict]]:
        """
        Check all required models.

        Returns:
            Tuple of (available_models, missing_models)
        """
        available = []
        missing = []

        for name, model_id, size_gb, required in self.models:
            model_info = {
                "name": name,
                "model_id": model_id,
                "size_gb": size_gb,
                "required": required
            }

            if self.check_model_exists(model_id):
                model_info["path"] = str(self.get_model_path(model_id))
                available.append(model_info)
            else:
                missing.append(model_info)

        return available, missing

    def download_model(self, model_id: str, model_name: str) -> bool:
        """
        Download a model from HuggingFace Hub.

        Returns:
            True if successful, False otherwise
        """
        if not HF_AVAILABLE:
            print(f"❌ Cannot download {model_name}: huggingface_hub not installed")
            return False

        try:
            print(f"\n📥 Downloading {model_name} ({model_id})...")
            print(f"   This may take several minutes depending on your connection speed.")

            # Download the model
            snapshot_download(
                repo_id=model_id,
                local_dir=None,  # Use default cache
                local_dir_use_symlinks=True,
                resume_download=True
            )

            print(f"✅ {model_name} downloaded successfully")
            return True

        except Exception as e:
            print(f"❌ Failed to download {model_name}: {e}")
            return False

    def print_status(self):
        """Print the current model status."""
        print("\n" + "="*70)
        print("🔍 TraductAL Model Status Check")
        print("="*70)

        available, missing = self.check_all_models()

        if available:
            print("\n✅ AVAILABLE MODELS:")
            for model in available:
                print(f"   • {model['name']:20s} ({model['size_gb']:.1f}GB)")

        if missing:
            total_size = sum(m['size_gb'] for m in missing)
            print(f"\n⚠️  MISSING MODELS ({len(missing)} models, ~{total_size:.1f}GB total):")
            for model in missing:
                required_str = "REQUIRED" if model['required'] else "OPTIONAL"
                print(f"   • {model['name']:20s} ({model['size_gb']:.1f}GB) - {required_str}")

        print(f"\n💡 NOTE: {self.tts_note}")
        print("="*70)

        return len(missing) == 0

    def run_interactive_setup(self) -> bool:
        """
        Run interactive setup to download missing models.

        Returns:
            True if all required models are available, False otherwise
        """
        available, missing = self.check_all_models()

        if not missing:
            print("\n✅ All models are ready!")
            return True

        # Filter for required models only
        required_missing = [m for m in missing if m['required']]
        optional_missing = [m for m in missing if not m['required']]

        if required_missing:
            print("\n⚠️  FIRST-TIME SETUP REQUIRED")
            print("="*70)
            print("TraductAL requires the following models to be downloaded:")
            print()

            total_size = sum(m['size_gb'] for m in required_missing)
            for model in required_missing:
                print(f"  📦 {model['name']}")
                print(f"     • Size: ~{model['size_gb']:.1f}GB")
                print(f"     • Model: {model['model_id']}")
                print()

            print(f"Total download size: ~{total_size:.1f}GB")
            print("="*70)

            response = input("\nDownload required models now? [Y/n]: ").strip().lower()

            if response in ['', 'y', 'yes']:
                success_count = 0
                for model in required_missing:
                    if self.download_model(model['model_id'], model['name']):
                        success_count += 1

                if success_count == len(required_missing):
                    print("\n✅ All required models downloaded successfully!")
                    return True
                else:
                    print(f"\n⚠️  Only {success_count}/{len(required_missing)} models downloaded")
                    return False
            else:
                print("\n⚠️  Setup cancelled. TraductAL requires these models to function.")
                return False

        if optional_missing:
            print(f"\n💡 Optional models available: {', '.join(m['name'] for m in optional_missing)}")
            print("   These will be downloaded automatically when needed.")

        return True

    def ensure_models_ready(self, interactive: bool = True) -> bool:
        """
        Ensure all required models are ready.

        Args:
            interactive: If True, prompt user to download missing models.
                        If False, just check and report status.

        Returns:
            True if all required models are available, False otherwise
        """
        if interactive:
            return self.run_interactive_setup()
        else:
            all_ready = self.print_status()

            if not all_ready:
                available, missing = self.check_all_models()
                required_missing = [m for m in missing if m['required']]

                if required_missing:
                    print("\n❌ Required models are missing. Run with interactive mode to download.")
                    return False

            return True


def check_models(interactive: bool = True) -> bool:
    """
    Main entry point for model checking.

    Args:
        interactive: Whether to interactively prompt for downloads

    Returns:
        True if all required models are ready, False otherwise
    """
    checker = ModelChecker()
    return checker.ensure_models_ready(interactive=interactive)


def main():
    """Command-line interface for model checking."""
    import argparse

    parser = argparse.ArgumentParser(
        description="TraductAL Model Checker - Verify and download required models"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Don't prompt for downloads, just show status"
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Force re-download of all models"
    )

    args = parser.parse_args()

    checker = ModelChecker()

    if args.force_download:
        print("🔄 Force downloading all models...")
        for name, model_id, size_gb, required in checker.models:
            if required:
                checker.download_model(model_id, name)
    else:
        success = checker.ensure_models_ready(interactive=not args.non_interactive)

        if not success:
            sys.exit(1)

    print("\n✅ Startup check complete!")


if __name__ == "__main__":
    main()
