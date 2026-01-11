#!/usr/bin/env python3
"""
TraductAL Gradio Web Interface
Multilingual translation system with NLLB-200 + Apertus8B
Supports 66+ languages with STT/TTS capabilities
"""

import os
import sys
import gradio as gr
import warnings
warnings.filterwarnings("ignore")

# Run startup check for required models
try:
    from startup_check import check_models
    print("🔍 Checking required models...")
    if not check_models(interactive=False):
        print("\n⚠️  Some required models are missing.")
        print("💡 Run 'python startup_check.py' to download them interactively.")
        # Continue anyway for development/testing
except ImportError:
    print("⚠️  startup_check.py not found - skipping model verification")
except Exception as e:
    print(f"⚠️  Model check failed: {e}")
    # Continue anyway

try:
    from unified_translator import UnifiedTranslator
    print("✅ Unified translator loaded")
except ImportError as e:
    print(f"❌ Error loading translator: {e}")
    sys.exit(1)

try:
    from tts_engine import TTSEngine
    print("✅ TTS engine loaded")
    tts_enabled = True
except ImportError as e:
    print(f"⚠️  TTS engine not available: {e}")
    tts_enabled = False

try:
    from whisper_stt import WhisperSTT
    print("✅ Whisper STT engine loaded")
    whisper_enabled = True
except ImportError as e:
    print(f"⚠️  Whisper STT not available: {e}")
    whisper_enabled = False

# Initialize translator, TTS, and Whisper globally
translator = UnifiedTranslator()
if tts_enabled:
    tts_engine = TTSEngine()
if whisper_enabled:
    whisper_stt = WhisperSTT(model_size="base")

# Language options - Expanded for production (50+ languages)
# NLLB-200 supports 200 languages, showing the most commonly used ones

NLLB_LANGUAGES = {
    # Core European Languages
    "German": "de",
    "English": "en",
    "French": "fr",
    "Italian": "it",
    "Spanish": "es",
    "Portuguese": "pt",

    # Major World Languages
    "Russian": "ru",
    "Chinese": "zh",
    "Hindi": "hi",
    "Arabic": "ar",
    "Japanese": "ja",
    "Korean": "ko",

    # Additional European Languages
    "Dutch": "nl",
    "Polish": "pl",
    "Czech": "cs",
    "Swedish": "sv",
    "Danish": "da",
    "Norwegian": "no",
    "Finnish": "fi",
    "Greek": "el",
    "Turkish": "tr",
    "Hungarian": "hu",
    "Romanian": "ro",

    # Major Asian Languages
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Malay": "ms",
    "Tamil": "ta",
    "Bengali": "bn",
    "Urdu": "ur",
    "Persian": "fa",
    "Hebrew": "he",

    # African Languages
    "Swahili": "sw",
    "Amharic": "am",
    "Hausa": "ha",
    "Yoruba": "yo",

    # Regional European Languages
    "Catalan": "ca",
    "Galician": "gl",
    "Basque": "eu",

    # Slavic Languages
    "Ukrainian": "uk",
    "Bulgarian": "bg",
    "Serbian": "sr",
    "Croatian": "hr",
    "Slovak": "sk",
    "Slovenian": "sl",

    # Baltic & Other European
    "Albanian": "sq",
    "Macedonian": "mk",
    "Lithuanian": "lt",
    "Latvian": "lv",
    "Estonian": "et",
    "Icelandic": "is"
}

# Apertus-8B Specialist Languages (Swiss & Low-Resource Languages)
APERTUS_LANGUAGES = {
    # Romansh Variants (Swiss)
    "Romansh Sursilvan": "rm-sursilv",
    "Romansh Vallader": "rm-vallader",
    "Romansh Puter": "rm-puter",
    "Romansh Surmiran": "rm-surmiran",
    "Romansh Sutsilvan": "rm-sutsilv",
    "Rumantsch Grischun": "rm-rumgr",

    # Other Low-Resource Languages supported by Apertus
    "Occitan": "oc",
    "Breton": "br",
    "Welsh": "cy",
    "Scottish Gaelic": "gd",
    "Irish": "ga",
    "Luxembourgish": "lb",
    "Friulian": "fur",
    "Ladin": "lld",
    "Sardinian": "sc"
}

