# 📜 Licensing & Legal Information

## ⚖️ **Complete License Overview**

This document provides comprehensive licensing information for all components of the Offline Neural Machine Translation System.

---

## 🔴 **NLLB-200 Models - Meta Platforms License**

### **Model Information**
- **Models**: NLLB-200-1.3B, NLLB-200-3.3B
- **Developer**: Meta Platforms, Inc. (formerly Facebook)
- **Copyright**: © Meta Platforms, Inc.
- **License Type**: Custom License (based on CC BY-NC 4.0)

### **License Terms Summary**
**✅ PERMITTED USES:**
- ✅ **Research and Academic Use**: Free for educational and research purposes
- ✅ **Personal Use**: Individual translation needs
- ✅ **Non-Commercial Professional Use**: Professional translators using for their work
- ✅ **Modification**: Can fine-tune and adapt models
- ✅ **Redistribution**: Can share models with proper attribution
- ✅ **Internal Business Use**: Use within organizations for internal purposes

**❌ RESTRICTED USES:**
- ❌ **Commercial Services**: Cannot sell translation services using NLLB-200
- ❌ **SaaS Products**: Cannot offer as commercial software-as-a-service
- ❌ **Competitive Products**: Cannot use to compete with Meta's services
- ❌ **Large-Scale Commercial**: Cannot use for large-scale commercial operations

### **Required Attribution**
When using or redistributing NLLB-200 models, you must include:
```
NLLB-200 Models developed by Meta AI Research
Copyright © Meta Platforms, Inc.
Licensed under Custom License for Non-Commercial Use
```

### **Commercial Licensing**
For commercial use, contact Meta Platforms:
- **Email**: opensource@meta.com
- **Website**: https://ai.meta.com/resources/models-and-libraries/
- **Process**: Request commercial license for NLLB-200 models

---

## 🟢 **Integration Framework - Open Source Components**

### **Python Scripts (Created for This Distribution)**
- **Files**: `nllb_translator.py`, `download_nllb_200.py`, `migrate_to_nllb.py`, etc.
- **License**: MIT License (see below)
- **Usage**: Freely usable for any purpose including commercial

### **MIT License for Integration Scripts**
```
MIT License

Copyright (c) 2025 Neural MT Offline Distribution

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🔵 **Third-Party Libraries**

### **Transformers Library (Hugging Face)**
- **License**: Apache License 2.0
- **Usage**: Fully commercial-friendly
- **Attribution**: © Hugging Face, Inc.
- **Website**: https://github.com/huggingface/transformers

### **PyTorch**
- **License**: BSD 3-Clause License
- **Usage**: Fully commercial-friendly
- **Attribution**: © Facebook, Inc. and its affiliates
- **Website**: https://pytorch.org/

### **SentencePiece**
- **License**: Apache License 2.0
- **Usage**: Fully commercial-friendly
- **Attribution**: © Google Inc.
- **Website**: https://github.com/google/sentencepiece

### **Other Dependencies**
All other Python libraries (numpy, json, pathlib, etc.) are under permissive licenses compatible with both commercial and non-commercial use.

---

## 📋 **Usage Guidelines by Scenario**

### **🎓 Academic & Research Use**
**Status**: ✅ **FULLY PERMITTED**
- Use all components freely
- Publish research papers
- Include in educational curricula
- Share with students and colleagues
- No restrictions or licensing fees

**Required**: Basic attribution to Meta for NLLB-200 models

### **👤 Personal Use**
**Status**: ✅ **FULLY PERMITTED**
- Translate personal documents
- Use for language learning
- Customize and modify system
- Share with friends and family
- No restrictions or licensing fees

**Required**: No special requirements

### **💼 Professional Translator Use**
**Status**: ✅ **PERMITTED** (with conditions)
- Use for translating client documents
- Integrate into personal workflows
- Customize for specific domains
- Use offline for sensitive documents

**Conditions**: 
- Cannot charge specifically for "NLLB-200 translation services"
- Can charge for translation work that happens to use NLLB-200
- Must maintain client confidentiality (system supports this)

**Required**: Basic attribution if sharing system

### **🏢 Internal Business Use**
**Status**: ✅ **PERMITTED**
- Use within organization for internal translations
- Deploy on company servers
- Integrate with internal tools
- Train employees on system

**Conditions**: Cannot offer as external service to other companies

**Required**: Basic attribution in internal documentation

### **💰 Commercial Services**
**Status**: ❌ **REQUIRES META LICENSE**
- Selling translation services using NLLB-200
- SaaS translation platforms
- API services using NLLB-200
- Large-scale commercial operations

**Solution**: Contact Meta for commercial licensing

### **🔧 Software Development**
**Status**: 🟡 **MIXED**
- ✅ Can use integration framework commercially
- ✅ Can sell setup and customization services
- ✅ Can create commercial tools around the framework
- ❌ Cannot redistribute NLLB-200 models commercially
- ❌ Cannot include NLLB-200 in commercial software packages

**Approach**: Sell the framework, let users download models themselves

---

## 🎯 **Practical Recommendations**

### **For Individual Translators**
```
✅ DO:
- Use for all your translation work
- Share setup with colleagues
- Customize for your needs
- Charge clients for your translation services

