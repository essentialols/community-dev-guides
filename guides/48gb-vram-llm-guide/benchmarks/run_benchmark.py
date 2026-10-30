```python
import argparse
import time
import json
import subprocess
import shutil
import sys
from llama_cpp import Llama

# --- Constants ---
DEFAULT_PROMPTS = [
    "What is the capital of France?",
    "Tell me a short story about a brave knight and a dragon.",
    "Explain the concept of quantum entanglement in simple terms."
]
DEFAULT_MAX_TOKENS = 100
BENCHMARK_FILE = "benchmark_results.json"

# --- Utility Function for VRAM ---
def get_vram_usage():
    """
    Queries NVIDIA GPU VRAM usage if nvidia-smi is available.
    Returns VRAM usage in MB, or None if not available/error.
    """
    if shutil.which("nvidia-smi"):
        try:
            # Get VRAM used for all GPUs, sum them up
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, check=True
            )
            vram_mb = sum(int(x.strip()) for x in result.stdout.strip().split('\n') if x.strip().isdigit())
            return vram_mb
        except Exception as e:
            print(f"Warning: Could not query VRAM usage: {e}", file=sys.stderr)
            return None
    return None

# --- Main Benchmark Script ---
def main():
    parser = argparse.ArgumentParser(
        description="Benchmark LLM quantization performance using llama-cpp-python."
    )
    parser.add_argument(
        "model_path",
        type=str,
        help="Path to the GGUF model file (e.g., model.gguf)."
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"Maximum number of tokens to generate per prompt (default: {DEFAULT_MAX_TOKENS})."
    )
    parser.add_argument(
        "--n_gpu_layers",
        type=int,
        default=-1, # -1 means all layers, 0 means CPU
        help="Number of layers to offload to GPU (-1 for all, 0 for CPU). Default: -1."
    )
    args = parser.parse_args()

    # Store benchmark results
    benchmark_results = {
        "model_path": args.model_path,
        "max_tokens_per_prompt": args.max_tokens,
        "n_gpu_layers": args.n_gpu_layers,
        "individual_prompt_results": [],
        "average_results": {}
    }

    print(f"--- Starting LLM Benchmark for: {args.model_path} ---")

    # 1. Measure VRAM before model load
    vram_before = get_vram_usage()
    if vram_before is not None:
        print(f"VRAM usage before model load: {vram_before} MB")
        benchmark_results["vram_before_load_mb"] = vram_before

    # Load the LLM model
    print("Loading model...")
    load_start_time = time.perf_counter()
    try:
        llm = Llama(
            model_path=args.model_path,
            n_gpu_layers=args.n_gpu_layers,
            verbose=False, # Suppress llama_cpp output during benchmark
        )
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        print("Please ensure the model_path is correct and llama-cpp-python is installed with GPU support if n_gpu_layers > 0.")
        sys.exit(1)
    load_end_time = time.perf_counter()
    model_load_time = load_end_time - load_start_time
    print(f"Model loaded in {model_load_time:.2f} seconds.")
    benchmark_results["model_load_time_s"] = model_load_time

    # 2. Measure VRAM after model load (model footprint)
    vram_after = get_vram_usage()
    if vram_after is not None:
        print(f"VRAM usage after model load: {vram_after} MB")
        benchmark_results["vram_after_load_mb"] = vram_after
        if vram_before is not None:
            benchmark_results["vram_model_footprint_mb"] = vram_after - vram_before

    print("\n--- Running Prompts ---")
    all_ttfts = []
    all_tps = []

    # Run benchmark for each prompt
    for i, prompt in enumerate(DEFAULT_PROMPTS):
        print(f"\nPrompt {i+1}/{len(DEFAULT_PROMPTS)}: '{prompt}'")
        
        prompt_start_time = time.perf_counter()
        first_token_time = None
        total_generated_tokens = 0
        
        try:
            # Stream tokens for accurate TTFT and TPS
            for token_chunk in llm.create_completion(prompt, max_tokens=args.max_tokens, stream=True):
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                
                # Count only the newly generated output tokens
                if 'choices' in token_chunk and len(token_chunk['choices']) > 0 and 'text' in token_chunk['choices'][0]:
                    total_generated_tokens += 1 
        except Exception as e:
            print(f"Error during generation for prompt '{prompt}': {e}", file=sys.stderr)
            benchmark_results["individual_prompt_results"].append({
                "prompt": prompt, "status": "failed", "error": str(e)
            })
            continue # Skip to next prompt

        prompt_end_time = time.perf_counter()

        # Calculate metrics for the current prompt
        ttft = (first_token_time - prompt_start_time) if first_token_time else 0
        
        # Calculate generation duration from first token to last token
        generation_duration = (prompt_end_time - first_token_time) if first_token_time else 0
        
        tps = 0
        if total_generated_tokens > 1 and generation_duration > 0:
            # TPS for subsequent tokens (excluding the very first token time)
            tps = (total_generated_tokens - 1) / generation_duration 
        elif total_generated_tokens == 1 and ttft > 0:
            # If only one token, TPS cannot be properly measured for continuous flow.
            # We can approximate it as 1/TTFT, though it's less meaningful.
            tps = 1 / ttft 
        
        all_ttfts.append(ttft)
        all_tps.append(tps)

        # Store individual prompt results
        prompt_result = {
            "prompt": prompt,
            "max_tokens_requested": args.max_tokens,
            "tokens_generated": total_generated_tokens,
            "time_to_first_token_s": ttft,
            "tokens_per_second": tps,
            "total_generation_time_s": generation_duration,
            "status": "success"
        }
        benchmark_results["individual_prompt_results"].append(prompt_result)

        print(f"  Tokens Generated: {total_generated_tokens}")
        print(f"  Time to First Token (TTFT): {ttft:.4f} s")
        print(f"  Tokens per Second (TPS): {tps:.2f} t/s")
        print(f"  Total Generation Time (after first token): {generation_duration:.4f} s")

    # Calculate averages
    avg_ttft = sum(all_ttfts) / len(all_ttfts) if all_ttfts else 0
    avg_tps = sum(all_tps) / len(all_tps) if all_tps else 0

    benchmark_results["average_results"] = {
        "avg_time_to_first_token_s": avg_ttft,
        "avg_tokens_per_second": avg_tps,
    }

    print("\n--- Benchmark Summary ---")
    print(f"{'Metric':<35} {'Value':<15}")
    print(f"{'-'*50}")
    if "vram_model_footprint_mb" in benchmark_results:
        print(f"{'VRAM Usage (model footprint)':<35} {benchmark_results['vram_model_footprint_mb']} MB")
    elif "vram_after_load_mb" in benchmark_results:
        print(f"{'VRAM Usage (after load)':<35} {benchmark_results['vram_after_load_mb']} MB")
    else:
        print(f"{'VRAM Usage':<35} {'N/A'}")

    print(f"{'Model Load Time':<35} {benchmark_results['model_load_time_s']:.2f} s")
    print(f"{'Avg Time to First Token':<35} {avg_ttft:.4f} s")
    print(f"{'Avg Tokens per Second (generation)':<35} {avg_tps:.2f} t/s")
    print(f"{'Total Prompts Tested':<35} {len(DEFAULT_PROMPTS)}")
    print(f"{'Max Tokens per Prompt Requested':<35} {args.max_tokens}")
    print(f"{'GPU Layers Offloaded (n_gpu_layers)':<35} {args.n_gpu_layers}")
    
    # Save results to JSON
    try:
        with open(BENCHMARK_FILE, 'w') as f:
            json.dump(benchmark_results, f, indent=4)
        print(f"\nDetailed results saved to {BENCHMARK_FILE}")
    except IOError as e:
        print(f"Error saving results to {BENCHMARK_FILE}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```