# Keep backward compatibility
ROMANSH_VARIANTS = {k: v for k, v in APERTUS_LANGUAGES.items() if k.startswith("Romansh") or k.startswith("Rumantsch")}
COMMON_LANGUAGES = NLLB_LANGUAGES  # For backward compatibility

# Languages with TTS support (MMS-TTS subset)
# Note: Not all languages have MMS-TTS models - only including confirmed ones
TTS_LANGUAGES = {
    # Core languages with MMS-TTS support
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Portuguese": "pt",
    "Russian": "ru",
    "Hindi": "hi",
    "Arabic": "ar",
    "Korean": "ko",

    # Additional European languages with TTS
    "Dutch": "nl",
    "Polish": "pl",
    "Czech": "cs",
    "Swedish": "sv",
    "Finnish": "fi",
    "Greek": "el",
    "Turkish": "tr",
    "Hungarian": "hu",
    "Romanian": "ro",

    # Additional Asian languages with TTS
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Tamil": "ta",
    "Bengali": "bn",
    "Urdu": "ur",
    "Persian": "fa",
    "Hebrew": "he",

    # African languages with TTS
    "Swahili": "sw"
}

# Combine all languages for full translation support
ALL_LANGUAGES = {**NLLB_LANGUAGES, **APERTUS_LANGUAGES}

# Languages with STT support (Whisper supports 100+ languages)
# Including all NLLB languages + Apertus specialist languages
STT_LANGUAGES = {**NLLB_LANGUAGES, **APERTUS_LANGUAGES}

ENGINE_OPTIONS = {
    "Auto (Recommended)": None,
    "NLLB-200 (Fast)": "nllb",
    "Apertus8B (Swiss Specialist)": "apertus"
}


def translate_text(text, src_lang_name, tgt_lang_name, engine_name, show_details):
    """Translate text with selected parameters."""
    if not text.strip():
        return "⚠️ Please enter text to translate", ""

    src_code = ALL_LANGUAGES.get(src_lang_name)
    tgt_code = ALL_LANGUAGES.get(tgt_lang_name)
    engine = ENGINE_OPTIONS.get(engine_name)

    if not src_code or not tgt_code:
        return "❌ Invalid language selection", ""

    # Perform translation
    result = translator.translate(text, src_code, tgt_code, engine=engine)

    if "error" in result:
        return f"❌ Translation Error:\n{result['error']}", ""

    translation = result.get("translation", "")

    # Build details string
    details = ""
    if show_details:
        details = f"""
**Translation Details:**
- **Engine**: {result.get('engine', 'Unknown')}
- **Model**: {result.get('model', 'Unknown')}
- **Time**: {result.get('total_time', result.get('time', 'Unknown'))}
- **Device**: {result.get('device', 'Unknown')}
        """

    return translation, details


def batch_translate(file_content, src_lang_name, tgt_lang_name):
    """Batch translate lines from uploaded file."""
    if not file_content:
        return "⚠️ Please upload a text file"

    src_code = ALL_LANGUAGES.get(src_lang_name)
    tgt_code = ALL_LANGUAGES.get(tgt_lang_name)

    lines = file_content.strip().split('\n')
    translations = []

    for i, line in enumerate(lines, 1):
        if not line.strip():
            translations.append("")
            continue

        result = translator.translate(line.strip(), src_code, tgt_code)

        if "error" in result:
            translations.append(f"[ERROR: {result['error']}]")
        else:
            translations.append(result.get("translation", ""))

    return "\n".join(translations)


