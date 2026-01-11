# Authorship and Attribution - TraductAL System

**Version**: 1.0
**Date**: January 2026
**Purpose**: Clear documentation of authorship for research and teaching contexts

---

## Executive Summary

The TraductAL multilingual translation system is a **collaborative work** combining:
1. **Original research and implementation** by the author (human researcher)
2. **AI-assisted development** by Claude Code (Anthropic)
3. **Third-party open-source models and frameworks**

This document provides transparent attribution for academic integrity, reproducibility, and proper citation in research and educational contexts.

---

## 🎓 Original Human Authorship (Core Intellectual Contribution)

### 1. Linguistic Framework & Theoretical Foundation

**Author**: Rogaton (pseudonym)
**Credentials**:
- Master's in French Language and Literature, University of Geneva (1984)
- Master's in Computational Linguistics, University of Geneva (1991)
- Master's in Computer Science, Swiss Federal Institute of Technology (EPFL, 1996)
- Member: Association for Computational Linguistics (ACL)
- Life Member: Association for Computing Machinery (ACM)

**Based on**: Master's Degree Dissertation in Computational Linguistics (1989-1991)
**Original Work**: French 2L Error Detection Parser using DCG Formalism

#### Core Contributions:
- **DCG Grammar Rules** (`glossary_parser/grammar.pl`)
  - Linguistic analysis and rule design
  - Part-of-speech tagging strategies
  - Syntactic structure definitions
  - Notation and dialect marker parsing
  - Multi-line entry handling

- **Lexicon Architecture** (`glossary_parser/lexicon.pl`)
  - Lexical categorization framework
  - Morphological analysis rules
  - Language-specific patterns

- **Coptic Dependency Parser** (External: `~/copticNLP/coptic-dependency-parser/`)
  - Complete dependency grammar for Coptic
  - Based on CopticScriptorium corpus analysis
  - Original linguistic research

#### Intellectual Property:
- ✅ **Fully original**: Grammar design, linguistic rules, theoretical framework
- ✅ **Research-based**: Grounded in computational linguistics methodology
- ✅ **Academic contribution**: Suitable for citation in scholarly work

**Citation Format:**
```
Rogaton. (1991). French 2L Error Detection Parser using Definite Clause
Grammar Formalism. Master's Thesis in Computational Linguistics, University of Geneva.

Rogaton. (2025-2026). TraductAL: Hybrid Neural-Symbolic Translation System
with DCG-based Validation. Research Project.
```

**Note on Pseudonymity**: Rogaton is a pseudonym. Real identity available on request for academic collaboration, grants, and formal publications.

---

## 🤖 AI-Assisted Development (Implementation & Integration)

### 2. System Architecture & Integration Code

