---
title: "why PHP shell RCE vulnerabilities are critical: PHP2Shell Core RCE Flaws Affect 70% of the Web"
seoTitle: "PHP2Shell RCE Flaws in Core PHP Engine: Fact Check"
excerpt: "Flaws in core PHP request handling permit unauthenticated remote code execution, prompting coordinated emergency updates across cloud CDNs."
description: "Wiz Research uncovered critical memory safety bugs in core PHP, triggering emergency global security patches across web hosting infrastructure."
category: 'Reality Check'
tags: ['cybersecurity', 'php', 'vulnerabilities', 'wiz']
author: 'Yash'
authorRole: 'Contributing Writer'
pubDate: '2026-10-22 13:30'
primarySource: 'UK NCSC Security Advisory and Wiz Research Threat Briefing on PHP Core'
primarySourceUrl: 'https://www.ncsc.gov.uk/'
whyItMatters: 'PHP powers seven in ten websites worldwide; engine-level memory flaws execute beneath application security controls.'
sources:
  - title: 'UK National Cyber Security Centre: Critical security issue affecting PHP'
    url: 'https://www.ncsc.gov.uk/'
    publisher: 'NCSC'
  - title: 'Wiz Blog: PHP2Shell AI Uncovers Critical RCE Vulnerabilities'
    url: 'https://www.wiz.io/'
    publisher: 'Wiz Research'
  - title: 'The PHP Group: Official Core Security Releases'
    url: 'https://www.php.net/'
    publisher: 'The PHP Group'
heroImage: '/images/php2shell-core-vulnerability.jpg'
heroAlt: 'Stark editorial illustration of towering server rack silhouettes with a vermilion memory breach highlight'
trending: true
claim: 'PHP2Shell enables unauthenticated remote code execution on 70% of all websites across the global internet.'
claimSource: 'Viral cybersecurity headlines and technical threat alerts, October 2026'
verdict: 'True with context'
---

**Short answer:** Core PHP engine vulnerabilities tracked as CVE-2026-109618 and CVE-2026-109619 allow unauthenticated attackers to execute arbitrary code or read raw process memory. The underlying memory flaws exist in PHP releases dating back to version 5.4, covering roughly 70% of the public web. While proof-of-concept exploits succeeded against standard WordPress, Drupal, and Joomla containers, exploitation requires strict heap conditions, and coordinated cloud provider defenses deployed prior to disclosure.

## 1. What the viral report claims

Headlines circulating across developer forums warn that PHP2Shell puts 70% of the internet at immediate risk of automated takeover. The claim stems from research by cloud security firm Wiz, which announced the discovery of unauthenticated remote code execution bugs in the PHP runtime.

Viral posts claim attackers can bypass login screens and firewalls. They warn adversaries can seize web servers, steal passwords, and leak database credentials.

The coverage highlights that the vulnerable code has lived inside PHP for over a decade. Because the flaw resides within PHP core rather than user code, posts warn that even a secure standalone script remains exposed.

## 2. What the technical data and CVEs confirm

On October 21, 2026, the PHP development team released emergency updates addressing two critical advisories with severity scores reaching CVSS 9.2.

The flaws center on how the PHP Zend engine handles fatal out-of-memory errors during HTTP request termination. When an allocation fails during request startup, internal cleanup paths can leave stale pointers inside worker memory.

Under CVE-2026-109618, an upload-progress unserializer bug leaves request state exposed in the worker heap. A subsequent request handled by the same worker reclaims that memory, granting attackers arbitrary code execution or dumping live worker memory into a PHPSESSID cookie. In the memory disclosure chain, PHP parses RFC 1867 multipart requests before module initialization finishes. When an allocation failure aborts cleanup, the session pointer PS(id) points to freed heap data. A subsequent request re-encodes that pointer into a cookie, exposing process memory even if the application never invokes session_start.

Under CVE-2026-109619, fatal-error backtrace references and OPcache shared memory mappings survive request destruction. During script persistence, allocation failures leave worker pointer maps unsynchronized with shared memory frontiers. Later worker tasks resolve shared slots into conflicting types, triggering memory corruption. Wiz researchers chained these primitives to gain unauthenticated remote shell access against default Docker containers of WordPress, Drupal, and Joomla.

Frontier artificial intelligence played an active role in discovering and proving the attack chains. Wiz reported using Wiz Atlas, Gemini 4 Argon, and GPT-5.6 Sol to navigate complex heap alignments. Raluca Ada Popa, Head of Gemini Security at Google DeepMind, noted that frontier models bridged key defense gaps by locating flaws and validating vendor patches.

Wiz discovered the initial flaw on August 19, 2026. Researchers confirmed Drupal execution on August 20, alerted the PHP team on August 24, and coordinated public disclosure on October 21 alongside Calif and OpenAI.

## 3. What is missing: Memory constraints and cloud mitigations

While the technical risk is acute, real-world exploitation is not an automatic one-click event across every server.

First, successful remote exploitation requires precise manipulation of request timing and memory limits. Attackers must trigger an out-of-memory error during specific initialization windows and ensure subsequent requests land on the exact same worker process.

Second, major cloud providers including Cloudflare, AWS, Google Cloud, Fastly, and Akamai deployed edge rules and runtime filtering prior to public disclosure. These shields block anomalous multipart requests that attempt to force early allocation crashes. Similar coordinated protections were deployed during recent [TLS certificate revocations](/emudhra-tls-intermediate-certificates-compromised-fact-check/), illustrating how edge infrastructure buffers backend runtimes while teams patch.

The UK National Cyber Security Centre (NCSC) issued an alert advising organizations to audit internet-facing hosts immediately. The agency urged administrators to apply engine updates immediately. Where upgrades stall, teams should apply PHP Foundation mitigations and monitor server logs for worker crashes. Similar structural isolation benefits have been documented in [memory-safe software engines](/artcraft-rust-creative-engine-adobe-alternative/), highlighting the systemic shift away from manual memory management in core web runtimes.

## Sources to check yourself

- UK National Cyber Security Centre: Advisory on CVE-2026-109618 and CVE-2026-109619 memory corruption flaws (October 2026).
- Wiz Research: Technical threat briefing on PHP2Shell engine exploits and AI-assisted discovery workflows.
- The PHP Group: Official security releases for PHP 8.1, 8.2, and 8.3 maintenance branches.

## Frequently asked questions

**Q: Does my website need application-level code fixes?**
A: No. The vulnerabilities exist inside the C runtime of PHP itself, meaning changes to WordPress plugins or custom PHP scripts cannot resolve the underlying memory flaw.

**Q: Can attackers steal data without full server takeover?**
A: Yes. CVE-2026-109618 allows attackers to dump raw worker memory into session cookies, potentially exposing database credentials, API tokens, and session keys from prior web requests.

**Q: What should system administrators prioritize first?**
A: Teams must update PHP runtimes on public-facing servers. When patching stalls, administrators should apply official memory mitigations and review logs for repeated 500 errors.
