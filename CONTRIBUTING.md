# Contributing

These guides improve with real data. Here's how to help.

## Add your benchmark data

The most valuable contribution is a real benchmark with full details:

```markdown
**Hardware:** GPU model, CPU, RAM, OS
**Software:** llama.cpp version, CUDA version, driver version
**Model:** exact model name + quantization (e.g., Qwen 1.5 32B Q8 GGUF)
**Test:** what you ran (prompt, temperature, number of runs)
**Result:** tokens/sec, VRAM usage, any quality observations
```

Open a PR on the specific guide repo with your data. Even one benchmark with proper methodology is more valuable than ten anecdotes.

## Fix an error

If you spot a wrong model name, broken link, or inaccurate claim, open an issue or PR on the relevant guide repo:

- [48GB VRAM LLM Playbook](https://github.com/essentialols/48gb-vram-llm-guide)
- [Entry-Level Dev Survival Guide](https://github.com/essentialols/entry-level-dev-survival-guide)
- [AI for Infrastructure as Code](https://github.com/essentialols/ai-infrastructure-as-code-guide)
- [DevOps to Platform Engineering](https://github.com/essentialols/devops-platform-engineering-guide)
- [Go Modular Monolith](https://github.com/essentialols/go-modular-monolith-guide)

## Suggest a new guide topic

Open an issue on this hub repo with:

- Link to a Reddit/SO thread with 20+ comments
- Why you think it would make a good guide
- What's missing from existing resources on the topic

## Style guidelines

These guides follow the writing patterns of [Toni Sagrista](https://tonisagrista.com/blog/2026/quantization/), [Sebastian Raschka](https://magazine.sebastianraschka.com), and [Enclave AI](https://enclaveai.app/blog/):

- First person, honest about uncertainty
- Every claim has a numbered source reference
- Unverified community reports are explicitly flagged
- Tables with real numbers, not vague descriptions
- 5 numbered takeaways at the end
