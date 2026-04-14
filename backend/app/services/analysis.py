from dataclasses import dataclass


@dataclass
class StructuredOutput:
    summary: str
    decisions: list[str]
    action_items: list[dict]
    topics: list[str]


def split_transcript_token_safe(text: str, chunk_size: int = 3000, overlap: int = 200) -> list[str]:
    if not text:
        return []
    words = text.split()
    chunks: list[str] = []
    step = max(chunk_size - overlap, 1)
    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if i + chunk_size >= len(words):
            break
    return chunks


def extract_chunk(chunk: str) -> StructuredOutput:
    # Placeholder extractor; wire this function to your LLM provider.
    summary = chunk[:400] + ("..." if len(chunk) > 400 else "")
    return StructuredOutput(
        summary=summary,
        decisions=[],
        action_items=[],
        topics=[],
    )


def merge_structured_outputs(partials: list[StructuredOutput]) -> StructuredOutput:
    summaries = [p.summary for p in partials if p.summary]
    decisions: list[str] = []
    action_items: list[dict] = []
    topics: list[str] = []

    for partial in partials:
        decisions.extend(partial.decisions)
        action_items.extend(partial.action_items)
        topics.extend(partial.topics)

    return StructuredOutput(
        summary=" ".join(summaries)[:1200],
        decisions=sorted(set(decisions)),
        action_items=action_items,
        topics=sorted(set(topics)),
    )
