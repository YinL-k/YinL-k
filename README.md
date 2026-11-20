<div align="center">
  <img src="https://raw.githubusercontent.com/YinL-k/YinL-k/main/assets/profile-banner-animated.svg?v=9" alt="Xianzhuo (Ari) Yin — Co-Founder and CTO at YuanMil; Computer Science at Drew University; Applied AI and platform engineering" width="100%" />
  <p>
    <a href="https://www.linkedin.com/in/xianzhuo-yin-602562331/">LinkedIn</a> ·
    <a href="https://apps.apple.com/cn/app/%E5%85%83%E7%A6%A7os/id6795852285">YuanMil OS</a> ·
    <a href="https://chromewebstore.google.com/detail/hnajkeiigdkgafcobbkchpcdafddfpki">SakuraMeter</a> ·
    <a href="https://github.com/YinL-k?tab=repositories">Repositories</a>
  </p>
</div>

I build and lead software across multi-surface products, payment infrastructure, and applied AI. I combine technical direction with hands-on engineering—from backend architecture and integrations to product interfaces and retrieval systems.

**Co-Founder & CTO @ YuanMil** · **Computer Science @ Drew University** · **Mathematics Minor**

## Featured Products

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://apps.apple.com/cn/app/%E5%85%83%E7%A6%A7os/id6795852285">
        <img src="assets/products/yuanmil-os.jpg" alt="YuanMil OS product screens" width="100%" />
      </a>
      <h3>YuanMil OS · 元禧</h3>
      <p><strong>Co-Founder & CTO · Hospitality technology</strong></p>
      <p>A multi-surface hospitality platform spanning an iOS app, WeChat Mini Program, merchant workflows, operations tools, and shared backend services.</p>
      <p><strong>My work:</strong> Technical direction, platform architecture, payment workflows, AI/MCP integrations, and engineering delivery.</p>
      <p><a href="https://apps.apple.com/cn/app/%E5%85%83%E7%A6%A7os/id6795852285">App Store</a> · <a href="https://yuanmilos.com/">Website</a> · <a href="docs/yuanmil-engineering-overview.md">Engineering case study</a></p>
      <p><sub>Java · Spring Boot · Vue 3 · uni-app · React · Redis/Lua · MCP</sub></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://chromewebstore.google.com/detail/hnajkeiigdkgafcobbkchpcdafddfpki">
        <img src="assets/products/sakurameter.jpg" alt="SakuraMeter Chrome extension preview" width="100%" />
      </a>
      <h3>SakuraMeter</h3>
      <p><strong>Creator & Developer · Chrome extension</strong></p>
      <p>A browser extension for ChatGPT activity insights and Codex usage visibility, with Side Chat and an experimental browser-agent workflow.</p>
      <p>Third-party global reset forecasts are clearly labeled as experimental signals, not official OpenAI predictions.</p>
      <p><a href="https://chromewebstore.google.com/detail/hnajkeiigdkgafcobbkchpcdafddfpki">Chrome Web Store</a> · <a href="https://github.com/YinL-k/chatgpt-codex-usage-reset-tracker">Source code</a> · <a href="https://github.com/YinL-k/chatgpt-codex-usage-reset-tracker/releases">Releases</a></p>
      <p><sub>TypeScript · Chrome Extension APIs · Browser automation · Local-first data</sub></p>
    </td>
  </tr>
</table>

## Internal Product System · YuanMil Hotel Operations Console

<p align="center">
  <img src="assets/products/yuanmil-hotel-operations.gif" alt="YuanMil Hotel Operations Console walkthrough showing map-based hotel search, rate and cancellation-policy comparison, and commission analytics" width="100%" />
</p>

**Internal hospitality operations platform · Hotel discovery · Rate intelligence · Commission analytics**

This is a substantial internal operations system—not a small demo or a standalone UI experiment. It supports hotel discovery by map area, availability and rate comparison, cancellation-policy review, and commission analysis across travel dates. The goal is to turn fragmented hotel-sourcing and pricing work into a single operational workflow.

The portfolio walkthrough uses **32 fictional hotels** and **30 days of simulated data** to demonstrate the product experience without exposing internal hotel, supplier, or business information. The production system and source code are private; this GIF is a visual product walkthrough, not a claim that the underlying system is open source.

## Applied AI & Research