def transcribe_audio_multilang(audio_file, src_lang_name="Romansh Sursilvan"):
    """Transcribe audio to text using Whisper (general languages) or wav2vec2 (Romansh)."""
    if audio_file is None:
        return "⚠️ Please upload an audio file"

    try:
        src_code = STT_LANGUAGES.get(src_lang_name)

        # Check if Romansh variant - use wav2vec2
        if src_code and src_code.startswith('rm'):
            print(f"🎤 Using wav2vec2 for Romansh transcription...")
            # Import speech recognition libraries
            import torch
            from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
            import librosa

            # Load wav2vec2 model from Hugging Face
            model_name = "sammy786/wav2vec2-xlsr-romansh_sursilvan"
            processor = Wav2Vec2Processor.from_pretrained(model_name)
            model = Wav2Vec2ForCTC.from_pretrained(model_name)

            # Load and preprocess audio
            audio, rate = librosa.load(audio_file, sr=16000)

            # Process audio
            inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)

            with torch.no_grad():
                logits = model(inputs.input_values).logits

            # Decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = processor.batch_decode(predicted_ids)[0]

            return transcription

        # Use Whisper for other languages
        elif whisper_enabled:
            print(f"🎤 Using Whisper for {src_lang_name} transcription...")
            # Get language code for Whisper
            lang_code = None
            if src_code in ['de', 'en', 'fr', 'it', 'es', 'pt', 'ru', 'zh', 'hi', 'ar', 'ja', 'ko']:
                lang_code = src_code

            transcription = whisper_stt.transcribe(audio_file, language=lang_code)
            return transcription
        else:
            return "❌ Whisper STT not available. Install with: pip install openai-whisper"

    except ImportError as e:
        return f"❌ Missing library: {e}\nInstall with: pip install librosa transformers"
    except Exception as e:
        return f"❌ Transcription error: {str(e)}"


def transcribe_audio(audio_file):
    """Legacy function for backward compatibility - defaults to Romansh."""
    return transcribe_audio_multilang(audio_file, "Romansh Sursilvan")


def audio_to_translation(audio_file, src_lang_name, tgt_lang_name):
    """Complete STT + Translation pipeline."""
    if audio_file is None:
        return "⚠️ Please upload an audio file", ""

    # Step 1: Transcribe
    transcription = transcribe_audio_multilang(audio_file, src_lang_name)

    if transcription.startswith("❌") or transcription.startswith("⚠️"):
        return transcription, ""

    # Step 2: Translate
    src_code = STT_LANGUAGES.get(src_lang_name)
    tgt_code = ALL_LANGUAGES.get(tgt_lang_name)
    result = translator.translate(transcription, src_code, tgt_code)

    if "error" in result:
        return transcription, f"❌ Translation failed: {result['error']}"

    return transcription, result.get("translation", "")


def text_to_speech_simple(text, language_name):
    """Convert text to speech using TTS engine."""
    if not tts_enabled:
        return None, "❌ TTS engine not available"

    if not text.strip():
        return None, "⚠️ Please enter text to synthesize"

    try:
        audio_path, sample_rate = tts_engine.text_to_speech(text, language_name)
        return audio_path, f"✅ Speech synthesized successfully!\n📊 Sample rate: {sample_rate}Hz"
    except Exception as e:
        return None, f"❌ TTS Error: {str(e)}"


def translate_and_speak(text, src_lang_name, tgt_lang_name):
    """Translate text and convert to speech."""
    if not tts_enabled:
        return "", None, "❌ TTS engine not available"

    if not text.strip():
        return "", None, "⚠️ Please enter text to translate"

    # Step 1: Translate
    src_code = ALL_LANGUAGES.get(src_lang_name)
    tgt_code = ALL_LANGUAGES.get(tgt_lang_name)

    result = translator.translate(text, src_code, tgt_code)

    if "error" in result:
        return f"❌ Translation Error:\n{result['error']}", None, ""

    translation = result.get("translation", "")

    # Step 2: Text-to-Speech
    try:
        audio_path, sample_rate = tts_engine.text_to_speech(translation, tgt_lang_name)
        details = f"✅ Translation and speech synthesis complete!\n📊 Sample rate: {sample_rate}Hz"
        return translation, audio_path, details
    except Exception as e:
        return translation, None, f"⚠️ Translation succeeded but TTS failed: {str(e)}"


