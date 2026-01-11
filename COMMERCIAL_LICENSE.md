# TraductAL Commercial License

**Version 1.0 - January 2026**

---

> 📋 **STATUS**: Commercial licensing framework in development
>
> This document outlines our planned commercial licensing structure. We are currently:
> - Finalizing payment infrastructure
> - Completing legal review
> - Setting up support systems
>
> **Available NOW**: Academic/research use (free MIT License)
> **Interested in commercial licensing?** Contact: relanir@bluewin.ch for early access and custom terms
>
> Expected full commercial launch: Q1 2026

---

## Overview

TraductAL is available under **dual licensing**:

1. **MIT License** (LICENSE file) - For non-commercial, academic, and research use
2. **Commercial License** (this file) - For commercial, enterprise, and proprietary use

This document defines the terms for commercial use of TraductAL.

---

## When Do You Need a Commercial License?

You need a commercial license if you:

### ✅ Required for Commercial License:

- **Embed TraductAL in a commercial product or service** that you sell, license, or distribute
- **Provide translation services** using TraductAL as part of a paid offering
- **Deploy TraductAL** in a for-profit organization's internal operations (above free tier limits)
- **Modify and distribute** TraductAL code in a proprietary/closed-source product
- **Offer hosted/SaaS services** based on TraductAL
- **Use TraductAL** in consulting or client projects for which you charge fees

### ❌ NOT Required (MIT License Applies):

- **Academic research** and teaching at educational institutions
- **Non-profit organizations** using TraductAL for their mission
- **Personal use** and experimentation
- **Open-source projects** that remain open source (MIT-compatible)
- **Evaluation and testing** (up to 90 days) before making a licensing decision
- **Small businesses** with annual revenue under $100k USD (see Free Tier below)

---

## Commercial License Tiers

### Tier 1: Startup License
**FREE** for qualifying organizations

**Eligibility:**
- Annual revenue < $100,000 USD (or equivalent)
- Fewer than 10 employees
- Not a subsidiary of a larger company

**Includes:**
- Full access to TraductAL source code
- Deploy on unlimited internal servers
- No support or warranty
- Must display attribution: "Powered by TraductAL"

**How to Activate:**
Contact: relanir@bluewin.ch with company details for written confirmation

---

### Tier 2: Professional License
**$2,500 USD per year** (per legal entity)

**For:**
- Small-to-medium businesses
- Consulting firms
- Translation agencies
- SaaS providers (up to 10,000 API calls/month)

**Includes:**
- Full source code access
- Deploy on unlimited servers within your organization
- Embed in one commercial product
- Email support (best-effort, 5 business days response)
- Remove attribution requirement
- Sublicense rights for your product's end users

**Restrictions:**
- No redistribution of TraductAL as a standalone product
- No white-label reselling of TraductAL itself

---

### Tier 3: Enterprise License
**$15,000 USD per year** (per legal entity)

**For:**
- Large enterprises
- Government contractors
- High-volume SaaS providers
- Multi-product deployments

**Includes:**
- Everything in Professional License
- Unlimited API calls/usage
- Embed in unlimited products
- Priority email support (2 business day response)
- Quarterly consultation calls (4 hours/year)
- Private security vulnerability notifications
- Access to commercial-only features (if developed)

**Optional Add-ons:**
- On-site training: $5,000/day
- Custom model fine-tuning: Starting at $10,000
- Dedicated support contract: $25,000/year

---

### Tier 4: OEM/Redistribution License
**Custom pricing** (starting at $50,000 USD/year)

**For:**
- Software vendors who want to embed TraductAL in their products
- Distributors who want to resell TraductAL
- White-label deployments
- Hardware appliance manufacturers

**Includes:**
- Everything in Enterprise License
- Full redistribution rights
- White-label rights (remove all TraductAL branding)
- Source code modifications with proprietary extensions
- Dedicated technical account manager
- Custom SLA agreements

**Contact:** relanir@bluewin.ch for custom terms

---

## Academic and Non-Profit Exceptions

The following organizations may use TraductAL under the MIT License regardless of their size:

1. **Universities and Research Institutions**
   - For research and teaching purposes
   - Publications must cite TraductAL appropriately

2. **Registered Non-Profit Organizations (501(c)(3) or equivalent)**
   - For mission-related activities
   - Not for commercial consulting or revenue-generating services

3. **Government Research Agencies**
   - For research purposes only
   - Operational/production deployments require commercial license

4. **Open Source Projects**
   - Projects that remain fully open source (MIT, Apache 2.0, GPL, etc.)
   - Cannot be sublicensed into proprietary products

---

## License Grants and Restrictions

### What the Commercial License Grants You:

✅ Right to use TraductAL in commercial products
✅ Right to modify source code for internal use
✅ Right to deploy on any number of servers/instances
✅ Right to embed in products you distribute to customers
✅ Indemnification against license compliance claims
✅ Priority access to updates and security patches

### What Is NOT Granted:

❌ Patent grants (TraductAL does not claim any patents)
❌ Right to use "TraductAL" trademark without permission
❌ Right to resell or redistribute TraductAL as a competing product
❌ Right to remove copyright notices from source files
❌ Transfer of ownership (license is non-transferable without written consent)

---

## Third-Party Components

TraductAL incorporates third-party models and libraries with their own licenses:

### Translation Models:
- **NLLB-200** (Meta AI): CC-BY-NC 4.0 - **Non-commercial only**
- **Apertus-8B**: Apache 2.0 - Commercial use permitted

### Important Restrictions:

