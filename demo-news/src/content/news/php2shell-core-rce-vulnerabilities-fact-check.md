---
title: "PHP2Shell: Why Two Core PHP Flaws Put 70% of the Web at Risk"
seoTitle: "PHP2Shell RCE Flaws: CVE-2026-109618 and 109619"
excerpt: "Two memory-safety bugs in core PHP allow unauthenticated remote code execution and memory disclosure. Patches and a CISA KEV listing followed within days."
description: "PHP2Shell: CVE-2026-109618 and CVE-2026-109619 allow unauthenticated RCE in core PHP. What Wiz found, who is affected, and how to patch."
category: 'Reality Check'
tags: ['cybersecurity', 'php', 'vulnerabilities', 'wiz']
author: 'Yash'
authorRole: 'Contributing Writer'
pubDate: '2026-10-22 13:30'
primarySource: 'CISA alert on PHP vulnerabilities CVE-2026-109618 and CVE-2026-109619'
primarySourceUrl: 'https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching'
whyItMatters: 'PHP powers seven in ten websites worldwide; engine-level memory flaws execute beneath application security controls.'
updatedDate: '2026-11-14'
sources:
  - title: 'Critical Vulnerabilities in PHP Require Immediate Patching'
    url: 'https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching'
    publisher: 'CISA'
  - title: 'PHP2Shell: AI uncovers critical RCE vulnerabilities affecting 70% of the Internet'
    url: 'https://www.wiz.io/blog/php2shell-php-rce'
    publisher: 'Wiz Research'
  - title: 'PHP2Shell: Exploitation Attempts and Remediation Trends'
    url: 'https://www.wiz.io/blog/php2shell-exploitation-so-far'
    publisher: 'Wiz Research'
  - title: 'php2shell (CVE-2026-109618, CVE-2026-109619): Critical PHP RCE FAQ'
    url: 'https://www.tenable.com/blog/php2shell-cve-2026-109618-cve-2026-109619-frequently-asked-questions-about-critical-php-remote'
    publisher: 'Tenable'
  - title: 'Critical security issue affecting PHP'
    url: 'https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php'
    publisher: 'National Cyber Security Centre'
  - title: 'PHP: News Archive - 2026'
    url: 'https://www.php.net/archive/2026.php'
    publisher: 'The PHP Group'
heroImage: '/images/php2shell-core-vulnerability.jpg'
heroAlt: 'Stark editorial illustration of towering server rack silhouettes with a vermilion memory breach highlight'
trending: true
claim: 'PHP2Shell enables unauthenticated remote code execution on 70% of all websites across the global internet.'
claimSource: 'Viral cybersecurity headlines and technical threat alerts, October 2026'
verdict: 'True with context'
---

**Short answer:** Core PHP engine vulnerabilities tracked as CVE-2026-109618 and CVE-2026-109619 allow unauthenticated attackers to execute arbitrary code or read raw process memory. The underlying memory flaws exist in PHP releases dating back to version 5.4, covering roughly 70% of the public web. Wiz demonstrated working exploits against standard WordPress, Drupal and Joomla containers, but exploitation requires strict heap conditions. Cloud providers prepared mitigations before disclosure, and CISA added both flaws to its Known Exploited Vulnerabilities catalog on October 26, 2026.

*Correction (2026-11-14): An earlier version said major cloud providers had already deployed edge rules before public disclosure and listed the patched branches as PHP 8.1, 8.2 and 8.3. Wiz and CISA report that providers prepared mitigations before disclosure, and CISA lists the fixed versions as PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35. The earlier version also omitted the October 26 KEV addition.*

## 1. What the viral report claims

Headlines circulating across developer forums warn that PHP2Shell puts 70% of the internet at immediate risk of automated takeover. The claim stems from research by cloud security firm Wiz, which announced the discovery of unauthenticated remote code execution bugs in the PHP runtime.

Viral posts claim attackers can bypass login screens and firewalls. They warn adversaries can seize web servers, steal passwords, and leak database credentials.

The coverage highlights that the vulnerable code has lived inside PHP for over a decade. Because the flaw resides within PHP core rather than user code, posts warn that even a secure standalone script remains exposed.

## 2. What the technical data and CVEs confirm

On October 21, 2026, the PHP development team released emergency updates addressing two critical advisories with severity scores reaching CVSS 9.2. CISA lists the fixed versions as PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35.

