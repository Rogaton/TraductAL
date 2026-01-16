#!/usr/bin/env python3
"""
Smart Text Chunker for Long Document Translation
Handles texts of any length by intelligently splitting at natural boundaries
"""

import re
from typing import List, Tuple


class SmartTextChunker:
    """
    Intelligently chunks long texts for translation while preserving:
    - Paragraph boundaries
    - Sentence boundaries
    - Context and coherence
    """

    def __init__(self, max_tokens=400, tokenizer=None):
        """
        Initialize the text chunker.

        Args:
            max_tokens: Target maximum tokens per chunk (default 400, safe margin from 512)
            tokenizer: Optional tokenizer for accurate token counting
        """
        self.max_tokens = max_tokens
        self.tokenizer = tokenizer

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        If tokenizer available, use it. Otherwise estimate:
        - 1 token ≈ 0.75 words for European languages
        - 1 token ≈ 4 characters
        """
        if self.tokenizer:
            try:
                tokens = self.tokenizer(text, return_tensors="pt", add_special_tokens=False)
                return len(tokens['input_ids'][0])
            except:
                pass

        # Fallback: estimate based on words
        word_count = len(text.split())
        # Conservative estimate: 1.3 tokens per word (safer than 0.75 words per token)
        return int(word_count * 1.3)

    def split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        # Split on double newlines or more
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]

    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Enhanced sentence splitting pattern
        # Handles: . ! ? followed by space and capital letter, or end of string
        pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])$'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]

    def split_by_tokens(self, text: str, max_tokens: int) -> List[str]:
        """
        Split text into chunks of approximately max_tokens.
        Tries to split at sentence boundaries if possible.
        """
        sentences = self.split_sentences(text)
        chunks = []
        current_chunk = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = self.estimate_tokens(sentence)

            # If single sentence is too long, split it further
            if sentence_tokens > max_tokens:
                # Save current chunk if any
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_tokens = 0

                # Split long sentence by words
                words = sentence.split()
                temp_chunk = []
                temp_tokens = 0

                for word in words:
                    word_tokens = self.estimate_tokens(word)
                    if temp_tokens + word_tokens > max_tokens and temp_chunk:
                        chunks.append(' '.join(temp_chunk))
                        temp_chunk = [word]
                        temp_tokens = word_tokens
                    else:
                        temp_chunk.append(word)
                        temp_tokens += word_tokens

                if temp_chunk:
                    chunks.append(' '.join(temp_chunk))

            # If adding this sentence would exceed limit, start new chunk
            elif current_tokens + sentence_tokens > max_tokens and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_tokens = sentence_tokens

            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens

        # Add remaining chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def chunk_text(self, text: str) -> List[Tuple[str, str]]:
        """
        Main method: Intelligently chunk text of any length.

        Strategy:
        1. Check if text fits in one chunk → return as-is
        2. Try splitting by paragraphs
        3. If paragraphs too long, split by sentences
        4. If sentences too long, split by words

        Returns:
            List of (chunk_text, chunk_type) tuples
            chunk_type: 'full', 'paragraph', 'sentence', 'word-split'
        """
        text = text.strip()
        if not text:
            return []

        # Check if entire text fits
        total_tokens = self.estimate_tokens(text)
        if total_tokens <= self.max_tokens:
            return [(text, 'full')]

        # Split into paragraphs first
        paragraphs = self.split_paragraphs(text)

        chunks = []
        for para in paragraphs:
            para_tokens = self.estimate_tokens(para)

            # If paragraph fits, keep it whole
            if para_tokens <= self.max_tokens:
                chunks.append((para, 'paragraph'))

            # Otherwise, split paragraph into smaller chunks
            else:
                para_chunks = self.split_by_tokens(para, self.max_tokens)
                for chunk in para_chunks:
                    chunk_tokens = self.estimate_tokens(chunk)
                    if chunk_tokens <= self.max_tokens:
                        chunks.append((chunk, 'sentence'))
                    else:
                        # Very long sentence, had to split by words
                        chunks.append((chunk, 'word-split'))

        return chunks

    def get_stats(self, text: str) -> dict:
        """Get statistics about text chunking."""
        chunks = self.chunk_text(text)

        return {
            'total_chars': len(text),
            'estimated_tokens': self.estimate_tokens(text),
            'num_chunks': len(chunks),
            'chunk_types': {
                'full': sum(1 for _, t in chunks if t == 'full'),
                'paragraph': sum(1 for _, t in chunks if t == 'paragraph'),
                'sentence': sum(1 for _, t in chunks if t == 'sentence'),
                'word-split': sum(1 for _, t in chunks if t == 'word-split')
            },
            'chunks': [
                {
                    'text_preview': chunk[:100] + '...' if len(chunk) > 100 else chunk,
                    'type': chunk_type,
                    'chars': len(chunk),
                    'estimated_tokens': self.estimate_tokens(chunk)
                }
                for chunk, chunk_type in chunks
            ]
        }


def demo():
    """Demo the text chunker."""
    chunker = SmartTextChunker(max_tokens=100)

    test_texts = [
        # Short text
        "Hello, how are you?",

        # Multi-paragraph
        """This is the first paragraph. It contains multiple sentences. Each sentence adds information.

        This is the second paragraph. It also has several sentences. They flow naturally together.

        And here is a third paragraph to test the chunking.""",

        # Very long text
        " ".join(["This is sentence number {}.".format(i) for i in range(1, 51)])
    ]

    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}")
        print(f"{'='*70}")
        print(f"Input length: {len(text)} chars")

        chunks = chunker.chunk_text(text)
        stats = chunker.get_stats(text)

        print(f"\nChunks: {stats['num_chunks']}")
        print(f"Estimated tokens: {stats['estimated_tokens']}")
        print(f"\nChunk breakdown:")
        for j, (chunk, chunk_type) in enumerate(chunks, 1):
            print(f"  [{j}] {chunk_type}: {len(chunk)} chars, ~{chunker.estimate_tokens(chunk)} tokens")
            preview = chunk[:80] + '...' if len(chunk) > 80 else chunk
            print(f"      \"{preview}\"")


if __name__ == "__main__":
    demo()
