from app.rag import KnowledgeBase


def test_retrieval_returns_relevant_source():
    kb = KnowledgeBase()
    kb.add_document("Calendar", "The odd semester begins in July. The even semester begins in January.")
    results = kb.retrieve("When does the odd semester begin?", 1)
    assert results
    assert results[0][0].title == "Calendar"


def test_empty_kb_returns_no_results():
    kb = KnowledgeBase()
    assert kb.retrieve("library hours") == []