⚠️ **NLLB-200 Limitation**: The default NLLB-200 model is licensed CC-BY-NC 4.0, which **prohibits commercial use**.

**For commercial deployments**, you must:
1. **Option A**: Replace NLLB-200 with a commercially-licensed alternative
   - Fine-tune your own model (we can assist - see services)
   - Use Apertus-8B exclusively (supports 1811 languages)
   - Use other commercial MT models (M2M-100 with commercial license, etc.)

2. **Option B**: Obtain separate commercial license from Meta AI for NLLB-200
   - Contact Meta AI directly
   - Provide proof of NLLB-200 commercial license to us

**Your TraductAL commercial license covers the TraductAL codebase only**, not third-party models. You are responsible for ensuring compliance with all third-party licenses.

See `THIRD_PARTY_LICENSES.md` for complete attribution.

---

## Payment Terms

- **Annual subscription**: Invoiced annually, due within 30 days
- **Payment methods**: Bank transfer, credit card (Stripe), PayPal (for smaller licenses)
- **Currency**: USD (can quote in EUR/CHF on request)
- **Renewal**: Auto-renewal with 60 days written notice to cancel
- **Refunds**: Pro-rated refunds within first 90 days if license not suitable

---

## Support Terms

### Response Times:
- **Professional**: Best-effort, 5 business days
- **Enterprise**: 2 business days for critical issues
- **OEM**: 24 hours for critical, 1 business day for normal

### Support Channels:
- Email: [Support Email]
- Priority issue tracker (commercial customers only)
- Scheduled video calls (Enterprise and above)

### Support Scope:
- ✅ Installation and configuration assistance
- ✅ Bug reports and fixes
- ✅ Usage guidance and best practices
- ✅ Integration consulting
- ❌ Custom development (see Professional Services)
- ❌ Training your staff (see add-on services)
- ❌ Third-party model issues (contact model providers)

---

## Warranty and Liability

### Limited Warranty:
For commercial license holders, we warrant that:
- TraductAL will substantially conform to documented functionality
- We have the right to license the TraductAL code (excluding third-party components)
- We will fix reproducible bugs within reasonable timeframes

### Warranty Exclusions:
- Third-party models and dependencies
- Modifications you make to the code
- Hardware/infrastructure issues
- Translation quality or accuracy (ML models are probabilistic)

### Liability Cap:
Our total liability is limited to the fees you paid in the 12 months prior to the claim, except for:
- Gross negligence
- Willful misconduct
- Breach of confidentiality

**Commercial translation is not perfect. Human review is recommended for critical content.**

---

## Compliance and Audit Rights

We reserve the right to:
1. Request verification of your license tier eligibility (revenue, employee count)
2. Audit your usage upon reasonable notice (Enterprise and below)
3. Terminate license for material breaches (with 30 days cure period)

You agree to:
1. Maintain accurate records of TraductAL deployment
2. Notify us of significant changes in usage (e.g., 10x traffic increase)
3. Upgrade license tier if you exceed your tier's limits

---

## How to Purchase

### Step 1: Choose Your Tier
Review the tiers above and select the appropriate license.

### Step 2: Contact Us
**Email**: relanir@bluewin.ch
**Subject Line**: "Commercial License Inquiry - [Tier Name]"

**Include**:
- Company name and website
- Intended use case
- Estimated usage volume
- Number of products/deployments
- Any questions

### Step 3: Receive Quote
We'll send you:
- Custom quote (if needed)
- License agreement draft
- Payment instructions

### Step 4: Execute Agreement
- Sign license agreement
- Submit payment
- Receive license certificate and credentials

### Step 5: Deploy
- Access commercial documentation
- Register for support portal
- Begin deployment with peace of mind

---

## Frequently Asked Questions

**Q: Can I evaluate TraductAL before purchasing?**
A: Yes, 90-day free evaluation under MIT License for commercial assessment.

**Q: What happens if my startup grows beyond $100k revenue?**
A: Congratulations! Upgrade to Professional within 60 days of crossing threshold.

**Q: Do you offer monthly payment plans?**
A: Currently annual only, but we can discuss quarterly payments for Enterprise+.

**Q: Can I buy a perpetual license instead of subscription?**
A: Contact us for perpetual licensing (typically 3-5x annual fee, limited updates).

**Q: What if I only need TraductAL for a 6-month project?**
A: We can offer pro-rated 6-month licenses at 60% of annual price.

**Q: Do non-profits get a discount?**
A: Non-profits qualify for MIT License (free) unless providing commercial services.

**Q: Can I get source code with the commercial license?**
A: Yes, all tiers include full source code access (except OEM custom terms).

**Q: What about academic publications using TraductAL commercially?**
A: Academic research is MIT-licensed. Commercial products arising from research need commercial license.

**Q: How do I handle NLLB-200's non-commercial restriction?**
A: See "Third-Party Components" section above. We can help you fine-tune commercial alternatives.

---

## Contact Information

**Licensing Inquiries**: relanir@bluewin.ch
**Technical Questions**: relanir@bluewin.ch
**Partnership Opportunities**: relanir@bluewin.ch

**Response Time**: Within 3 business days for all inquiries

---

## Legal Notices

This Commercial License is offered by:
**Rogaton (Independent Researcher)**
**Switzerland**

For legal entity information (required for contracts), contact: relanir@bluewin.ch

Governed by the laws of **Switzerland**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 2026 | Initial commercial license structure |

---

**This document supplements but does not replace the MIT License (LICENSE file) for non-commercial use.**

For the full MIT License terms, see: `LICENSE`
For authorship and attribution details, see: `AUTHORSHIP_AND_ATTRIBUTION.md`
