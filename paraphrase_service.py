from llama_cpp import Llama
import time
import os
from typing import Dict, Optional


class ParaphraseService:
    """Service for paraphrasing articles using LLM"""
    
    def __init__(self, model_path: str, n_ctx: int = 4096, n_threads: Optional[int] = None, n_batch: int = 512):
        """
        Initialize the paraphrase service with LLM model
        
        Args:
            model_path: Path to the GGUF model file
            n_ctx: Context window size
            n_threads: Number of threads (None for auto-detect)
            n_batch: Batch size for processing
        """
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads or os.cpu_count() or 8,
            n_batch=n_batch,
            verbose=False
        )
    
    def paraphrase_article(self, original_article: str, max_tokens: int = 3500) -> Dict:
        """
        Paraphrase an article while maintaining length and all details
        
        Args:
            original_article: The original article text to paraphrase
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary containing paraphrased article and statistics
        """
        # Count original words and paragraphs
        original_word_count = len(original_article.split())
        original_paragraphs = len([p for p in original_article.split('\n\n') if p.strip()])
        
        # Create prompt that emphasizes maintaining length and detail
        prompt = f"""Paraphrase this article paragraph by paragraph. Use different words but keep the SAME LENGTH and ALL details. Do not summarize or shorten anything.

Original Article ({original_word_count} words):
{original_article}

Paraphrased Version (must be approximately {original_word_count} words):"""
        
        # Measure inference time
        start_time = time.time()
        
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
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
        length_match_percentage = (paraphrased_word_count / original_word_count) * 100 if original_word_count > 0 else 0
        
        # Create structured output
        result = {
            "original_article": original_article,
            "paraphrased_article": paraphrased_text,
            "statistics": {
                "original_word_count": original_word_count,
                "original_paragraph_count": original_paragraphs,
                "paraphrased_word_count": paraphrased_word_count,
                "length_match_percentage": round(length_match_percentage, 2),
                "inference_time_seconds": round(inference_time, 2),
                "tokens_per_second": round(paraphrased_word_count / inference_time, 2) if inference_time > 0 else 0
            }
        }
        
        return result

