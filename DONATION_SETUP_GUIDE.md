# Setting Up Donations for TraductAL

**Simple options for accepting donations as an independent researcher**

---

## Recommended Options (Easiest to Implement)

### 1. GitHub Sponsors ⭐ (Recommended)

**Pros:**
- Built into GitHub (where your code lives)
- "Sponsor" button appears on your repository
- No fees for non-profits/individuals
- Multiple payment methods (credit card, PayPal)
- Tax-friendly (GitHub handles reporting)

**Setup:**
1. Go to https://github.com/sponsors
2. Join waitlist or apply (if not already enrolled)
3. Set up payout method (bank account or Stripe)
4. Create sponsor tiers (or just "custom amount")
5. GitHub adds "Sponsor" button to your repo automatically

**Suggested tiers:**
- $5/month - Coffee supporter
- $25/month - Regular supporter
- $100/month - Institutional supporter
- Custom amount

**Time to set up:** 30 minutes + approval wait

---

### 2. Ko-fi (Simplest)

**Pros:**
- Very simple, no approval needed
- "Buy me a coffee" style (one-time donations)
- No monthly fees (they take 0% on donations)
- Only takes payment processing fees (~2-3%)
- Can add "Ko-fi" button to README with badge

**Setup:**
1. Go to https://ko-fi.com
2. Sign up (free)
3. Set up PayPal or Stripe for payouts
4. Get your Ko-fi link (e.g., ko-fi.com/rogaton)
5. Add button to README

**In your README:**
```markdown
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/rogaton)
```

**Time to set up:** 15 minutes

---

### 3. PayPal Donation Button

**Pros:**
- Familiar to donors
- Works worldwide
- Can add button directly to README
- One-time or recurring

**Setup:**
1. Have PayPal account (personal or business)
2. Go to PayPal → Tools → PayPal Buttons
3. Create "Donate" button
4. Get HTML/link code
5. Add to README or separate donations page

**In your README:**
```markdown
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?hosted_button_id=YOUR_ID)
```

**Time to set up:** 10 minutes (if you have PayPal)

---

### 4. GitHub README Donation Badges

**Simple badge approach:**

```markdown
## Support This Project

<a href="https://ko-fi.com/rogaton">
  <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support via Ko-fi">
</a>

Or via PayPal: [paypal.me/yourlink](https://paypal.me/yourlink)
```

---

## Options for European Researchers

### 5. Buy Me a Coffee

Similar to Ko-fi:
- https://www.buymeacoffee.com
- Works in Europe
- Simple one-time donations

### 6. Liberapay

**Pros:**
- European (France-based)
- Non-profit
- Open-source friendly
- Recurring donations
- Very transparent

**Cons:**
- Less known than others
- Setup slightly more complex

**Website:** https://liberapay.com

---

## Bank Transfer (Traditional)

**For Swiss researchers:**

Simply list:
```markdown
### Bank Transfer (Switzerland)

For direct bank transfer, contact: relanir@bluewin.ch

I'll provide:
- IBAN
- Bank details
- Reference information
```

**Pros:**
- No fees (for you)
- Traditional, familiar to Swiss/European donors

**Cons:**
- Manual process
- Not as convenient for international donors

---

## What NOT to Use

❌ **Patreon**: Takes 5-12% fees, too creator-focused
❌ **GoFundMe**: For campaigns, not ongoing projects
❌ **Kickstarter**: For specific projects with goals
❌ **Cryptocurrency**: Complex, tax implications

---

## Recommended Approach for You

Based on being an independent Swiss researcher:

**Phase 1 (Now - Simple):**
1. **Ko-fi** - Quick, easy, works immediately
2. **Email for bank transfer** - For those who prefer traditional

**Phase 2 (Next month):**
3. **GitHub Sponsors** - Apply now, use when approved

**Phase 3 (Optional):**
4. **PayPal button** - If many people request it

---

## Tax Implications (Switzerland)

**Donations as income:**
- In Switzerland, donations you receive are generally taxable income
- Keep records of all donations received
- Declare on annual tax return
- Consult a Swiss tax advisor for specifics

**Research exemptions:**
- Some research activities may have different treatment
- Academic institutions often have special status
- Consult with tax professional

**Not tax advice** - this is general information only.

---

## Suggested Text for Your README

### Option A: Minimal

```markdown
## Support Development

TraductAL is developed by an independent researcher.

**Optional donations**: [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/rogaton)

Or contact relanir@bluewin.ch for bank transfer details.
```

### Option B: Slightly More Detail

```markdown
## Supporting TraductAL

TraductAL is developed and maintained by an independent computational linguist in Switzerland.

If you find it useful, optional donations help support:
- Adding new languages
- Improving translation quality
- Maintaining documentation
- Research on hybrid approaches

**Donate via:**
- Ko-fi: [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/rogaton)
- Bank transfer: Contact relanir@bluewin.ch

**Academic collaboration**: Also contact relanir@bluewin.ch
```

---

## Implementation Steps

### This Week:

1. **Choose one method** (I recommend Ko-fi for simplicity)
2. **Set up account** (15-30 minutes)
3. **Add button to README** (5 minutes)
4. **Update COMMERCIAL_LICENSE.md** with actual donation links
5. **Commit and push**

### Next Steps:

6. **Apply for GitHub Sponsors** (when ready)
7. **Monitor donations** (if any come in)
8. **Thank donors** (email or acknowledgment)
9. **Report on tax return** (end of year)

---

## My Recommendation

**For you specifically:**

```markdown
**Start with Ko-fi** (simplest, works immediately)
+ **Email for bank transfer** (for Swiss/European donors)
+ **GitHub Sponsors** (apply now, use later)
= Three simple options, no complexity
```

**Don't overthink it.** Most open-source projects get few donations anyway. The point is to:
1. Give people an option if they want
2. Not beg or be salesy
3. Focus on the research, not fundraising

---

**Want me to help you set up Ko-fi and add the button to your README?**

It takes 15 minutes and then you're done with the "donation infrastructure."
