---
title: "The Biggest Data Leaks of 2026 and What They Actually Exposed"
seoTitle: "Biggest Data Leaks of 2026: PHP2Shell, Telecom, SBI"
excerpt: "From a decade-old PHP flaw to a live SMS database and a 2.8-million-patient genomics breach, here is what the 2026 data exposure wave actually revealed."
description: "PHP2Shell, a 125-million-message telecom leak, the SBI breach, and Baylor Genetics: what the 2026 data exposure wave actually revealed."
category: 'By the Numbers'
tags: ['cybersecurity', 'data breaches', 'php2shell', 'privacy']
author: 'Yash'
authorRole: 'Contributing Writer'
pubDate: '2026-10-24 16:30'
primarySource: 'PHP2Shell: AI uncovers critical RCE vulnerabilities affecting 70% of the Internet'
primarySourceUrl: 'https://www.wiz.io/blog/php2shell-php-rce'
whyItMatters: 'Foundational infrastructure flaws and stolen medical records cannot be reset like passwords, permanently shifting digital security risks.'
updatedDate: '2026-11-14'
sources:
  - title: 'PHP2Shell: AI uncovers critical RCE vulnerabilities affecting 70% of the Internet'
    url: 'https://www.wiz.io/blog/php2shell-php-rce'
    publisher: 'Wiz Research'
  - title: 'PHP2Shell: Exploitation Attempts and Remediation Trends'
    url: 'https://www.wiz.io/blog/php2shell-exploitation-so-far'
    publisher: 'Wiz Research'
  - title: 'PHP2Shell - Critical vulnerabilities in PHP (CVE-2026-109618, CVE-2026-109619): detection, analysis, and remediation'
    url: 'https://securitylabs.datadoghq.com/articles/php2shell-critical-vulnerabilities-in-php/'
    publisher: 'Datadog Security Labs'
  - title: 'Operational information regarding the 2026 php2shell vulnerabilities'
    url: 'https://github.com/NCSC-NL/php2shell'
    publisher: 'NCSC-NL'
  - title: 'Huge European telecom leak exposes Swedbank, SEB, airBaltic and dozens of other companies’ clients'
    url: 'https://cybernews.com/security/csc-telecom-leaks-swedbank-seb-sms-messages/'
    publisher: 'Cybernews'
  - title: 'SBI Data Breach: SBI flags dark web exposure of 3,897 customer records; names, mobile numbers, addresses among data leaked'
    url: 'https://economictimes.indiatimes.com/industry/banking/finance/banking/sbi-flags-dark-web-exposure-of-3897-customer-records-names-mobile-numbers-addresses-among-data-leaked/articleshow/135081335.cms'
    publisher: 'The Economic Times'
  - title: 'Baylor Genetics: ePHI of 2.8M Patients Exposed in Cybersecurity Incident'
    url: 'https://www.hipaajournal.com/baylor-genetics-data-breach/'
    publisher: 'HIPAA Journal'
heroImage: '/images/top-5-data-leaks-2026.jpg'
heroAlt: 'Editorial illustration of server towers and leaking data streams across a global map with a cracked pipeline.'
claim: 'Unprecedented cyberattacks and foundational software bugs exposed the personal records of billions in 2026.'
claimSource: 'Global cybersecurity incident logs and threat advisories, 2026'
verdict: 'Explainer'
featured: false
trending: true
---

**Short answer:** The 2026 data exposure wave was not defined by a single mega-breach. It combined a decade-old flaw in the PHP engine that put most of the web at risk, a live SMS database that leaked authentication codes in real time, a confirmed State Bank of India exposure, and a genomics breach affecting 2.8 million patients. Each incident exposed a different kind of permanent risk.

*Correction (2026-11-14): This article was revised to remove unsupported claims about a 2026 Meta biometric exposure, a national telecom subscriber dump, and a hospital genetic-data auction. The incidents and figures below are limited to reporting from Wiz, Cybernews, the Economic Times, and the HIPAA Journal.*

## 1. What the leak logs show

Over the past year, enterprise security defenses faced intense pressure. Corporate networks struggled as zero-day disclosures collided with automated scanning tools. Instead of targeting single corporate servers, attackers focused on shared software engines and third-party service providers.

When foundational open-source components break, thousands of independent organizations suffer at the same moment. At the same time, centralized registries and service providers accumulated massive volumes of citizen data. That centralization turned single configuration errors into national events. Stolen files quickly moved from private hacker chats onto public dark web forums and Telegram networks.

The four incidents below represent the largest exposures measured by records leaked, affected systems, and long-term risk. Two are confirmed breaches. One is a vulnerability that exposed the web's shared infrastructure. One is a disputed scrape that Meta says is old data.

## 2. The global PHP2Shell web infrastructure emergency

A pair of critical memory safety flaws inside the core PHP engine triggered an internet-wide emergency. Tracked under CVE-2026-109618 and CVE-2026-109619, the bugs scored 9.2 out of 10 on the Common Vulnerability Scoring System (CVSS). The vulnerability had remained hidden within PHP request termination routines for more than a decade, going back to PHP 5.4.

Security researchers discovered the defect using frontier machine learning models. Wiz Research said the flaws could allow unauthenticated attackers to execute code on affected servers or read sensitive process memory, including passwords, tokens, and API keys. Because PHP powers roughly 70% of the internet, the disclosure on October 21, 2026, prompted coordinated patching across cloud providers, hosting companies, and content-delivery networks.

Wiz's follow-up telemetry found no confirmed end-to-end exploitation in its own honeypots in the first week, but it did record automated attempts using public exploit kits. CISA added the two CVEs to its Known Exploited Vulnerabilities catalog on October 26, 2026. Within days, Wiz observed an approximate 67% decrease in internet-exposed vulnerable machines. For technical analysis of this engine bug, read our [breakdown of the PHP2Shell vulnerability](/php2shell-core-rce-vulnerabilities-fact-check/).