❌ DON'T:
- Advertise "NLLB-200 translation services"
- Sell the models themselves
- Create commercial APIs using NLLB-200
```

### **For Organizations**
```
✅ DO:
- Deploy internally for employee use
- Use for internal document translation
- Integrate with internal workflows
- Train staff on the system

❌ DON'T:
- Offer as external service to clients
- Include in commercial products
- Resell translation services based on NLLB-200
```

### **For Educators**
```
✅ DO:
- Use in courses and training
- Share with students
- Include in research projects
- Publish academic papers about implementation

❌ DON'T:
- Sell commercial training based solely on NLLB-200
- Include in paid commercial courses without proper licensing
```

---

## 📞 **Getting Proper Licenses**

### **For Commercial NLLB-200 Use**
1. **Contact Meta**: opensource@meta.com
2. **Specify use case**: Describe your intended commercial application
3. **Negotiate terms**: Work out licensing fees and conditions
4. **Get written agreement**: Ensure proper legal documentation

### **Alternative Approaches**
1. **Use MT5 instead**: More permissive licensing for commercial use
2. **Hybrid approach**: Commercial framework + user-downloaded models
3. **Service-based**: Sell setup, training, and support services
4. **Consulting**: Offer implementation and customization services

---

## 🔍 **License Verification**

### **How to Check Current Licenses**
```bash
# Check NLLB-200 model license
cat models/deployed_models/nllb_200_1.3b/README.md

# Check Transformers license
python3 -c "import transformers; print(transformers.__file__)"
# Then check LICENSE file in that directory

# Check PyTorch license
python3 -c "import torch; print(torch.__file__)"
# Then check LICENSE file in that directory
```

### **Staying Updated**
- **NLLB-200**: Check Hugging Face model pages for latest terms
- **Libraries**: Monitor GitHub repositories for license changes
- **Meta policies**: Follow Meta AI announcements for policy updates

---

## ⚠️ **Important Disclaimers**

### **No Warranty**
This software is provided "as is" without warranty of any kind. Users assume all risks associated with its use.

### **Legal Compliance**
Users are responsible for ensuring their use complies with:
- Local laws and regulations
- Export control restrictions
- Data protection requirements (GDPR, etc.)
- Professional ethics and confidentiality requirements

### **License Changes**
Licenses may change over time. Always check current terms before:
- Commercial use
- Redistribution
- Integration into other projects
- Large-scale deployment

---

## 📚 **Additional Resources**

### **Official Documentation**
- **Meta NLLB-200**: https://ai.meta.com/research/no-language-left-behind/
- **Hugging Face Models**: https://huggingface.co/facebook/nllb-200-1.3B
- **Transformers License**: https://github.com/huggingface/transformers/blob/main/LICENSE
- **PyTorch License**: https://github.com/pytorch/pytorch/blob/main/LICENSE

### **Legal Resources**
- **Creative Commons**: https://creativecommons.org/licenses/by-nc/4.0/
- **Apache License**: https://www.apache.org/licenses/LICENSE-2.0
- **BSD License**: https://opensource.org/licenses/BSD-3-Clause
- **MIT License**: https://opensource.org/licenses/MIT

---

## 📝 **Summary for Quick Reference**

| Component | License | Commercial Use | Attribution Required |
|-----------|---------|----------------|---------------------|
| **NLLB-200 Models** | Custom (CC BY-NC based) | ❌ Requires Meta license | ✅ Yes |
| **Integration Scripts** | MIT | ✅ Yes | ✅ Recommended |
| **Transformers** | Apache 2.0 | ✅ Yes | ✅ Yes |
| **PyTorch** | BSD 3-Clause | ✅ Yes | ✅ Yes |
| **SentencePiece** | Apache 2.0 | ✅ Yes | ✅ Yes |

**Bottom Line**: The system is free for personal, academic, and non-commercial professional use. For commercial services using NLLB-200, contact Meta for licensing.

---

*This document is provided for informational purposes. For legal advice regarding specific use cases, consult with a qualified attorney familiar with software licensing and intellectual property law.*