def audio_to_audio_pipeline(audio_file, src_lang_name, tgt_lang_name):
    """Complete pipeline: Audio (any language) → Transcription → Translation → TTS."""
    if not tts_enabled:
        return "", "", None, "❌ TTS engine not available"

    if audio_file is None:
        return "", "", None, "⚠️ Please upload an audio file"

    # Step 1: Transcribe
    transcription = transcribe_audio_multilang(audio_file, src_lang_name)

    if transcription.startswith("❌") or transcription.startswith("⚠️"):
        return transcription, "", None, ""

    # Step 2: Translate
    src_code = STT_LANGUAGES.get(src_lang_name)
    tgt_code = ALL_LANGUAGES.get(tgt_lang_name)
    result = translator.translate(transcription, src_code, tgt_code)

    if "error" in result:
        return transcription, f"❌ Translation failed: {result['error']}", None, ""

    translation = result.get("translation", "")

    # Step 3: Text-to-Speech
    try:
        audio_path, sample_rate = tts_engine.text_to_speech(translation, tgt_lang_name)
        details = f"✅ Complete pipeline successful!\n📊 Audio sample rate: {sample_rate}Hz"
        return transcription, translation, audio_path, details
    except Exception as e:
        return transcription, translation, None, f"⚠️ TTS failed: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="TraductAL - Multilingual Translation System", theme=gr.themes.Soft()) as demo:

    tts_status_msg = " + MMS-TTS" if tts_enabled else ""
    whisper_status_msg = " + Whisper STT" if whisper_enabled else ""

    # Count languages dynamically
    total_languages = len(ALL_LANGUAGES)
    nllb_count = len(NLLB_LANGUAGES)
    apertus_count = len(APERTUS_LANGUAGES)

    gr.Markdown(f"""
    # 🌍 TraductAL - Multilingual Translation System

    **Unified translation engine: NLLB-200 (200 languages) + Apertus8B (1,811 languages){tts_status_msg}{whisper_status_msg}**

    **Available in interface**: {total_languages} languages ({nllb_count} NLLB + {apertus_count} Apertus specialist languages)
    - **NLLB-200**: Major world languages (50+ most common)
    - **Apertus-8B**: Swiss languages (6 Romansh variants) + Low-resource languages

    **Capabilities**: Text Translation • Multi-language Speech-to-Text (100+ languages) • Text-to-Speech ({len(TTS_LANGUAGES)} languages) • Audio-to-Audio
    """)

    with gr.Tabs():
        # Tab 1: Text Translation
        with gr.TabItem("📝 Text Translation"):
            gr.Markdown("### Translate text between languages")

            with gr.Row():
                with gr.Column():
                    src_lang = gr.Dropdown(
                        choices=sorted(list(ALL_LANGUAGES.keys())),
                        value="German",
                        label="Source Language",
                        filterable=True
                    )
                    input_text = gr.Textbox(
                        lines=6,
                        placeholder="Enter text to translate...",
                        label="Input Text"
                    )

                with gr.Column():
                    tgt_lang = gr.Dropdown(
                        choices=sorted(list(ALL_LANGUAGES.keys())),
                        value="Romansh Sursilvan",
                        label="Target Language",
                        filterable=True
                    )
                    output_text = gr.Textbox(
                        lines=6,
                        label="Translation"
                    )

            with gr.Row():
                engine_choice = gr.Radio(
                    choices=list(ENGINE_OPTIONS.keys()),
                    value="Auto (Recommended)",
                    label="Translation Engine"
                )
                show_details = gr.Checkbox(
                    value=True,
                    label="Show translation details"
                )

            translate_btn = gr.Button("🌍 Translate", variant="primary", size="lg")

            details_output = gr.Markdown(label="Details")

            # Example translations
            gr.Markdown("### 💡 Try these examples:")
            gr.Examples(
                examples=[
                    ["Guten Tag! Wie geht es Ihnen?", "German", "Romansh Sursilvan"],
                    ["Willkommen in der Schweiz", "German", "Romansh Sursilvan"],
                    ["Bonjour, comment allez-vous?", "French", "Romansh Vallader"],
                    ["Hello, how are you?", "English", "Rumantsch Grischun"],
                    ["Buongiorno, come sta?", "Italian", "Romansh Puter"],
                ],
                inputs=[input_text, src_lang, tgt_lang]
            )

            translate_btn.click(
                fn=translate_text,
                inputs=[input_text, src_lang, tgt_lang, engine_choice, show_details],
                outputs=[output_text, details_output]
            )

        # Tab 2: Batch Translation
        with gr.TabItem("📄 Batch Translation"):
            gr.Markdown("### Translate multiple lines from a file")
            gr.Markdown("Upload a text file with one sentence per line")

            with gr.Row():
                with gr.Column():
                    batch_src_lang = gr.Dropdown(
                        choices=sorted(list(ALL_LANGUAGES.keys())),
                        value="German",
                        label="Source Language",
                        filterable=True
                    )
                    batch_file = gr.Textbox(
                        lines=10,
                        placeholder="Paste text here (one line per sentence) or upload file below...",
                        label="Input Text"
                    )
                    upload_file = gr.File(
                        label="Or upload .txt file",
                        file_types=[".txt"]
                    )

                with gr.Column():
                    batch_tgt_lang = gr.Dropdown(
                        choices=sorted(list(ALL_LANGUAGES.keys())),
                        value="Romansh Sursilvan",
                        label="Target Language",
                        filterable=True
                    )
                    batch_output = gr.Textbox(
                        lines=10,
                        label="Translations"
                    )

            batch_btn = gr.Button("🌍 Translate All", variant="primary", size="lg")

            def load_file_content(file):
                if file is None:
                    return ""
                with open(file.name, 'r', encoding='utf-8') as f:
                    return f.read()

            upload_file.change(
                fn=load_file_content,
                inputs=[upload_file],
                outputs=[batch_file]
            )

            batch_btn.click(
                fn=batch_translate,
                inputs=[batch_file, batch_src_lang, batch_tgt_lang],
                outputs=[batch_output]
            )

        # Tab 3: Speech to Text (STT) - Multi-language with Whisper
        with gr.TabItem("🎤 Speech to Text (STT)"):
            gr.Markdown("### Transcribe audio to text (100+ languages)")
            gr.Markdown("Upload audio file or record directly")

            with gr.Row():
                with gr.Column():
                    stt_src_lang = gr.Dropdown(
                        choices=sorted(list(STT_LANGUAGES.keys())),
                        value="English",
                        label="Audio Language",
                        filterable=True
                    )
                    audio_input = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Audio Input"
                    )
                    transcribe_btn = gr.Button("📝 Transcribe", variant="primary")

                with gr.Column():
                    transcription_output = gr.Textbox(
                        lines=8,
                        label="Transcription"
                    )

            gr.Markdown("""
            **STT Engines**:
            - **Whisper** (OpenAI open-source): 100+ languages including English, German, French, Spanish, Italian, Russian, Hindi, Arabic, Chinese, Japanese, Korean
            - **wav2vec2**: Romansh Sursilvan specialist

            The system automatically selects the appropriate engine based on the source language.
            """)

            transcribe_btn.click(
                fn=transcribe_audio_multilang,
                inputs=[audio_input, stt_src_lang],
                outputs=[transcription_output]
            )

        # Tab 4: Audio Translation Pipeline - Multi-language
        with gr.TabItem("🎤→🌍 Audio Translation"):
            gr.Markdown("### Complete pipeline: Audio (any language) → Transcription → Translation")
            gr.Markdown("Upload audio in any language and get automatic translation")

            with gr.Row():
                with gr.Column():
                    audio_src_lang = gr.Dropdown(
                        choices=sorted(list(STT_LANGUAGES.keys())),
                        value="Romansh Sursilvan",
                        label="Audio Language",
                        filterable=True
                    )
                    audio_input_2 = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Audio Input"
                    )
                    audio_tgt_lang = gr.Dropdown(
                        choices=sorted(list(ALL_LANGUAGES.keys())),
                        value="German",
                        label="Translate to",
                        filterable=True
                    )
                    audio_translate_btn = gr.Button("🎤→🌍 Transcribe & Translate", variant="primary")

                with gr.Column():
                    audio_transcription = gr.Textbox(
                        lines=4,
                        label="1️⃣ Transcription"
                    )
                    audio_translation = gr.Textbox(
                        lines=4,
                        label="2️⃣ Translation"
                    )

            gr.Markdown("""
            **Use cases**:
            - Transcribe and translate Romansh radio broadcasts
            - Convert English podcasts to German text
            - Translate Russian news to French
            - Process Hindi audio to Arabic text
            - Any language combination supported
            """)

            audio_translate_btn.click(
                fn=audio_to_translation,
                inputs=[audio_input_2, audio_src_lang, audio_tgt_lang],
                outputs=[audio_transcription, audio_translation]
            )

        # Tab 5: Text-to-Speech (TTS)
        if tts_enabled:
            with gr.TabItem("🔊 Text-to-Speech"):
                gr.Markdown("### Convert text to natural speech")
                gr.Markdown("Generate audio from text in any supported language")

                with gr.Row():
                    with gr.Column():
                        tts_text = gr.Textbox(
                            lines=6,
                            placeholder="Enter text to convert to speech...",
                            label="Input Text"
                        )
                        tts_language = gr.Dropdown(
                            choices=sorted(list(TTS_LANGUAGES.keys())),
                            value="English",
                            label="Speech Language",
                            filterable=True
                        )
                        tts_btn = gr.Button("🔊 Generate Speech", variant="primary", size="lg")

                    with gr.Column():
                        tts_audio_output = gr.Audio(
                            label="Generated Speech",
                            type="filepath"
                        )
                        tts_status = gr.Textbox(
                            lines=3,
                            label="Status"
                        )

                gr.Markdown("### 💡 Try these examples:")
                gr.Examples(
                    examples=[
                        ["Hello! Welcome to the TraductAL translation system.", "English"],
                        ["Guten Tag! Willkommen im TraductAL Übersetzungssystem.", "German"],
                        ["Bonjour! Bienvenue dans le système de traduction TraductAL.", "French"],
                        ["Buongiorno! Benvenuti nel sistema di traduzione TraductAL.", "Italian"],
                        ["¡Hola! Bienvenido al sistema de traducción TraductAL.", "Spanish"],
                    ],
                    inputs=[tts_text, tts_language]
                )

                tts_btn.click(
                    fn=text_to_speech_simple,
                    inputs=[tts_text, tts_language],
                    outputs=[tts_audio_output, tts_status]
                )

        # Tab 6: Translation + TTS
        if tts_enabled:
            with gr.TabItem("🌍→🔊 Translate & Speak"):
                gr.Markdown("### Translate text and convert to speech")
                gr.Markdown("Complete pipeline: Text translation + audio generation")

                with gr.Row():
                    with gr.Column():
                        translate_tts_src_lang = gr.Dropdown(
                            choices=sorted(list(ALL_LANGUAGES.keys())),
                            value="German",
                            label="Source Language",
                            filterable=True
                        )
                        translate_tts_text = gr.Textbox(
                            lines=6,
                            placeholder="Enter text to translate and speak...",
                            label="Input Text"
                        )

                    with gr.Column():
                        translate_tts_tgt_lang = gr.Dropdown(
                            choices=sorted(list(TTS_LANGUAGES.keys())),
                            value="English",
                            label="Target Language (with speech)",
                            filterable=True
                        )
                        translate_tts_translation = gr.Textbox(
                            lines=6,
                            label="Translation"
                        )

                translate_tts_btn = gr.Button("🌍→🔊 Translate & Speak", variant="primary", size="lg")

                translate_tts_audio = gr.Audio(
                    label="Generated Speech",
                    type="filepath"
                )
                translate_tts_status = gr.Textbox(
                    lines=2,
                    label="Status"
                )

                gr.Markdown("""
                **Use case**: Perfect for creating spoken translations, language learning,
                or generating audio content in multiple languages.
                """)

                translate_tts_btn.click(
                    fn=translate_and_speak,
                    inputs=[translate_tts_text, translate_tts_src_lang, translate_tts_tgt_lang],
                    outputs=[translate_tts_translation, translate_tts_audio, translate_tts_status]
                )

        # Tab 7: Complete Audio Pipeline (Audio → Audio) - Multi-language
        if tts_enabled:
            with gr.TabItem("🎤→🔊 Audio to Audio"):
                gr.Markdown("### Complete audio pipeline: Audio (any language) → Transcription → Translation → Speech")
                gr.Markdown("Upload audio in any language and get spoken translation in target language")

                with gr.Row():
                    with gr.Column():
                        pipeline_src_lang = gr.Dropdown(
                            choices=sorted(list(STT_LANGUAGES.keys())),
                            value="Romansh Sursilvan",
                            label="Audio Language",
                            filterable=True
                        )
                        pipeline_audio_input = gr.Audio(
                            sources=["upload", "microphone"],
                            type="filepath",
                            label="Audio Input"
                        )
                        pipeline_tgt_lang = gr.Dropdown(
                            choices=sorted(list(TTS_LANGUAGES.keys())),
                            value="German",
                            label="Target Language (with speech)",
                            filterable=True
                        )
                        pipeline_btn = gr.Button("🎤→🔊 Complete Pipeline", variant="primary", size="lg")

                    with gr.Column():
                        pipeline_transcription = gr.Textbox(
                            lines=3,
                            label="1️⃣ Transcription"
                        )
                        pipeline_translation = gr.Textbox(
                            lines=3,
                            label="2️⃣ Translation"
                        )
                        pipeline_audio_output = gr.Audio(
                            label="3️⃣ Generated Speech",
                            type="filepath"
                        )
                        pipeline_status = gr.Textbox(
                            lines=2,
                            label="Status"
                        )

                gr.Markdown("""
                **Use cases**:
                - Translate Romansh radio broadcasts to spoken German/French/English
                - Convert English podcasts to spoken Spanish
                - Transform Russian news audio to spoken French
                - Process Hindi audio to spoken Arabic
                - Any combination of supported languages

                **Example workflow**: Upload English audio → Get spoken Hindi translation
                """)

                pipeline_btn.click(
                    fn=audio_to_audio_pipeline,
                    inputs=[pipeline_audio_input, pipeline_src_lang, pipeline_tgt_lang],
                    outputs=[pipeline_transcription, pipeline_translation, pipeline_audio_output, pipeline_status]
                )

        # Tab 8: About & Info
        with gr.TabItem("ℹ️ About"):
            gr.Markdown("""
            ## About TraductAL

            ### 🎯 System Overview

            This application combines two state-of-the-art translation engines:

            #### 1. **NLLB-200** (Meta AI)
            - 200 languages supported
            - Seq2seq architecture
            - Fast inference (0.5-2s per sentence)
            - Best for common language pairs

            #### 2. **Apertus8B** (Swiss AI - ETH Zurich & EPFL)
            - 1,811 languages supported
            - Specialized for Swiss languages
            - All 6 Romansh variants
            - Released September 2025
            - 8B parameters, fully open source

            ### 🇨🇭 Romansh Support

            **Supported Variants:**
            - Sursilvan (55% of speakers)
            - Vallader (20%)
            - Puter (12%)
            - Surmiran (10%)
            - Sutsilvan (3%)
            - Rumantsch Grischun (official standard)

            ### 🎤 Speech Recognition (STT)

            **Multi-language support with automatic engine selection:**

            #### Whisper (OpenAI open-source)
            - 100+ languages supported
            - Automatic language detection
            - High-quality transcription
            - Model: whisper-base (74M parameters)
            - Languages: English, German, French, Italian, Spanish, Portuguese, Russian, Hindi, Arabic, Chinese, Japanese, Korean, and many more

            #### wav2vec2-xlsr-romansh_sursilvan
            - Romansh Sursilvan specialist
            - Fine-tuned on Mozilla Common Voice 8.0
            - WER: 13.82% | CER: 3.02%
            - Used automatically for Romansh audio

            ### 📊 Dataset

            **Training Data**: swiss-ai/apertus-posttrain-romansh
            - 46,092 German-Romansh parallel sentences
            - Dictionary translations, idioms, instructions
            - CC-BY-4.0 License

            ### 🔒 Privacy

            - 100% offline processing
            - No data sent to external servers
            - All models run locally
            - GDPR compliant

            ### 📚 Resources

            - **Apertus8B**: [huggingface.co/swiss-ai/Apertus-8B-2509](https://huggingface.co/swiss-ai/Apertus-8B-2509)
            - **NLLB-200**: [huggingface.co/facebook/nllb-200-1.3B](https://huggingface.co/facebook/nllb-200-1.3B)
            - **Dataset**: [huggingface.co/datasets/swiss-ai/apertus-posttrain-romansh](https://huggingface.co/datasets/swiss-ai/apertus-posttrain-romansh)

            ---

            **Version**: 1.0.0 | **License**: Apache 2.0
            """)

    gr.Markdown("""
    ---
    💡 **Tip**: The system automatically selects the best engine - Apertus8B for Romansh translations,
    NLLB-200 for other language pairs.
    """)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌍 TraductAL - Multilingual Translation System")
    print("="*60)
    print("🚀 Starting Gradio interface...")
    print("📡 Server will be available at: http://localhost:7860")
    print("="*60 + "\n")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
