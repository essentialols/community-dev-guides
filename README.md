<div align="center">

# Community Dev Guides

### Real data from real developers. Not another LLM-generated listicle.

[![Guides](https://img.shields.io/badge/guides-5-blue)]()
[![Community Reports](https://img.shields.io/badge/total_data_points-147-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Every guide is built from real community discussions: actual benchmarks, tested solutions, and gotchas reported by practitioners. All claims include numbered source references linking to the original threads. Not generic advice an LLM could produce on demand.

</div>

---

## Guides

### AI / Local LLMs

| Guide                                                                             | Data Points                         | Source                     |
| --------------------------------------------------------------------------------- | ----------------------------------- | -------------------------- |
| **[48GB VRAM LLM Playbook](https://github.com/essentialols/48gb-vram-llm-guide)** | 38 data points from 72 user reports | r/LocalLLaMA (124 upvotes) |

> Model selection, quantization configs, VRAM calculator with formulas, multi-GPU PCIe bandwidth analysis, and real performance data. All claims source-linked with numbered references.

### DevOps / Infrastructure

| Guide                                                                                                   | Data Points                    | Source                 |
| ------------------------------------------------------------------------------------------------------- | ------------------------------ | ---------------------- |
| **[AI for Infrastructure as Code](https://github.com/essentialols/ai-infrastructure-as-code-guide)**    | 16 data points from 30 reports | r/devops (45 upvotes)  |
| **[DevOps to Platform Engineering](https://github.com/essentialols/devops-platform-engineering-guide)** | 30 data points from 49 reports | r/devops (151 upvotes) |

> How teams actually use LLMs for Terraform/CloudFormation, and career paths for the DevOps -> Platform Eng transition. Includes skills readiness matrix.

### Software Engineering

| Guide                                                                                             | Data Points                   | Source                |
| ------------------------------------------------------------------------------------------------- | ----------------------------- | --------------------- |
| **[Go Modular Monolith Architecture](https://github.com/essentialols/go-modular-monolith-guide)** | 7 data points from 17 reports | r/golang (34 upvotes) |

> Real patterns and pitfalls for structuring large Go codebases without drowning in complexity.

### Career

| Guide                                                                                                | Data Points                    | Source                 |
| ---------------------------------------------------------------------------------------------------- | ------------------------------ | ---------------------- |
| **[Entry-Level Dev Survival Guide](https://github.com/essentialols/entry-level-dev-survival-guide)** | 56 data points from 97 reports | r/webdev (355 upvotes) |

> What actually works for landing dev jobs in 2025-2026. Hiring data, portfolio strategies, and career paths aggregated from 200+ comments.

---

## How These Guides Are Made

1. **Demand scanning**: Reddit and StackOverflow are monitored for high-engagement questions (20+ comments, specific technical topics)
2. **Community data harvesting**: Thread comments are scraped and classified into benchmarks, solutions, gotchas, and configurations
3. **Enriched generation**: An LLM generates the guide structure, but real community data points are woven throughout
4. **Quality check**: Community citations are verified against source threads

The result: guides that contain information you can't get by just asking ChatGPT, because the value comes from aggregated real-world experience.

## Contributing

- **Found an error?** Open an issue or PR on the specific guide repo
- **Have a topic suggestion?** Open an issue here
- **Want to add your own data?** PRs with real benchmarks/experiences are always welcome

## License

All guides are MIT licensed.
