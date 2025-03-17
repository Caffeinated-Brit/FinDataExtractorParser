from collections import Counter

small_prompt = "Give me an essay about bees with at least 10 talking points."
large_prompt = """I need a comprehensive, highly detailed, and in-depth essay that reaches at least 5000 tokens about "The Role of Bees in the Global Ecosystem and Their Economic, Environmental, and Agricultural Impact." 

Please structure your response as follows:

1. **Introduction** (300+ words)
   - Overview of bees and their importance.
   - Brief history of beekeeping and pollination in human civilization.

2. **Pollination and Its Significance** (600+ words)
   - How bees contribute to plant reproduction.
   - The impact of pollination on global food supply.
   - Case studies of agricultural sectors dependent on bees.

3. **Biodiversity and Environmental Balance** (600+ words)
   - The role of bees in maintaining biodiversity.
   - How bee extinction would affect ecosystems.
   - Symbiotic relationships between bees and other species.

4. **Economic Contributions of Bees** (700+ words)
   - The financial impact of honey production, beeswax, and royal jelly.
   - Global market statistics on beekeeping industries.
   - Job creation and businesses dependent on bee-related products.

5. **Threats to Bee Populations** (800+ words)
   - Climate change and its effects on bee habitats.
   - Pesticides, pollution, and industrial farming risks.
   - Colony Collapse Disorder (CCD): causes and consequences.

6. **Scientific Research and Innovations in Beekeeping** (700+ words)
   - Genetic research on bee resilience.
   - AI and technology in monitoring bee health.
   - Sustainable beekeeping practices.

7. **Legal and Government Policies on Bee Conservation** (600+ words)
   - Global policies protecting bee populations.
   - Laws on pesticide usage affecting bees.
   - Conservation programs and their effectiveness.

8. **How Humans Can Help Bees** (500+ words)
   - Urban beekeeping and community initiatives.
   - Bee-friendly gardening and pesticide-free agriculture.
   - Education and advocacy for bee conservation.

9. **Conclusion** (500+ words)
   - Summary of key points.
   - Final thoughts on the importance of protecting bees.
   - Future outlook on bees in the global ecosystem.

📌 **Guidelines for the Response:**
- **Each section should be fully developed** with multiple examples, statistics, and references.
- **Use scientific, economic, and historical perspectives** to support each argument.
- **Include step-by-step breakdowns, comparisons, and case studies** where applicable.
- **Ensure a long and detailed response**, reaching as close as possible to 5000 tokens.
"""

request_count = 50

def benchmark_vllm(prompt):
    from FinDataExtractorParser.AI import Vllm
    vllm_results, vllm_total_time = Vllm.run_benchmarking(request_count, prompt)

    total_generated_tokens = sum(result[2] for result in vllm_results)

    # Counting occurrences of each response
    response_texts = [result[0] for result in vllm_results]
    response_counts = Counter(response_texts)

    unique_responses = len(response_counts)
    most_common_response, most_common_count = response_counts.most_common(1)[0]  # Get most common response
    repeatability_percentage = ((request_count - unique_responses) / (request_count - 1)) * 100

    average_elapsed_time = vllm_total_time / request_count
    average_generated_tokens = total_generated_tokens / request_count
    average_throughput = total_generated_tokens / vllm_total_time

    return {
        "model": "Vllm",
        "total_tokens": total_generated_tokens,
        "repeatability_percentage": repeatability_percentage,
        "most_common_response": most_common_response,
        "most_common_count": most_common_count,
        "average_time_per_prompt": average_elapsed_time,
        "average_throughput": average_throughput,
        "average_generated_tokens": average_generated_tokens,
        "total_time": vllm_total_time
    }


def benchmark_ollama(prompt):
    from FinDataExtractorParser.AI import Ollama
    ollama_results, ollama_total_time = Ollama.run_benchmarking(request_count, prompt)

    total_generated_tokens = sum(result[2] for result in ollama_results)

    # Counting occurrences of each response
    response_texts = [result[0] for result in ollama_results]
    response_counts = Counter(response_texts)

    unique_responses = len(response_counts)
    most_common_response, most_common_count = response_counts.most_common(1)[0]  # Get most common response
    repeatability_percentage = ((request_count - unique_responses) / (request_count - 1)) * 100

    average_elapsed_time = ollama_total_time / request_count
    average_generated_tokens = total_generated_tokens / request_count
    average_throughput = total_generated_tokens / ollama_total_time

    return {
        "model": "Ollama",
        "total_tokens": total_generated_tokens,
        "repeatability_percentage": repeatability_percentage,
        "most_common_response": most_common_response,
        "most_common_count": most_common_count,
        "average_time_per_prompt": average_elapsed_time,
        "average_throughput": average_throughput,
        "average_generated_tokens": average_generated_tokens,
        "total_time": ollama_total_time
    }


# Run both benchmarks and store results
vllm_results = benchmark_vllm(large_prompt)
#ollama_results = benchmark_ollama(large_prompt)

print("\nFinal Benchmarking Summary:")
print("=" * 50)
for result in [
    #ollama_results,
    vllm_results
    ]:
    print(f"\nBenchmarking Results for {result['model']}:")
    print("-" * 50)
    print(f"Total Tokens Generated: {result['total_tokens']:.2f}")
    print(f"Repeatability Percentage: {result['repeatability_percentage']:.2f}%")
    print(
        f"Most Common Response (Occurred {result['most_common_count']} times):\n{result['most_common_response'][:500]}...")  # Truncate for display
    print(f"Average Time Per Prompt: {result['average_time_per_prompt']:.2f} seconds")
    print(f"Average Throughput: {result['average_throughput']:.2f}")
    print(f"Average Generated Tokens Per Prompt: {result['average_generated_tokens']:.0f}")
    print(f"Total Time: {result['total_time']:.2f} seconds")
    print("-" * 50)