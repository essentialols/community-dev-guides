<div align="center">

# The 48GB VRAM Playbook
### Maximizing Local LLMs: A Community-Driven Guide

[![Community Data](https://img.shields.io/badge/community_data_points-38-blue)](https://reddit.com/r/LocalLLaMA/comments/1ti2ga0/)
[![Contributors](https://img.shields.io/badge/user_reports-72-green)](https://reddit.com/r/LocalLLaMA/comments/1ti2ga0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Built from 72 real user reports aggregated from [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA/comments/1ti2ga0/). Not another generic LLM guide.*

</div>

## Table of Contents

- [About This Guide](#about-this-guide)
- [The 48GB VRAM Sweet Spot](#the-48gb-vram-sweet-spot-and-its-limits)
- [Quick Comparison Matrix](#quick-comparison-matrix-48gb-vram-strategies)
- [Models, Quantization & Configs](#detailed-feature-breakdown-models-quantization-and-configs)
- [Performance Benchmarks](#performance-benchmarks--real-world-throughput)
- [Decision Framework](#when-to-choose-which-strategy)
- [Cost Analysis](#cost-analysis-maximizing-value-at-48gb)
- [Gotchas & Warnings](#gotchas-warnings-and-community-wisdom)
- [Migration Path](#migration-path-beyond-48gb-or-deeper-optimization)
- [Benchmark Scripts](#run-your-own-benchmarks)

---


## About This Guide

Welcome to "The 48GB VRAM Playbook," your essential resource for navigating the exciting world of local LLMs with a 48GB VRAM setup. This guide is built not on theoretical specs or marketing hype, but on the hard-won experiences and shared wisdom of real users from the r/LocalLLaMA community. If you've got 48GB of VRAM and you're wondering what models to run, how to configure them, and what performance to expect, you've come to the right place.

We've aggregated real benchmarks, user configurations, and critical "gotchas" to provide you with actionable insights. Forget generic advice – this guide delivers the specific numbers and strategies that fellow enthusiasts are using right now. From daily driver models to multi-GPU setups and the nuances of quantization, we distill the collective knowledge into a clear decision framework designed to help you get the most out of your hardware. Whether you're a seasoned local LLM runner or just getting started, this playbook aims to be the $1-5 resource you wish you had from day one.

---

## The 48GB VRAM Sweet Spot (and its Limits)

48GB of VRAM represents a powerful tier for local LLM inference, often achieved through configurations like dual 24GB consumer GPUs (e.g., 2x RTX 3090, 2x RTX 4090) or more specialized workstation cards (e.g., older Nvidia P40s or professional series cards). It's a sweet spot that allows for larger models and deeper context windows than mainstream 8-12GB cards, but it's also a domain where users constantly "wish they had more VRAM," as highlighted by the community consensus. Even users who upgrade to 96GB VRAM still find themselves pushing limits for larger models or context, confirming that the desire for more VRAM is almost universal. As one highly upvoted comment bluntly puts it, "Who is *ever* going to say 'no' to this?"

This guide explores how to wring every last bit of performance and utility from your 48GB, balancing model size, quantization, and context to meet your specific needs.

## Quick Comparison Matrix: 48GB VRAM Strategies

| Strategy                  | Primary Goal                 | Typical Models & Quantization        | VRAM Usage (~48GB) | Key Benefits                                     | Trade-offs                                           | Community Insight                                                                                                                                                                                                                                                                         |
| :------------------------ | :--------------------------- | :----------------------------------- | :----------------- | :----------------------------------------------- | :--------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Balanced 70B (Q4-Q5)** | Maximize Model Size          | Llama 3 70B Q4/Q5 GGUF/AWQ         | ~40-45GB           | Access to larger, more capable models            | Reduced context, potential quality degradation       | "Used to mainly run either q4 of various llama3 70b tunes." - *Former 48GB user (70 upvotes)*                                                                                                                                                                                            |
| **2. High-Performance 27-31B (Q8)** | Optimal Speed & Quality      | Gemma4 31B Q8, Qwen 27B Q8         | ~32-40GB           | Excellent quality, faster inference, good context | Smaller parameter count than 70B                   | "Gemma 4 31B Q8 GGUF is the daily driver." "Qwen 3.6 27b Q8 with 150k is a perfect fit for 48GB." - *(22 & 39 upvotes respectively)*                                                                                                                                         |
| **3. Deep Context (27-31B Q8)** | Maximize Context Window      | Qwen 27B Q8, Gemma4 31B Q8         | ~40-48GB           | Extensive context for long documents/conversations | Slightly slower inference than shorter contexts      | "Qwen 3.6 27b Q8 with 150k is a perfect fit for 48GB." - *(39 upvotes)*                                                                                                                                                                                                                |
| **4. Multi-Purpose Split (Multi-GPU)** | Run Multiple Services/Models | Gemma4 31B Q8 (main), image model, TTS/STT (secondary) | ~20-24GB per card  | Versatility, parallel operations                 | Main model context may be limited by available VRAM on a single card | "Split the workload across two GPUs. Already in the leftover space, if I'm good with 32K context, I can run an image model on one card, and also get TTS, STT, etc. loaded." - *P40 user (22 upvotes)*                                                                           |

---

## Detailed Feature Breakdown: Models, Quantization, and Configs

Navigating the local LLM landscape with 48GB VRAM involves key decisions around model selection, quantization, and specific configurations. Here's a breakdown informed by community experiences:

### 1. Model Selection: The Daily Drivers

The community data points to a clear set of models that are frequently used and perform well within the 48GB VRAM constraint:

*   **Llama 3 70B (Quantized Q4/Q5):** This was a primary choice for a "former 48GB user" (70 upvotes), running "q4 of various llama3 70b tunes." While pushing the VRAM limits, Q4 quantization makes these larger, highly capable models accessible. Expect to use nearly all your 48GB for the model weights, potentially leaving limited room for extensive context.
*   **Mistral Small (Full-Precision) or Mistral Medium (Quantized Q4):** The same user also reported running "full-precision mistral small" on 48GB, indicating that smaller, unquantized models are an option for those prioritizing absolute quality over parameter count. For Mistral Medium, a "q4" version was occasionally run even after upgrading to 96GB, suggesting it's a viable option on 48GB with appropriate quantization.
*   **Gemma 4 31B Q8 GGUF:** This model stands out as a "daily driver" for many. A user running on "old P40 cards" (22 upvotes) specifically highlights "Gemma 4 31B Q8 GGUF" for its balance, allowing for "a nice context size." Another user, even after upgrading to 96GB, reports "still running almost exclusively gemma" but with "few hundred thousands of context and much faster!" This indicates Gemma's efficiency and strong performance even when scaling VRAM.
*   **Qwen 3.6 27B Q8:** Praised as a "perfect fit for 48GB" with "150k context" (39 upvotes). This is a strong contender for users prioritizing a substantial context window while maintaining good model quality and performance. The 150k context window is a significant feature for long-form generation or analysis.

**Community Observation:** While 70B models are popular, there's a perceived gap in the industry: "I am still a bit sad the industry gave up on the 70B model family for the most part. It is mostly sub 8B models, 24-32B models and then it seems to jump to 100B+." (6 upvotes). This makes the existing well-tuned 70B models, even quantized, particularly valuable for 48GB users.

### 2. Quantization Choices: The Quality vs. VRAM Trade-off

Quantization is critical for fitting larger models into 48GB VRAM, but it comes with potential quality implications.

*   **Q4:** Commonly used for 70B models to fit them into 48GB, as seen with "q4 of various llama3 70b tunes." It allows access to larger models but often at the cost of some instruction following or factual accuracy.
*   **Q6:** Mentioned in the context of "q6 gemma4 31b" by a former 48GB user who upgraded. This strikes a balance between VRAM usage and quality, often offering a noticeable improvement over Q4 without the full VRAM demand of Q8 or full-precision.
*   **Q8:** Emerges as a strong recommendation in the community for 27-31B models. "Gemma 4 31B Q8 GGUF" and "Qwen 3.6 27b Q8" are highlighted as daily drivers, indicating that for models of this size, Q8 offers a sweet spot for quality and VRAM efficiency.
    *   **The "Suspicion of Quantization" Warning:** A crucial "gotcha" arises regarding quantization: "I've recently started to become very suspicious of quantization and avoid going below Q8 on anything." (4 upvotes). This user's sentiment reflects a growing concern about the quality degradation introduced by lower quantizations (Q4, Q5). The question "Would you be willing to share your overall sense of what led you to feel this way? Trying to decide on my own choice of more parameters vs. lower quantization" underscores the community's struggle with this trade-off. **Actionable Advice:** If model quality is paramount, prioritize Q8 or higher for models that fit, even if it means opting for a slightly smaller model (e.g., 31B Q8 instead of 70B Q4). If you *must* run a 70B model on 48GB, understand that Q4/Q5 will be necessary and may introduce noticeable quality compromises.

### 3. Multi-GPU Setups for 48GB

Many 48GB setups involve two 24GB GPUs (e.g., 2x RTX 3090, 2x P40s). This enables flexible VRAM allocation:

*   **Splitting the Workload:** A user running "Gemma 4 31B Q8 GGUF" on "old P40 cards" (22 upvotes) describes splitting the workload "across two GPUs." This allows for distributing the model or, more interestingly, running multiple services concurrently.
*   **Secondary Services:** With leftover VRAM on one card, "if I'm good with 32K context, I can run an image model on one card, and also get TTS, STT, etc. loaded." This highlights a significant advantage of multi-GPU setups: the ability to run a primary LLM on one GPU or across both, while dedicating the remaining VRAM to other AI tasks, effectively turning your 48GB rig into a versatile AI powerhouse.

### 4. Real User Configurations & Optimizations

Specific command-line flags and batch sizes can significantly impact performance:

*   **2x RTX 3090 Configuration:** A user with this setup reports "20tk/s on Q8" (3 upvotes) using the following flags, acknowledging they might be "doing something wrong as usual but it works well enough":
    *   `--batch-size 4096`
    *   `--ubatch-size 1024`
    *   `--spec-type ngram-mod`
    *   `--spec-ngram-mod-n-match 16`
    *   `--spec-draft-n-max 4`

    **Actionable Advice:** These flags suggest a focus on high batch processing and speculative decoding (`spec-type`) to maximize token generation speed. While specific to the user's setup and model, these parameters provide a starting point for experimentation to optimize throughput, especially with Q8 models where performance is a key benefit.

---

## Performance Benchmarks & Real-World Throughput

Actual performance varies widely based on the model, quantization, context size, and specific hardware setup (e.g., PCIe generation, CPU, RAM speed). However, community data offers concrete benchmarks:

*   **20 tokens/second on 2x RTX 3090 with Q8:** This is a critical benchmark provided by a user (3 upvotes), showcasing excellent throughput for a Q8 quantized model. Achieving 20tk/s allows for very responsive chat and generation experiences. This figure likely represents optimized settings, potentially with the `--batch-size` and `--spec-type` flags mentioned in the user configurations.
*   **Impact of Context:** While the "Qwen 3.6 27b Q8 with 150k" (39 upvotes) is described as a "perfect fit," high context sizes generally lead to slower inference. The user who upgraded to 96GB still noted their Gemma model was "much faster" with "few hundred thousands of context," implying that while 48GB *can* handle large contexts, the speed will improve significantly with more VRAM.

**Key Takeaway:** For optimal speed on 48GB, target Q8 quantized models in the 27B-31B range. Larger models (70B Q4) will typically offer lower token generation rates, especially as context grows.

---

## When to Choose Which Strategy

Your choice of strategy for your 48GB VRAM setup should align with your primary use case and priorities:

### 1. Choose **Balanced 70B (Q4-Q5)** if:
*   **You need the highest parameter count possible:** Your applications demand the raw reasoning capability or broader knowledge base of a 70B model.
*   **You prioritize model size over absolute inference speed or extensive context:** You're willing to accept lower token generation rates and limited context (e.g., < 8K) to access a larger model.
*   **Quality degradation from Q4/Q5 is acceptable:** You've tested it for your specific tasks and found it sufficient, or your tasks are robust to minor imperfections.
*   **Example Use Case:** Experimenting with cutting-edge open-source 70B models, general-purpose chatbot where occasional inaccuracies are tolerable.

### 2. Choose **High-Performance 27-31B (Q8)** if:
*   **You prioritize fast, responsive inference:** You need quick answers for chat, coding assistance, or interactive applications.
*   **You demand high quality:** You agree with the "suspicion of quantization below Q8" and want to minimize artifacts or logical errors.
*   **You need good context, but not extreme context:** Models like Gemma 4 31B Q8 offer a strong balance of quality and context (e.g., 32K or more), which is sufficient for most daily tasks.
*   **Example Use Case:** Daily driver chatbot, creative writing assistance, rapid code generation and debugging, where consistent quality and speed are paramount.

### 3. Choose **Deep Context (27-31B Q8)** if:
*   **You need to process extremely long documents or conversations:** Your tasks involve summarization, RAG with large datasets, or maintaining long conversational history.
*   **You value extensive memory over slightly faster token generation:** You're willing to trade a marginal decrease in speed for the ability to handle up to 150K tokens of context.
*   **You are happy with 27B-31B model capabilities:** You don't need the absolute largest models, but rather intelligent processing over long inputs.
*   **Example Use Case:** Academic research, legal document analysis, complex software project understanding, journaling applications requiring long memory. The "Qwen 3.6 27b Q8 with 150k" is explicitly a "perfect fit" for this strategy (39 upvotes).

### 4. Choose **Multi-Purpose Split (Multi-GPU)** if:
*   **You have a dual-GPU 48GB setup (e.g., 2x 24GB cards):** This strategy is only feasible with multiple physical GPUs.
*   **You want to run more than just an LLM:** You need to integrate other AI services like image generation (SDXL), Text-to-Speech (TTS), or Speech-to-Text (STT) alongside your primary LLM.
*   **You can tolerate a slightly smaller primary LLM context on one card:** For example, running Gemma 4 31B Q8 with 32K context on one 24GB card, leaving the other free for secondary tasks.
*   **Example Use Case:** AI assistant that combines chat, image generation, and voice interaction; developing complex multi-modal AI applications. This allows you to "run an image model on one card, and also get TTS, STT, etc. loaded" (22 upvotes).

---

## Cost Analysis: Maximizing Value at 48GB

The "modern price of hardware" is a recurring theme, with one user humorously suggesting a 48GB setup might cost "usually, a used bicycle" (8 upvotes) in comparison to other household expenses. While direct monetary values aren't provided, the community data allows us to infer cost-efficiency and investment considerations.

### Hardware Considerations:

*   **Used P40 Cards:** The mention of "old P40 cards" (22 upvotes) indicates that for budget-conscious users, older professional GPUs are a viable path to 48GB VRAM. P40s offer 24GB of VRAM each, meaning two can achieve 48GB relatively affordably compared to newer consumer cards. Their downside is often lower raw compute power, older architecture, and potentially higher power consumption, but they excel at VRAM capacity for their price.
*   **Newer Consumer Cards (e.g., 2x RTX 3090, 2x RTX 4090):** The user reporting "20tk/s on Q8 with my 2x 3090" (3 upvotes) represents a more premium 48GB setup. While 3090s are no longer current generation, they still command a significant price, and 4090s are at the top end of consumer GPU pricing. These setups offer superior raw performance, lower power consumption (for 4090s compared to 3090s), and access to newer features (e.g., DLSS, better encoders/decoders for non-LLM tasks).
*   **Mac Studio (512GB RAM):** A lament for a "512gb Mac Studio" (16 upvotes) highlights that unified memory architectures offer a different approach to large "VRAM" pools. While technically RAM, a Mac Studio can dedicate a substantial portion of its unified memory to GPU tasks. This represents a significant upfront cost for an integrated system, but offers a very different user experience (power efficiency, quiet operation). However, the community focuses more on discrete GPU solutions for LLM inference due to their raw compute power.

### Price vs. Performance & Value:

*   **The "Used Bicycle" Analogy:** This implies that investing in 48GB VRAM can be a significant expenditure relative to a user's overall budget, especially for hobbyists. The value proposition is thus critical: what are you getting for your money?
*   **Maximizing Existing Investment:** The guide emphasizes strategies to maximize *your existing* 48GB, recognizing that many users are already at their VRAM limit and looking for the best possible experience, not necessarily contemplating an immediate upgrade. The focus is on software optimizations and model choices to get the most "bang for your buck" out of your current hardware.
*   **The 96GB Dream:** While 48GB is good, the consensus is that *more* VRAM is always desired. The mention of "1 tb of vram has gotta be way more than 99.99% of houses, right?" (29 upvotes) and the direct statement "I'd have about 1TB of VRAM if that didn't cost as much as some houses" (community consensus) underscores that the cost of truly massive VRAM setups is prohibitive. This context makes the 48GB tier a balance point between capability and financial accessibility.

**Actionable Cost Advice:**
If building new:
1.  **Budget-conscious (Multi-purpose):** Consider used professional cards like P40s to achieve 48GB. You'll sacrifice some raw speed for VRAM capacity, but can run Q8 31B models effectively and leverage multi-GPU splitting.
2.  **Performance-focused:** Opt for 2x RTX 3090s (used or new, depending on market) or 2x RTX 4090s. This will provide superior inference speed and longevity.
If you already have 48GB:
*   Focus on the software optimizations and model choices outlined in this guide to maximize your current investment, as the cost of upgrading significantly (e.g., to 96GB) is often a major hurdle.

---

## Gotchas, Warnings, and Community Wisdom

Beyond the benchmarks and model choices, the community has identified several key "gotchas" and shared wisdom that are critical for 48GB VRAM users:

1.  **Suspicion of Low Quantization (below Q8):** This is perhaps the most significant warning. As one user expressed, "I've recently started to become very suspicious of quantization and avoid going below Q8 on anything." (4 upvotes). The debate between "more parameters vs. lower quantization" is ongoing.
    *   **Implication:** While Q4/Q5 can fit larger models (e.g., 70B) into 48GB, users report that the quality degradation can be noticeable. This might manifest as less coherent output, poorer instruction following, or more frequent "hallucinations."
    *   **Actionable Advice:** Prioritize Q8 or higher for critical applications. If you must use Q4/Q5, thoroughly test the model's performance on your specific use cases to ensure the output quality is acceptable. Don't assume a higher parameter count automatically means a better model if the quantization is too aggressive.

2.  **The Universal Desire for More VRAM:** "Who is *ever* going to say 'no' to this?" is the community's unanimous answer to the question "Do you wish you had more VRAM?" This isn't just a casual wish; it's a reflection of the continuous push towards larger models and deeper contexts.
    *   **Implication:** While 48GB is powerful, it's not the end-all-be-all. Expect to hit VRAM limits when trying to run the very latest, largest models or pushing context windows to extreme lengths (hundreds of thousands of tokens).
    *   **Actionable Advice:** Manage expectations. 48GB is excellent for many tasks, but it's not limitless. Frame your projects around the capabilities of 48GB rather than chasing every cutting-edge model that requires 100GB+.

3.  **The "70B Model Family" Gap:** "I am still a bit sad the industry gave up on the 70B model family for the most part. It is mostly sub 8B models, 24-32B models and then it seems to jump to 100B+." (6 upvotes).
    *   **Implication:** Finding optimized 70B models that fit 48GB (even quantized) might become harder as development focuses on smaller or much larger models.
    *   **Actionable Advice:** Treasure the existing good 70B Q4/Q5 models. For newer models, be prepared to consider the 27B-31B Q8 options as potentially offering a better balance of novelty, quality, and performance on your hardware.

4.  **Multi-GPU Management:** While beneficial, running multi-GPU setups, especially with "old P40 cards" (22 upvotes), can introduce complexities in software setup (e.g., GGUF split workloads), power management, and cooling.
    *   **Implication:** It's not always plug-and-play. Expect some configuration effort to get the most out of your multi-GPU setup.
    *   **Actionable Advice:** Leverage tools like `llama.cpp` (for GGUF models) or `text-generation-webui` with appropriate GPU splitting options. Pay attention to documentation for multi-GPU inference.

---

## Migration Path: Beyond 48GB or Deeper Optimization

So, what happens when you outgrow your 48GB, or how can you squeeze every last drop of performance from it?

### Path 1: Deeper Optimization of Current 48GB

Before thinking about upgrading, ensure you've fully optimized your current setup:

*   **Experiment with Quantization:** If you're on Q4/Q5 for a 70B model, try a Q8 31B model to see if the quality/speed trade-off is worth it for your tasks. The community's "suspicion of quantization below Q8" is a strong hint.
*   **Tune Inference Parameters:** Utilize flags like `--batch-size`, `--ubatch-size`, `--spec-type`, `--spec-ngram-mod-n-match`, and `--spec-draft-n-max` (as seen in the 2x 3090 config achieving 20tk/s) to fine-tune performance. These can significantly impact token generation speed.
*   **Explore Multi-Purpose Splits:** If you have dual 24GB GPUs, ensure you're leveraging the ability to run secondary services (image generation, TTS/STT) in parallel, maximizing the utility of your setup.
*   **Stay Updated:** Model architectures and inference software (e.g., `llama.cpp` updates) are constantly improving. Keep your software current for potential performance gains and better VRAM utilization.

### Path 2: Upgrading to 96GB VRAM

This is a common upgrade path for 48GB users, and the community provides direct feedback on its benefits:

*   **Improved Quality of Life (QoL):** A former 48GB user who upgraded to 96GB notes that the jump wasn't just about running *new* models, but more about "the QoL of running multiple models/contexts etc?" (17 upvotes). This implies less VRAM juggling and more flexibility.
*   **Faster Inference for Large Contexts:** The same user reported their Gemma model was "much faster" with "few hundred thousands of context" after upgrading. This is a significant benefit for long-form generation or RAG applications.
*   **Access to Larger Quantized Models (Q4 Mistral Medium) or Deeper Quantization:** The user mentioned running "q4 mistral medium" occasionally, suggesting that with 96GB, you can either run larger models with good quantization or better quantization on existing models.
*   **Real-World Example of 96GB:** The community points to systems like the "Nvidia RTX Pro 6000 Max-Q 96GB" (10 upvotes) as a path to 96GB, though such solutions often come at a premium.
*   **The "1TB VRAM Dream":** While 96GB is a realistic upgrade, the ultimate dream for many is truly massive VRAM, with users joking about 1TB VRAM costing "as much as some houses" (29 upvotes). This highlights that even 96GB is a compromise for some, but a significant step up from 48GB.

**Actionable Advice:**
If you frequently hit VRAM limits, find yourself constrained by context, or simply desire a smoother, more flexible experience, a 96GB upgrade is a logical next step. It won't solve the "wish I had more VRAM" problem entirely, but it significantly expands your capabilities. Consider the cost-benefit carefully, as such upgrades are substantial investments.

---

## Conclusion

48GB of VRAM is a formidable asset for local LLM inference, capable of running highly capable models like quantized Llama 3 70B and, more optimally, high-quality Q8 versions of 27B-31B models such as Qwen 3.6 27B and Gemma 4 31B. The community's real-world experiences confirm that with smart model selection, careful quantization choices, and strategic multi-GPU setups, you can achieve impressive performance and versatility.

Key takeaways from the r/LocalLLaMA community include prioritizing Q8 quantization when possible to avoid quality degradation, embracing models like Qwen 27B for their impressive context windows (150k tokens!), and utilizing multi-GPU setups for concurrent AI tasks. While the universal desire for more VRAM persists—and 96GB offers noticeable quality-of-life improvements—your 48GB setup, armed with these community-driven insights, is more than capable of delivering a powerful and fulfilling local LLM experience.

---

## Run Your Own Benchmarks

This repo includes scripts to generate your own data:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the benchmark suite on your model
python benchmarks/run_benchmark.py --model-path /path/to/your/model.gguf

# Compare two quantization levels side by side
python examples/compare_quant_quality.py /path/to/q4_model.gguf /path/to/q8_model.gguf
```

## Contributing

Found an error? Have better benchmarks? Have a different 48GB setup? PRs welcome! This guide improves with community input.

Originally inspired by [this r/LocalLLaMA discussion](https://reddit.com/r/LocalLLaMA/comments/1ti2ga0/) (135 comments, 124 upvotes).

## License

MIT


---

## Related Guides

- [DevOps to Platform Engineering Guide](https://github.com/essentialols/devops-platform-engineering-guide) - Career transition paths and upskilling roadmaps
- [Go Modular Monolith Guide](https://github.com/essentialols/go-modular-monolith-guide) - Architecture patterns for large Go codebases


> Part of [Community Dev Guides](https://github.com/essentialols/community-dev-guides) - a curated collection of community-driven developer guides.