**AI Assistant**: Claude Code (Anthropic's Claude Sonnet 4.5)
**Role**: Code generation, integration, documentation, debugging
**Period**: December 2025 - January 2026

#### AI-Generated Components:

##### A. **Python Integration Layer**
- `apertus_translator.py` - Apertus-8B wrapper
- `unified_translator.py` - Multi-engine orchestration
- `apertus_trealla_hybrid.py` - Neural-symbolic integration
- `whisper_stt.py` - Speech-to-text wrapper
- `tts_engine.py` - Text-to-speech wrapper
- `glossary_parser/trealla_interface.py` - Python-Prolog bridge
- `gradio_app.py` - Web interface
- `batch_news_translator.py` - Batch processing

**AI Contribution**: Implementation, error handling, API design, integration logic

##### B. **Documentation**
- `README.md` - System documentation
- `BATCH_TRANSLATION_EXAMPLES.md` - Usage examples
- `APERTUS_TREALLA_INTEGRATION.md` - Architecture documentation
- `INTEGRATION_ARCHITECTURE.md` - System design
- `MULTIMODAL_GUIDE.md` - Feature guides
- `SWISS_FRENCH_*.md` - Project documentation
- This file (`AUTHORSHIP_AND_ATTRIBUTION.md`)

**AI Contribution**: Technical writing, examples, tutorials, troubleshooting guides

##### C. **Infrastructure & Utilities**
- `start_gradio.sh` - Launch script
- `translate_enhanced.sh` - CLI wrapper
- `setup_janus.sh` - Prolog installation
- `download_romansh_dataset.py` - Data utilities
- Configuration and deployment scripts

**AI Contribution**: DevOps, automation, user experience

##### D. **Integration Glue Code**
All code interfacing between:
- Human-authored Prolog parsers ↔ Python
- Translation models ↔ Application logic
- User interfaces ↔ Backend engines
- Speech components ↔ Translation pipeline

**AI Contribution**: System integration, error handling, data flow

#### AI Methodology:
- **Code generation**: Based on requirements and existing patterns
- **Documentation**: Structured from code analysis and user feedback
- **Debugging**: Interactive problem-solving with human oversight
- **Refactoring**: Code optimization and organization

**Important Notes:**
1. **AI did NOT create**: Grammar rules, linguistic theory, lexicon design
2. **AI assisted with**: Implementation, integration, documentation
3. **AI role**: Tool for rapid development, not source of linguistic knowledge
4. **Human oversight**: All AI-generated code reviewed and validated

---

## 🌐 Third-Party Components (Open Source)

### 3. Pre-trained Models & Frameworks

#### Translation Models:
- **NLLB-200** (Meta AI)
  - License: CC-BY-NC 4.0
  - Citation: [Meta AI, 2022]
  - Role: Neural machine translation (200+ languages)

- **Apertus-8B** (Open Source)
  - License: Apache 2.0
  - Repository: HuggingFace (`apertus-8b`)
  - Role: Low-resource language translation (1811 languages)

#### Speech Models:
- **Whisper** (OpenAI)
  - License: MIT
  - Citation: [Radford et al., 2022]
  - Role: Speech-to-text (99 languages)

- **MMS-TTS** (Facebook)
  - License: CC-BY-NC 4.0
  - Citation: [Meta AI, 2023]
  - Role: Text-to-speech synthesis

#### Frameworks:
- **PyTorch** (Facebook/Meta)
- **Transformers** (HuggingFace)
- **Gradio** (HuggingFace)
- **Trealla Prolog** (Andrew Davison, MIT License)

#### Datasets:
- **Romansh Dataset** (HuggingFace)
- **CopticScriptorium** (Coptic text corpora)
- **Glossaire Vaudois** (1861, Canton de Vaud)

---

## 📋 Detailed Component Attribution

### File-by-File Breakdown

| Component | Primary Author | AI Assistance | Notes |
|-----------|---------------|---------------|-------|
| **Prolog Grammars** | | | |
| `glossary_parser/grammar.pl` | **100% Human** | 0% | Original linguistic research |
| `glossary_parser/lexicon.pl` | **100% Human** | 0% | Original lexical design |
| `coptic_parser_master.pl` | **100% Human** | 0% | External project, original research |
| | | | |
| **Python Integration** | | | |
| `apertus_translator.py` | 5% Human (specs) | **95% AI** | Implementation |
| `unified_translator.py` | 5% Human (specs) | **95% AI** | Implementation |
| `apertus_trealla_hybrid.py` | 20% Human (design) | **80% AI** | Integration logic |
| `trealla_interface.py` | 10% Human (specs) | **90% AI** | Bridge implementation |
| `whisper_stt.py` | 5% Human (specs) | **95% AI** | Wrapper implementation |
| `tts_engine.py` | 5% Human (specs) | **95% AI** | Wrapper implementation |
| `gradio_app.py` | 10% Human (requirements) | **90% AI** | UI implementation |
| `batch_news_translator.py` | 5% Human (specs) | **95% AI** | Utility implementation |
| | | | |
| **Shell Scripts** | | | |
| `start_gradio.sh` | 0% Human | **100% AI** | Automation |
| `translate_enhanced.sh` | 0% Human | **100% AI** | CLI wrapper |
| `setup_janus.sh` | 0% Human | **100% AI** | Installation |
| | | | |
| **Documentation** | | | |
| `README.md` | 30% Human (content) | **70% AI** | Technical writing |
| `BATCH_TRANSLATION_EXAMPLES.md` | 10% Human (requirements) | **90% AI** | Tutorial writing |
| `*_GUIDE.md` files | 15% Human (structure) | **85% AI** | Documentation |
| `AUTHORSHIP_AND_ATTRIBUTION.md` | 40% Human (requirements) | **60% AI** | This document |
| | | | |
| **Third-Party** | | | |
| NLLB-200 models | Meta AI | - | Pre-trained |
| Apertus-8B model | Apertus Team | - | Pre-trained |
| Whisper model | OpenAI | - | Pre-trained |
| MMS-TTS model | Meta AI | - | Pre-trained |

### Key Interpretation:
- **100% Human**: Original intellectual contribution, no AI assistance
- **AI Percentage**: Implementation code generated by AI
- **Human Percentage**: Requirements, design decisions, validation, linguistic knowledge

---

## 🎯 For Academic Citation

### How to Cite Different Aspects

#### 1. Citing the DCG Parser (Original Research)
```
Rogaton. (2025). DCG-based Glossary Parser for Swiss French Dialects.
In TraductAL Multilingual Translation System. [Implementation based on
Master's thesis work, 1989-1991].
```

#### 2. Citing the Complete System
```
Rogaton. (2025-2026). TraductAL: A Hybrid Neural-Symbolic Translation
System for Swiss Languages. Research Project. [System implementation with
AI-assisted development using Claude Code (Anthropic)].
```

#### 3. Citing the Integration Architecture
```
Rogaton and Claude Code (AI Assistant). (2026). Neural-Symbolic
Integration Architecture for Low-Resource Language Translation.
Technical Implementation in TraductAL System.
```

#### 4. For Research Papers
```latex
\section{Authorship and AI Assistance}
The TraductAL system combines original linguistic research with AI-assisted
implementation. The core DCG grammar rules and lexicon (grammar.pl, lexicon.pl)
represent original work by [Author] based on computational linguistics research
(1989-1991). System integration, Python wrappers, and documentation were
developed with assistance from Claude Code (Anthropic), an AI coding assistant.
The translation models (NLLB-200, Apertus-8B) are third-party open-source
components. For detailed attribution, see AUTHORSHIP_AND_ATTRIBUTION.md.
```

---

## 🏛️ For Teaching & Educational Use

### Transparency Statement for Students

When using TraductAL in educational contexts, inform students:

1. **Original Research Component**:
   - The Prolog DCG grammars represent genuine human linguistic research
   - These demonstrate classical computational linguistics methodology
   - Suitable for studying grammar formalism and linguistic analysis

2. **AI-Assisted Development**:
   - Most Python integration code was generated by AI (Claude Code)
   - This represents modern software development practices
   - Demonstrates human-AI collaboration in research software

3. **Learning Value**:
   - **Human contribution**: Linguistic theory, grammar design, research methodology
   - **AI contribution**: Rapid implementation, integration, documentation
   - **Combined result**: Functional research tool in limited time

### Recommended Disclosure
```
This system demonstrates a hybrid development approach:
- Linguistic core: Human research (Master's level computational linguistics)
- System implementation: AI-assisted development (Claude Code)
- External models: Open-source ML models (Meta, OpenAI, etc.)

This approach is increasingly common in research software development
and represents a valid modern methodology when properly attributed.
```

---

## ⚖️ Legal & Ethical Considerations

### Copyright & Licensing

#### Human-Authored Components
- **Grammar & Lexicon files**: © Rogaton, All Rights Reserved (MIT License for TraductAL distribution)
- **Coptic Parser**: © Rogaton (if applicable)
- Can be licensed separately for academic or commercial use

#### AI-Assisted Components
- **Python integration code**: Generated by AI, reviewed/validated by human
- **Documentation**: Co-created (human requirements + AI writing)
- Recommended license: MIT or Apache 2.0 for maximum research utility

#### Third-Party Components
- Respect individual licenses (see above)
- NLLB-200: Non-commercial only (CC-BY-NC)
- Apertus-8B: Permissive (Apache 2.0)

### Ethical Disclosure

For **research publication**:
```
DISCLOSURE: This research software was developed using a hybrid methodology
combining human linguistic expertise with AI-assisted coding (Claude Code,
Anthropic). The core linguistic components (DCG grammar, lexicon) represent
original human research. System integration and documentation were developed
with AI assistance. All AI-generated code was reviewed and validated by the
author. This disclosure follows emerging best practices for AI-assisted
research software development.
```

For **grant applications**:
```
The proposed system builds on original linguistic research (DCG-based parser,
Rogaton, 1989-1991) with modern implementation using AI-assisted development
tools. The intellectual contribution lies in the linguistic framework and system
design; implementation leverages contemporary AI coding assistants for efficiency.
This approach aligns with responsible AI use in research contexts.
```

---

## 🔍 Verification & Reproducibility

### How Others Can Verify Attribution

1. **Grammar/Lexicon Originality**:
   - Review `grammar.pl` and `lexicon.pl` - pure Prolog DCG
   - Compare with author's academic background and thesis work
   - Linguistic sophistication reflects human expertise

2. **AI-Generated Code Patterns**:
   - Modern Python idioms and comprehensive documentation
   - Consistent style across files
   - Rapid development timeline (weeks vs. months)

3. **Third-Party Components**:
   - Clear model downloads from HuggingFace
   - Standard framework usage (PyTorch, Transformers)
   - Documented dependencies

### Git History Recommendation
```bash
# Maintain clear commit messages
git log --oneline

# Example commit messages:
# "Add original DCG grammar (human-authored, 1989-1991 research)"
# "Integrate Apertus-8B with Python wrapper (AI-assisted)"
# "Update documentation with usage examples (AI-generated)"
```

---

## 📞 Contact & Questions

For questions about:
- **Linguistic components**: Contact Rogaton at relanir@bluewin.ch
- **System implementation**: Refer to this document and code comments
- **Third-party models**: See respective project documentation
- **Academic collaboration**: Contact Rogaton at relanir@bluewin.ch
- **Real identity**: Available on request for serious academic collaboration

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 2026 | Initial authorship documentation |

---

## Summary: What to Tell Users

**Short Answer**:
> "The linguistic core (Prolog DCG grammar and lexicon) is my original research from my Master's in Computational Linguistics (1989-1991). The system integration, Python code, and documentation were developed with AI assistance (Claude Code by Anthropic) to rapidly build a functional research tool. The translation models are open-source third-party components (Meta, OpenAI, etc.)."

**For Academic Contexts**:
> "This is human-led research with AI-assisted implementation - a valid modern methodology when transparently disclosed. The intellectual contribution is the linguistic framework; AI accelerated the software engineering. All components are clearly attributed for proper citation."

**For Students**:
> "This demonstrates collaborative human-AI development. I provided the linguistic expertise and research foundation; AI helped with coding and documentation. Learn from both: the linguistic theory (human) and the implementation patterns (AI-assisted)."

**For Reviewers/Evaluators**:
> "Please see AUTHORSHIP_AND_ATTRIBUTION.md for complete transparency. Core linguistic work is 100% human original research. Implementation leverages AI tools responsibly. This approach is increasingly standard in research software development."

---

**Recommendation**: Include this file in all distributions and reference it prominently in README.md, academic papers, and teaching materials.