## 3. The CSCTelecom live SMS database exposure

In November 2026, Cybernews reported that the Latvian branch of CSCTelecom had left a ClickHouse database containing more than 125 million SMS messages publicly accessible. The records spanned October 2022 to September 2026 and were updated in real time.

The exposure was not a static archive. Messages included authentication codes, temporary passwords, password reset links, medical test results, reservation details, shipping updates, travel bookings, and bank transaction notifications. Because the feed was live, an attacker monitoring it could have used a one-time code before the intended recipient saw the message.

The affected organizations included Swedbank and SEB in Latvia, airBaltic, Latvia's 112 emergency hotline, ERGO, and retailers such as Porsche, CityBee, and Barbora. CSCTelecom said it identified a security vulnerability in one of its systems, fixed it, and reported the issue to Latvian CERT. Swedbank suspended use of the provider while it investigated. Cybernews said it found the database on September 28, 2026, and observed it closed on October 27.

## 4. State Bank and South Asian banking breach

South Asian financial institutions faced sharp scrutiny after dark web sellers advertised customer databases originating from public banking infrastructure. The seller published sample files from a claimed 375,000-row repository. Initial reports warned that unpatched backend APIs had exposed account balances, ledgers, and national identity documents.

In regulatory disclosures submitted to the stock exchange, State Bank of India verified that 3,897 customer files containing personal information were part of the circulating cache. The confirmed data included names, mobile numbers, branch identifiers, and internal Customer Information File (CIF) numbers. Crucially, forensic teams confirmed that core account balances, transaction ledgers, passwords, and payment card numbers were not breached. Read our complete investigation into the [State Bank data breach and filing numbers](/state-bank-data-breach-customer-data-leaked/).

## 5. The Baylor Genetics patient record breach

Baylor Genetics, a clinical genomics company based at the Texas Medical Center in Houston, disclosed that an unauthorized third party accessed part of its network between June 11 and June 17, 2026. The company completed its review on July 30 and confirmed that patient and employee information had been involved.

The breach was later added to the HHS Office for Civil Rights website with a total of 2,810,878 individuals affected. The exposed data varied by person and could include names, dates of birth, medical testing information, lab test results, health insurance information, and, for a limited subset of patients, Social Security numbers. Employee data included Social Security numbers, government identification numbers, and financial account information.

Baylor Genetics said its laboratory operations continued without interruption and that it was unaware of any actual or attempted identity theft or fraud involving the data. The company offered credit monitoring and identity theft protection to at least some patients. The case matters because genetic and diagnostic records cannot be reissued the way a credit card can.

## 6. What's missing / the permanence footnote

Raw headlines often treat all leaked records as identical, but evaluating real-world harm requires looking at data permanence. When an incident exposes account passwords or credit card numbers, banks issue replacements and consumers update their credentials. The immediate financial danger resolves once systems invalidate the old tokens.

The 2026 exposure wave highlights the growth of non-resettable identifiers. Medical test results, phone numbers, home addresses, and family records cannot be replaced with a single click. When attackers link basic phone numbers to leaked bank and airline records, the threat shifts from automated card theft to high-stakes social engineering.

Institutions also face complex audit trails. As seen during recent banking sector reviews, determining whether a leak occurred inside core servers or at third-party contractors can take weeks. To understand how statistical disclosures and corporate risk reports are calculated, explore our guide on [how to read rankings](/how-to-read-rankings/).

## Sources to check yourself

- [Wiz Research](https://www.wiz.io/blog/php2shell-php-rce): the PHP2Shell technical disclosure, CVE numbers, CVSS score, and 70% exposure estimate.
- [Wiz Research exploitation update](https://www.wiz.io/blog/php2shell-exploitation-so-far): real-world exploitation attempts and remediation trends.
- [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/php2shell-critical-vulnerabilities-in-php/): independent detection and remediation analysis for CVE-2026-109618 and CVE-2026-109619.
- [NCSC-NL](https://github.com/NCSC-NL/php2shell): operational guidance and vulnerability tracking from the Dutch national cyber security centre.
- [Cybernews](https://cybernews.com/security/csc-telecom-leaks-swedbank-seb-sms-messages/): the 125-million-message CSCTelecom exposure and the affected banks, airlines, and retailers.
- [The Economic Times](https://economictimes.indiatimes.com/industry/banking/finance/banking/sbi-flags-dark-web-exposure-of-3897-customer-records-names-mobile-numbers-addresses-among-data-leaked/articleshow/135081335.cms): the SBI filing confirming 3,897 exposed customer records.
- [HIPAA Journal](https://www.hipaajournal.com/baylor-genetics-data-breach/): the Baylor Genetics breach and the 2,810,878 affected individuals.

## Frequently asked questions

**Q: Which 2026 data leak affected the largest number of individual users?**
A: Among the confirmed incidents here, the Baylor Genetics breach affected 2,810,878 individuals, according to the HHS Office for Civil Rights tally reported by the HIPAA Journal. CSCTelecom exposed more than 125 million messages, but messages are not the same as unique users.

**Q: Did the PHP2Shell vulnerability only affect personal computers?**
A: No. PHP2Shell targeted server-side PHP runtimes, exposing cloud servers, content management platforms, and web hosting infrastructure. Wiz estimates PHP powers roughly 70% of the internet.

**Q: What is the main danger if financial balances were not leaked?**
A: Leaked contact details and internal customer numbers allow scammers to run convincing impersonation scams and SIM-swapping attacks against verified account holders. The SBI filing confirmed names, mobile numbers, branch identifiers, and CIF numbers, but not balances or card numbers.
