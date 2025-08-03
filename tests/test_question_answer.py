from assistant.python.knowledge_base import KnowledgeBase
from assistant.python.semantics import Triple

memory_path = "assistant/json/memory.json"
knowledge_base = KnowledgeBase(memory_path)


def test_answer_is_a():
    t = Triple(subject="bleh bleh", predicate="is a", obj="bleh")
    assert knowledge_base.get_answer(t) == "PENDING_FACT"

    t = Triple(subject="dog", predicate="is a", obj="mammal")
    assert knowledge_base.get_answer(t) == "Yes."


def test_answer_has():
    t = Triple(subject="bleh bleh", predicate="has", obj="blah")
    assert knowledge_base.get_answer(t) == "PENDING_FACT"

    t = Triple(subject="dog", predicate="has", obj="fur")
    assert knowledge_base.get_answer(t) == "Yes."


def test_inverse_answer():
    t = Triple(subject=None, predicate="has", obj="two legs")
    assert knowledge_base.get_inverse_answer(t) == "bird"


def test_duplicate():
    t = Triple(subject="dog", predicate="is a", obj="mammal")
    assert knowledge_base.set_facts(t) == "I already know that fact"

def test_pending_fact():
    t = Triple(subject="blah", predicate="is a", obj="blah blah")
    assert knowledge_base.get_answer(t) == "PENDING_FACT"
    # fact should now be saved as pending
    assert knowledge_base.possible_fact("no") == "Okay, I won't remember it."