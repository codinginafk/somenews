---
title: "State Bank Data Breach: Did Hackers Leak 375,000 Customer Records?"
seoTitle: "State Bank Data Breach: Did Hackers Leak 375,000 Records?"
excerpt: "State Bank of India confirmed a preliminary breach involving 3,897 customer records from a 375,000-row dark web dump, while core banking credentials remain uncompromised."
description: "State Bank of India confirmed data loss across 3,897 records after dark web claims of 375,000 customer files, but core credentials were not leaked."
category: 'Reality Check'
tags: ['sbi', 'banking', 'cybersecurity', 'india']
author: 'Diyan'
authorRole: 'Staff Writer'
pubDate: '2026-10-24 16:20'
primarySource: 'State Bank of India Stock Exchange Filing on BSE'
primarySourceUrl: 'https://www.bseindia.com/'
whyItMatters: 'Impersonation scams surge when names, phone numbers, and branch IDs leak, even if account passwords and balances stay secure.'
sources:
  - title: 'State Bank of India Stock Exchange Filing on Incident'
    url: 'https://www.bseindia.com/'
    publisher: 'BSE India'
  - title: 'Customer Security and Phishing Incident Advisory'
    url: 'https://www.sbi.co.in/'
    publisher: 'State Bank of India'
  - title: 'Investigation of BreachForums Dark Web Financial Listings'
    url: 'https://www.freepressjournal.in/'
    publisher: 'The Free Press Journal'
  - title: 'National Cyber Security Guidelines and Incident Response'
    url: 'https://www.cert-in.org.in/'
    publisher: 'CERT-In'
heroImage: '/images/state-bank-breach.jpg'
heroAlt: 'Editorial illustration of a cracked bank vault silhouette with leaked digital documents and a red warning lock.'
claim: 'Hackers breached State Bank of India and leaked 375,000 customer banking records and loan files on the dark web.'
claimSource: 'BreachForums listing by threat actor Siriusim and security alerts on X, October 2026'
verdict: 'Misleading — Missing Context'
featured: false
trending: false
---

**Short answer:** State Bank of India confirmed an incident involving the loss of customer data, but the viral headlines claiming a full core banking breach leave out key facts. The state-run lender identified 3,897 verified customer records inside a 375,000-row dark web dump. The exposed files carry contact details and loan lead metadata rather than account balances, card numbers, passwords, PAN cards, or Aadhaar records.

## 1. What the viral post shows

On October 16, 2026, cybersecurity threat monitoring handle CyberPulse56 posted an alert on social platform X. The alert reported that a threat actor operating under the pseudonym Siriusim had posted an alleged State Bank of India database on BreachForums. BreachForums is an illicit clearinghouse known for trading corporate databases. 

The threat actor claimed the cache held 375,000 rows in CSV format alongside 2,722 standalone PDF documents. According to the listing, the dump included customer loan applications, account-opening forms, home addresses, and KYC identity paperwork. 

Journalists at The Free Press Journal inspected four sample files posted by the seller. Their reporters confirmed that the telephone numbers in those samples were live and operational. One sample phone number matched the WhatsApp profile picture of a borrower against a passport photo on an attached document. That sample verified that real citizen information existed in the folder. It sparked viral warnings that India's largest public lender had suffered an unmitigated system infiltration.

## 2. What the data actually says

On October 21, 2026, State Bank of India submitted an official regulatory disclosure to the Bombay Stock Exchange (BSE). The filing acknowledged that the bank had "experienced an incident involving the loss of certain data." 

The timeline started on October 16, 2026, when early warnings reached the bank through CERT-In (the Indian Computer Emergency Response Team) and the Defense Cyber Agency. Both agencies track foreign cyber operations against critical national infrastructure. In response, bank management activated emergency incident protocols. They appointed an independent security auditing firm from CERT-In's empanelled list to examine the dump.

The bank's preliminary examination revealed a distinct picture from the social media claims:

- **Confirmed record count:** SBI identified 3,897 customer records containing personal information within the wider 375,000-entry repository. That represents roughly 1% of the total dataset claimed by the threat actor.
- **Data categories exposed:** The filing lists names, dates of birth, gender, registered mobile numbers, email addresses, residential street addresses, lead IDs, branch codes, customer information file (CIF) numbers, and loan application metadata.
- **Financial assets untouched:** The dump contains zero bank account balances, login credentials, transaction histories, debit card pins, or one-time passcodes (OTPs). Crucially, statutory identifiers including Aadhaar numbers and Permanent Account Numbers (PAN) do not appear in the bank's incident filing.
- **Operational continuity:** The bank stated that the breach caused zero material disruption to retail banking systems, settlement networks, or commercial solvency.

The data confirms that sensitive personal markers were compromised. However, the data does not substantiate claims of an open drain on customer deposits or core database access.

## 3. What's missing / the footnote

The regulatory disclosure leaves several major questions unanswered. First, the bank has not confirmed whether the 3,897 verified records represent 3,897 separate individuals. It has also not confirmed what the remaining 371,000 rows in the dark web upload consist of.

Second, the origin point of the data remains completely unverified. In retail banking, loan acquisition leads often pass through third-party marketing agencies, direct selling agents (DSAs), and regional credit bureaus. The samples verified by reporters consisted primarily of preliminary loan leads. This structure mirrors an earlier breach disclosure by Bank of Baroda on July 27, 2026. In that event, Bank of Baroda cited a potential business email compromise at an external vendor rather than a breach of core servers. State Bank of India's filing names no root cause and does not specify whether third-party partners were involved.

Third, customer notification remains ambiguous. The bank's disclosure notes no direct customer alerts. SBI's public cybersecurity page advises customers to report suspicious calls to `report.phishing@sbi.co.in` or the national cyber helpline at 1930. 

Because financial credentials remain unexposed, the immediate danger is not automated account draining. The real hazard is sophisticated social engineering. Fraudsters armed with a target's genuine name, branch name, date of birth, and CIF number can construct convincing spear-phishing calls. When a scammer quotes your exact branch and application ID over the phone, convincing you to share an OTP becomes far easier.

For more background on public sector banking challenges, read our investigation into [mandatory weekend branch duty](/bank-strike-human-cost-sunday-duty/) and our analysis of the [disputed bank work week](/bank-strike-deferred-7-day-work-week/). To understand how corporate filings disclose statistical risk, see our reader guide on [how to read rankings](/how-to-read-rankings/).

## Sources to check yourself

- State Bank of India Corporate Filing (October 21, 2026), available through BSE India announcement records under scrip code 500112.
- CERT-In National Cyber Security Vulnerability Notes and Incident Response Guidelines at cert-in.org.in.
- The Free Press Journal investigative reporting on BreachForums dark web file samples.
- National Cybercrime Reporting Portal guidelines on identity theft and helpline 1930 documentation.

## Frequently asked questions

**Q: Were money or customer bank balances stolen during this incident?**
A: No. State Bank of India's regulatory filing confirms that passwords, passcodes, account balances, and payment cards were not compromised in the files reviewed by forensic auditors.

**Q: Why is CIF and branch data dangerous if balances are safe?**
A: Customer Information File (CIF) numbers and branch codes serve as internal account markers. Scammers combine these identifiers with mobile numbers and home addresses to impersonate bank representatives during targeted phishing phone calls.

**Q: How did the dark web seller obtain 375,000 rows?**
A: SBI has not determined the source of the broader dump. Investigations are checking whether the data originated from an internal repository, an affiliated subsidiary, or an external third-party loan marketing partner.