### DiscoveryHub · Drew Summer Science Institute (DSSI), Summer 2026

Built the query-side data and semantic-retrieval fine-tuning pipeline for matching pharma-side research-interest text with university technology-transfer listings and patent records.

- **26,648 normalized records:** 6,671 AUTM/TTO listings, 9,977 ClinicalTrials.gov records, and 10,000 USPTO patent records.
- **10,006 evaluation anchors** with query-document pairs, corpus records, relevance labels, and hard negatives.
- Fine-tuned and evaluated **Qwen3-Embedding-0.6B** and **multilingual-e5-large**.

| Embedding model | Recall@10: baseline → tuned | MRR@10: baseline → tuned | Median rank |
|---|---:|---:|---:|
| Qwen3-Embedding-0.6B | 54.3% → **67.3%** | 0.359 → **0.447** | 7 → **3** |
| multilingual-e5-large | 37.1% → **62.3%** | 0.238 → **0.406** | 42 → **4** |

**Data limitation:** ClinicalTrials.gov records were used as proxy research-interest text; they are not direct statements of companies' open-innovation priorities. Large model checkpoints and generated datasets are not included in the repository.

[Research repository](https://github.com/YinL-k/discoveryhub-technology-transfer-matchmaker) · [Detailed results](https://github.com/YinL-k/discoveryhub-technology-transfer-matchmaker/blob/main/RESULTS.md)

## Selected Engineering Projects

### Smooth Hotel Map Zoom

<p align="center">
  <img src="assets/products/hotel-map-smooth-zoom-clean.gif" alt="MapLibre demo showing smooth zoom and animated hotel-marker clustering" width="90%" />
</p>

An offline-friendly **MapLibre GL JS** demo featuring continuous zoom, animated marker clustering, collision-aware transitions, and reduced-motion support. The demo uses **49 synthetic hotel records**.

[Live demo](https://yinl-k.github.io/hotel-map-smooth-zoom/) · [Source code](https://github.com/YinL-k/hotel-map-smooth-zoom)

### Google Skills Learning Agent

A guarded browser-automation scaffold that inspects visible course and lab state, validates safe next actions, and maintains learning notes. It deliberately does not complete quizzes or assessments, use personal cloud credentials, or bypass platform restrictions.

[Source code](https://github.com/YinL-k/google-skills-learning-agent)

### Web Launch Console

A Windows PowerShell/WPF control panel for launching static sites or custom web servers, supervising child processes, running health checks, viewing logs, and optionally creating Cloudflare Quick Tunnels.

[Source code](https://github.com/YinL-k/web-launch-console)

## Selected Open-Source Contributions

Selected **merged** contributions to public projects:

- **[Gulliver #23](https://github.com/laaielichter/Gulliver/pull/23)** — added SQL warning GV016 for `ORDER BY RANDOM()` / `RAND()` sampling patterns, with regression coverage.
- **Pixiv-Shaft [#1309](https://github.com/CeuiLiSA/Pixiv-Shaft/pull/1309) · [#1310](https://github.com/CeuiLiSA/Pixiv-Shaft/pull/1310)** — fixed Unicode-safe filename truncation and preserved legacy one-based page-number semantics.
- **[whyfull #19](https://github.com/amlaban65/whyfull/pull/19)** — added repeatable `--exclude` paths for full scans, including reporting and regression tests.
- **[NAGI BENCH #22](https://github.com/nagi-studio/nagi-bench/pull/22)** — contributed a GPT-5.4 / Codex CLI skeleton-watch benchmark artifact and registry entry.

## Technical Focus

| Area | Hands-on technologies and concepts |
|---|---|
| **Languages** | TypeScript · JavaScript · Python · Java · SQL · PowerShell |
| **Backend & product systems** | Spring Boot · Node.js · Redis/Lua · MySQL · payment workflows · idempotency and recovery |
| **AI & data** | LLM tool calling · MCP · embedding fine-tuning · semantic retrieval · ranking evaluation |
| **Frontend & integrations** | React · Vue 3 · uni-app · Chrome Extension APIs · OAuth 2.0 / PKCE · browser automation |

## Contact

Interested in software engineering, product engineering, and applied AI opportunities.

[LinkedIn](https://www.linkedin.com/in/xianzhuo-yin-602562331/) · [GitHub repositories](https://github.com/YinL-k?tab=repositories)
