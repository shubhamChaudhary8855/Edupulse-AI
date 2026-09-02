import os


def generate_answer(question: str, results: list[dict]) -> str:
    if not results:
        return "I could not find this information in the university knowledge base."

    context = "\n\n".join(
        f"[Source: {item['title']}]\n{item['text']}" for item in results
    )
    if not os.getenv("OPENAI_API_KEY"):
        return results[0]["text"]

    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        input=(
            "Answer the student's question using only the supplied university context. "
            "If the context does not contain the answer, say so. Keep the answer concise.\n\n"
            f"Question: {question}\n\nContext:\n{context}"
        ),
    )
    return response.output_text
