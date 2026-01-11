#!/bin/bash
# Example workflow for Swiss French dataset collection
# This script demonstrates the complete workflow from setup to export

echo "🇨🇭 Swiss French Dataset Collection - Example Workflow"
echo "========================================================="
echo ""

# Step 1: Setup and create starter data
echo "📦 Step 1: Setting up dataset structure and creating starter data..."
python3 swiss_french_dataset_builder.py --setup --create-all
echo "✅ Setup complete!"
echo ""

# Step 2: Check initial statistics
echo "📊 Step 2: Checking initial dataset statistics..."
python3 swiss_french_dataset_builder.py --stats
echo ""

# Step 3: Generate synthetic data (example with small batch)
echo "🤖 Step 3: Generating synthetic translations..."
echo "   Note: This requires Apertus8B to be available"
echo ""

read -p "Do you want to generate synthetic data? (requires Apertus8B) [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Generate 10 synthetic translations for Valais with validation
    python3 swiss_french_synthetic_generator.py \
        --dialect valais \
        --generate 10 \
        --validation

    echo ""
    echo "✅ Synthetic data generated!"
    echo "📝 Review the validation file in: datasets/swiss_french/Validation/"
    echo "   Edit the JSON file, set approved: true for good translations"
    echo "   Then import with: python3 swiss_french_synthetic_generator.py --import-validated <file>"
else
    echo "⏭️  Skipping synthetic generation"
fi
echo ""

# Step 4: Import example dictionary (if you have one)
echo "📚 Step 4: Dictionary import example..."
echo "   If you have a CSV dictionary, import it with:"
echo "   python3 swiss_french_dataset_builder.py --dialect valais --import-csv my_dictionary.csv"
echo ""
echo "   Example CSV format:"
echo "   swiss_french,standard_french,dialect"
echo "   panosse,serpillière,valais"
echo "   ça joue,ça va,geneva"
echo ""

# Step 5: Create validation template
echo "✅ Step 5: Creating validation template for human translations..."
python3 swiss_french_dataset_builder.py --dialect valais --validation-template
echo ""
echo "📝 A CSV file has been created at: datasets/swiss_french/Validation/validation_template_valais.csv"
echo "   Open it in Excel/LibreOffice, fill in translations, then import:"
echo "   python3 swiss_french_dataset_builder.py --dialect valais --import-validated validation_template_valais.csv"
echo ""

# Step 6: Final statistics
echo "📊 Step 6: Final dataset statistics..."
python3 swiss_french_dataset_builder.py --stats
echo ""

# Step 7: Export instructions
echo "📦 Step 7: When ready to export for training..."
echo "   Run: python3 swiss_french_dataset_builder.py --export"
echo "   This creates a HuggingFace-compatible dataset in: datasets/swiss_french/huggingface_export/"
echo ""

echo "✅ Workflow demonstration complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Review the starter data in datasets/swiss_french/"
echo "   2. Add your own dictionary entries (CSV format)"
echo "   3. Generate and validate synthetic translations"
echo "   4. Fill in validation templates"
echo "   5. Collect data from GPSR, newspapers, native speakers"
echo "   6. When you have 20,000+ examples, export and train!"
echo ""
echo "📚 Full documentation: SWISS_FRENCH_DATASET_GUIDE.md"
echo ""
echo "🇨🇭 Bonne chance!"
