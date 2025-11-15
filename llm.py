from llama_cpp import Llama
import time
import json

# Initialize the model with VPS-optimized settings
llm = Llama(
    model_path=r"F:\image model test\llama-2-13b.Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=8,
    n_batch=512,
    verbose=False
)

# Article to paraphrase
original_article = """The Minister of Livestock and Rural Development of Somaliland, Omar Shucayb Mohamed, who participated in the Consultative Meeting on Addressing Trade Barriers and Enhancing Livestock Exports, stated that the country's economy heavily relies on livestocks, emphasizing that this sector generates the majority of the nation's hard currency earnings.

He said: "When looking at the national economy, 70% of our revenue comes from livestock."

The consultative meeting on livestock trade barriers and export development, held yesterday in Hargeisa, focused on the challenges facing livestock trade and export promotion in Somaliland. Experts examined various aspects, including obstacles affecting livestock and their export processes.

Organized by the Ministry of Livestock and Rural Development, the meeting was attended by the Minister of Livestock and Rural Development, the Minister of Trade and Tourism of Somaliland, livestock traders, stakeholders, and other experts.

Speaking at the forum, Minister Omar Shucayb Mohamed described Somaliland's livestock as the backbone of the national economy, but highlighted two major challenges:

The domestic livestock market system, and

The traditional livestock management practices, which are no longer beneficial given global climate change impacts.

The Minister urged livestock exporters to prioritize animal care before export, particularly while animals are in quarantine facilities. He called for the provision of high-quality, nutrient-rich feed to improve animal weight and overall health.

Somaliland is working to introduce nutrient-rich livestock feed to enhance the quality of animals both for export and domestic markets. This will ensure animals meet health standards, improve physical condition, and strengthen the sector—since live animals are the primary source of national revenue."""

# Count original words and paragraphs
original_word_count = len(original_article.split())
original_paragraphs = len([p for p in original_article.split('\n\n') if p.strip()])

# Prompt that emphasizes maintaining length and detail
prompt = f"""Paraphrase this article paragraph by paragraph. Use different words but keep the SAME LENGTH and ALL details. Do not summarize or shorten anything.

Original Article ({original_word_count} words):
{original_article}

Paraphrased Version (must be approximately {original_word_count} words):"""

# Measure inference time
print("Starting paraphrasing...")
print(f"Original article: {original_word_count} words, {original_paragraphs} paragraphs\n")
start_time = time.time()

output = llm(
    prompt,
    max_tokens=3500,  # Generous token limit for full paraphrase
    temperature=0.7,
    top_p=0.9,
    repeat_penalty=1.15,
    stop=["</s>", "\n\n\nOriginal Article:", "###"],
)

end_time = time.time()
inference_time = end_time - start_time

# Extract the generated text
paraphrased_text = output["choices"][0]["text"].strip()

# Count paraphrased words
paraphrased_word_count = len(paraphrased_text.split())
length_match_percentage = (paraphrased_word_count / original_word_count) * 100

# Create structured output
result = {
    "original_article": original_article,
    "paraphrased_article": paraphrased_text,
    "statistics": {
        "original_word_count": original_word_count,
        "paraphrased_word_count": paraphrased_word_count,
        "length_match_percentage": round(length_match_percentage, 2),
        "inference_time_seconds": round(inference_time, 2),
        "tokens_per_second": round(paraphrased_word_count / inference_time, 2)
    }
}

# Display results
print("=" * 70)
print("PARAPHRASED ARTICLE")
print("=" * 70)
print(paraphrased_text)

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"Original Words:    {original_word_count}")
print(f"Paraphrased Words: {paraphrased_word_count}")
print(f"Length Match:      {length_match_percentage:.1f}%")

if length_match_percentage < 80:
    print("⚠️  Warning: Paraphrased version is significantly shorter than original")
elif length_match_percentage > 120:
    print("⚠️  Warning: Paraphrased version is significantly longer than original")
else:
    print("✓ Length is approximately maintained")

print("\n" + "=" * 70)
print("PERFORMANCE METRICS")
print("=" * 70)
print(f"Inference Time:    {inference_time:.2f} seconds")
print(f"Tokens per Second: {paraphrased_word_count / inference_time:.2f}")
print("=" * 70)

# Save to JSON file
with open('paraphrased_output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\n✓ Output saved to 'paraphrased_output.json'")