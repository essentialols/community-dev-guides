```python
"""compare_quant_quality.py: Compares output quality and generation speed of two llama.cpp models side-by-side."""

import argparse
import time
from llama_cpp import Llama

def main():
    parser = argparse.ArgumentParser(description="Compares output quality and generation speed of two llama.cpp models.")
    parser.add_argument("model_path_1", help="Path to the first llama.cpp model (e.g., Q4_K_M.gguf).")
    parser.add_argument("model_path_2", help="Path to the second llama.cpp model (e.g., Q8_0.gguf).")
    parser.add_argument("--n_gpu_layers", type=int, default=-1,
                        help="Number of layers to offload to GPU (-1 for all, 0 for none). Default: -1.")
    args = parser.parse_args()

    prompts = [
        "Explain quantum entanglement simply.",
        "Write a short, uplifting poem about new beginnings.",
        "What are the main differences between a cat and a dog?",
        "Describe a future where AI and humans coexist peacefully.",
        "If you could have any superpower, what would it be and why?"
    ]

    # Extract model names for clearer output
    name1 = args.model_path_1.split('/')[-1]
    name2 = args.model_path_2.split('/')[-1]

    print(f"Loading model 1: {name1}")
    m1 = Llama(model_path=args.model_path_1, n_gpu_layers=args.n_gpu_layers, verbose=False)
    print(f"Loading model 2: {name2}")
    m2 = Llama(model_path=args.model_path_2, n_gpu_layers=args.n_gpu_layers, verbose=False)

    print("\n--- Starting Comparison ---\n")

    total_time_m1, total_time_m2 = 0, 0

    for i, prompt_text in enumerate(prompts):
        print(f"----- Prompt {i+1}/{len(prompts)} -----\nPrompt: {prompt_text}\n")

        # Model 1 generation
        start_time_m1 = time.time()
        out1 = m1.create_completion(prompt_text, max_tokens=100, temperature=0.7, stop=["\n", "User:", "###"])
        end_time_m1 = time.time()
        duration_m1 = end_time_m1 - start_time_m1
        text1 = out1['choices'][0]['text'].strip()
        total_time_m1 += duration_m1

        # Model 2 generation
        start_time_m2 = time.time()
        out2 = m2.create_completion(prompt_text, max_tokens=100, temperature=0.7, stop=["\n", "User:", "###"])
        end_time_m2 = time.time()
        duration_m2 = end_time_m2 - start_time_m2
        text2 = out2['choices'][0]['text'].strip()
        total_time_m2 += duration_m2

        print(f"Model 1 ({name1} - {duration_m1:.2f}s):")
        for line in text1.splitlines():
            print(f"  {line}")

        print("-" * 40)

        print(f"Model 2 ({name2} - {duration_m2:.2f}s):")
        for line in text2.splitlines():
            print(f"  {line}")

        print("\n" + "=" * 80 + "\n")

    print("\n--- Comparison Summary ---")
    avg_speed_m1 = total_time_m1 / len(prompts)
    avg_speed_m2 = total_time_m2 / len(prompts)
    print(f"Average generation speed for {name1}: {avg_speed_m1:.2f} seconds/prompt")
    print(f"Average generation speed for {name2}: {avg_speed_m2:.2f} seconds/prompt")
    print("\n--- End of Comparison ---")

if __name__ == "__main__":
    main()
```