The flaws center on how the PHP Zend engine handles fatal out-of-memory errors during HTTP request termination. When an allocation fails during request startup, internal cleanup paths can leave stale pointers inside worker memory.

Under CVE-2026-109618, an upload-progress unserializer bug leaves request state exposed in the worker heap. A subsequent request handled by the same worker reclaims that memory, granting attackers arbitrary code execution or dumping live worker memory into a PHPSESSID cookie. In the memory disclosure chain, PHP parses RFC 1867 multipart requests before module initialization finishes. When an allocation failure aborts cleanup, the session pointer PS(id) points to freed heap data. A subsequent request re-encodes that pointer into a cookie, exposing process memory even if the application never invokes session_start.

Under CVE-2026-109619, fatal-error backtrace references and OPcache shared memory mappings survive request destruction. During script persistence, allocation failures leave worker pointer maps unsynchronized with shared memory frontiers. Later worker tasks resolve shared slots into conflicting types, triggering memory corruption. Wiz researchers chained these primitives to gain unauthenticated remote shell access against default Docker containers of WordPress, Drupal, and Joomla.

Frontier artificial intelligence played an active role in discovering and proving the attack chains. Wiz reported using Wiz Atlas, Gemini 4 Argon, and GPT-5.6 Sol to navigate complex heap alignments. Raluca Ada Popa, Head of Gemini Security at Google DeepMind, noted that frontier models bridged key defense gaps by locating flaws and validating vendor patches.

Wiz discovered the initial flaw on August 19, 2026. Researchers confirmed Drupal execution on August 20, alerted the PHP team on August 24, and coordinated public disclosure on October 21 alongside Calif and OpenAI.

## 3. What is missing: Memory constraints and cloud mitigations

While the technical risk is acute, real-world exploitation is not an automatic one-click event across every server.

First, successful remote exploitation requires precise manipulation of request timing and memory limits. Attackers must trigger an out-of-memory error during specific initialization windows and ensure subsequent requests land on the exact same worker process.

Second, major cloud providers including Cloudflare, AWS, Google Cloud, Fastly and Akamai prepared edge rules and runtime filtering alongside Wiz before disclosure. These controls can block anomalous multipart requests that attempt to force early allocation crashes. CISA describes a web application firewall as a stopgap that may provide some protection until systems are updated. Similar coordinated protections were deployed during recent [TLS certificate revocations](/emudhra-tls-intermediate-certificates-compromised-fact-check/), illustrating how edge infrastructure buffers backend runtimes while teams patch.

The UK National Cyber Security Centre (NCSC) issued an alert advising organizations to patch internet-facing hosts immediately. CISA went further: organizations that cannot update immediately, or that still run PHP 8.1 or earlier, should take PHP-based systems offline until they can be patched. Administrators should also monitor for PHP worker processes launching shells or downloading tools. Similar structural isolation benefits have been documented in [memory-safe software engines](/artcraft-rust-creative-engine-adobe-alternative/), highlighting the systemic shift away from manual memory management in core web runtimes.

## Sources to check yourself

- [CISA](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching): the fixed PHP versions, affected server setups and the October 26 KEV addition.
- [Wiz Research](https://www.wiz.io/blog/php2shell-php-rce): the technical disclosure, the four bug classes, the CVSS 9.2 rating and the disclosure timeline.
- [Wiz Research exploitation update](https://www.wiz.io/blog/php2shell-exploitation-so-far): observed exploitation attempts and remediation trends after disclosure.
- [Tenable](https://www.tenable.com/blog/php2shell-cve-2026-109618-cve-2026-109619-frequently-asked-questions-about-critical-php-remote): an independent FAQ on exposure and patching.
- [NCSC](https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php) and [php.net](https://www.php.net/archive/2026.php): official advisories and the PHP release archive.

## Frequently asked questions

**Q: Does my website need application-level code fixes?**
A: No. The vulnerabilities exist inside the C runtime of PHP itself, meaning changes to WordPress plugins or custom PHP scripts cannot resolve the underlying memory flaw.

**Q: Can attackers steal data without full server takeover?**
A: Yes. CVE-2026-109618 allows attackers to dump raw worker memory into session cookies, potentially exposing database credentials, API tokens, and session keys from prior web requests.

**Q: What should system administrators prioritize first?**
A: Teams must update PHP runtimes on public-facing servers. When patching stalls, administrators should apply official memory mitigations and review logs for repeated 500 errors.
