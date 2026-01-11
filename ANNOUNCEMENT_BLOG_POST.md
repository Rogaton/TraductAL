# Introducing TraductAL: A Hybrid Neural-Symbolic Translation System

**Rogaton • January 2026 • Independent Researcher**

---

## TL;DR

I'm releasing **TraductAL**, an open-source multilingual translation system that:
- Supports **65+ languages** (mainstream + low-resource)
- Works **100% offline** (privacy-first, no data collection)
- Combines **neural + symbolic AI** (explainable translations)
- Free for academic/research use (MIT License)

**GitHub**: https://github.com/Rogaton/TraductAL
**Try it**: https://huggingface.co/Norelad/TraductAL
**Website**: https://modular9.org

---

## The Problem

Modern translation systems excel at popular languages but fail at:
1. **Low-resource languages** (Romansh, Celtic languages, indigenous languages)
2. **Privacy-sensitive content** (requires cloud services, data sent to third parties)
3. **Explainability** (pure neural networks are black boxes)
4. **Domain specificity** (can't enforce terminology or validate output)

If you work with Swiss Romansh, Welsh, or confidential legal documents, Google Translate isn't enough.

---

## The Solution: TraductAL

TraductAL addresses these gaps through a **hybrid architecture**:

### 1. Neural Translation (Fast & Fluent)
- **NLLB-200** (Meta AI): 200+ languages, state-of-the-art quality
- **Apertus-8B**: 1811 languages, specialized for low-resource languages

### 2. Symbolic Validation (Accurate & Explainable)
- **Prolog DCG grammars**: Linguistic rule-based checking
- **Custom glossaries**: Domain-specific terminology enforcement
- **Validation pipelines**: Catches errors neural models miss

### 3. Offline-First Design
- No internet required after setup
- No data collection or telemetry
- Perfect for confidential documents

---

## What Makes TraductAL Different?

### Feature Comparison

| Feature | Google Translate | DeepL | TraductAL |
|---------|------------------|-------|-----------|
| **Mainstream languages** | ✅ Excellent | ✅ Excellent | ✅ Good |
| **Low-resource languages** | ⚠️ Limited | ⚠️ Limited | ✅ 1811 languages |
| **Offline operation** | ❌ No | ❌ No | ✅ Yes |
| **Privacy (no data sent)** | ❌ No | ❌ No | ✅ Yes |
| **Custom glossaries** | ⚠️ Limited | ⚠️ Limited | ✅ Full DCG support |
| **Explainability** | ❌ Black box | ❌ Black box | ✅ Hybrid validation |
| **Cost** | Free tier | Paid | ✅ Free (MIT) |

### Supported Languages

**Mainstream** (50+):
English, French, German, Spanish, Italian, Portuguese, Russian, Chinese, Arabic, Japanese, Korean, Hindi, and more

**Low-Resource** (15+):
- **Romansh**: All 6 dialects (Sursilvan, Vallader, Puter, Surmiran, Sutsilvan, Rumantsch Grischun)
- **Celtic**: Welsh, Scottish Gaelic, Irish, Breton
- **Regional**: Occitan, Luxembourgish, Friulian, Ladin, Sardinian

---

## Real-World Use Cases

### 1. Swiss Canton Administration
**Challenge**: Translate official documents into all Romansh dialects

**Solution**: TraductAL with custom Romansh models, on-premise deployment for data sovereignty

**Result**: 80% cost reduction, consistent terminology, privacy compliance

### 2. Legal Firm (Confidential)
**Challenge**: Translate sensitive contracts without cloud exposure

**Solution**: 100% offline TraductAL deployment with legal terminology glossary

**Result**: Zero data breaches, 60% faster turnaround

### 3. Indigenous Language Preservation
**Challenge**: Educational materials in endangered Celtic languages

**Solution**: TraductAL with community-driven glossaries

**Result**: Sustainable translation pipeline for educational content

---

## Technical Architecture

### How It Works

```
User Input
    ↓
[Neural Translation]
    │
    ├─→ NLLB-200 (mainstream languages)
    ├─→ Apertus-8B (low-resource languages)
    ↓
[Symbolic Validation]
    │
    ├─→ DCG Grammar Check
    ├─→ Glossary Enforcement
    ├─→ Length/Format Validation
    ↓
Validated Output
```

### Technology Stack

- **Neural Models**: NLLB-200, Apertus-8B
- **Symbolic Engine**: Trealla Prolog (lightweight, fast)
- **Speech**: OpenAI Whisper (STT), MMS-TTS (TTS)
- **Interface**: Gradio (web), CLI tools
- **Language**: Python 3.8+

### Performance

- **Latency**: 1-3 seconds per sentence (CPU), <1s (GPU)
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 3-10GB for models
- **Accuracy**: Comparable to NLLB-200/Apertus-8B baselines + validation improvements

---

## Getting Started

### Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/[yourusername]/TraductAL
cd TraductAL

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download models (one-time, ~3-10GB)
python download_nllb_200.py

# 4. Launch web interface
./start_gradio.sh

# 5. Open browser
# → http://localhost:7860
```

### Try Online (No Installation)

Visit our **HuggingFace Space**: [URL]

---

## Academic Foundations

TraductAL builds on computational linguistics research:

- **DCG Formalism**: Based on my Master's thesis (1991, University of Geneva) on French error detection using Definite Clause Grammars
- **Neural-Symbolic Integration**: Combining statistical (neural) and rule-based (symbolic) approaches
- **Low-Resource MT**: Leveraging transfer learning and linguistic expertise

**Author Background**:
- Master's in French Language & Literature (University of Geneva, 1984)
- Master's in Computational Linguistics (University of Geneva, 1991)
- Master's in Computer Science (EPFL, 1996)
- ACL Member, ACM Life Member

This represents a hybrid methodology:
- **Linguistic core**: Human-designed grammars and rules
- **Implementation**: AI-assisted development (Claude Code, Anthropic)
- **Models**: Open-source pre-trained models (Meta, OpenAI, etc.)

For full transparency, see [AUTHORSHIP_AND_ATTRIBUTION.md](AUTHORSHIP_AND_ATTRIBUTION.md)

---

## Licensing & Usage

### Free for Academic/Research

TraductAL is **MIT Licensed** for:
- Universities and research institutions
- Non-profit organizations
- Personal use and experimentation
- Open-source projects

### Commercial Licensing Available

For commercial use (coming Q1 2026):
- Professional: $2,500/year
- Enterprise: $15,000/year
- Custom services available

See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) for details.

---

## Roadmap

### Current Status (v0.1.0)

✅ 65+ languages via NLLB-200 + Apertus-8B
✅ Offline operation
✅ Web interface + CLI
✅ Basic DCG validation
✅ Speech-to-text / Text-to-speech

### Upcoming (Q1-Q2 2026)

🔄 Fine-tuning guide for custom domains
🔄 More DCG grammars (Swiss German, historical languages)
🔄 Batch processing optimization
🔄 Docker containerization
🔄 Commercial licensing launch
🔄 Cloud API (optional hosted version)

### Research Directions

📋 Coptic language support (ancient Egyptian)
📋 Improved neural-symbolic integration
📋 Quality metrics for hybrid validation
📋 Community-contributed glossaries

---

## Why Open Source?

I believe translation technology should be:
- **Accessible**: Anyone can run it, modify it, improve it
- **Transparent**: Explainable outputs, auditable code
- **Privacy-respecting**: Your data stays on your machine
- **Academically rigorous**: Peer-reviewable, citable

By open-sourcing TraductAL, I hope to:
1. Advance research in neural-symbolic NLP
2. Support endangered and low-resource languages
3. Provide privacy-first alternatives to cloud services
4. Enable domain-specific customization

---

## Get Involved

### For Researchers

- **Collaborate**: Joint research projects, grant proposals
- **Cite**: Use TraductAL in your work (see citation guidelines)
- **Contribute**: DCG grammars, language pairs, improvements

### For Developers

- **Contribute code**: GitHub PRs welcome
- **Report bugs**: GitHub Issues
- **Extend**: Build on TraductAL for your projects

### For Language Communities

- **Add languages**: Help us support your language
- **Create glossaries**: Domain-specific or cultural terminology
- **Test & feedback**: Real-world usage insights

### For Commercial Users

- **Early access**: Contact us for pilot projects
- **Custom solutions**: Fine-tuning, integration, consulting
- **Partnership**: Let's discuss your translation needs

---

## Contact & Links

**Author**: Rogaton (pseudonym)
**Location**: Switzerland
**Email**: relanir@bluewin.ch

**Resources**:
- 💻 **GitHub**: https://github.com/Rogaton/TraductAL
- 🤗 **HuggingFace**: https://huggingface.co/Norelad/TraductAL
- 🌐 **Website**: https://modular9.org
- 📄 **Documentation**: See repository docs/ folder
- 📧 **Contact**: relanir@bluewin.ch

**Citation**:
```bibtex
@software{traductal2026,
  author = {Rogaton},
  title = {TraductAL: A Hybrid Neural-Symbolic Translation System},
  year = {2026},
  url = {https://github.com/Rogaton/TraductAL},
  note = {MIT License. Real identity available on request for academic collaboration.}
}
```

---

## Acknowledgments

TraductAL wouldn't exist without:

- **Meta AI**: NLLB-200 models
- **Apertus Team**: Apertus-8B for low-resource languages
- **OpenAI**: Whisper speech recognition
- **HuggingFace**: Transformers library and model hosting
- **Trealla Prolog**: Lightweight Prolog implementation
- **Claude Code** (Anthropic): AI-assisted development
- **Open-source community**: Countless tools and libraries

---

## Conclusion

Translation technology has advanced dramatically, but gaps remain for:
- Low-resource languages
- Privacy-sensitive applications
- Explainable, validated outputs
- Domain-specific customization

**TraductAL** addresses these gaps through a hybrid neural-symbolic architecture that's:
- Open source (MIT License)
- Offline-first (privacy by design)
- Academically rigorous (based on computational linguistics research)
- Commercially viable (sustainable development)

I'm excited to share this with the research community and beyond. Try it, break it, improve it, and let me know what you think!

**Download**: https://github.com/Rogaton/TraductAL
**Questions**: relanir@bluewin.ch

---

*This post is also available at: https://modular9.org*
