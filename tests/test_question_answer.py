from assistant.python.knowledge_base import KnowledgeBase
from assistant.python.semantics import Triple

memory_path = "assistant/json/memory.json"
knowledge_base = KnowledgeBase(memory_path)


def test_answer_is_a():
    t = Triple(subject="dog", predicate="is_a", obj="lemon")
    assert knowledge_base.get_answer(t) == "I know some things about dog, but not that."

    t = Triple(subject="fadnfakn", predicate="is_a", obj="lemon")
    assert knowledge_base.get_answer(t) == "I don't know."

    t = Triple(subject="dog", predicate="is_a", obj="mammal")
    assert knowledge_base.get_answer(t) == "Yes."


def test_answer_has():
    t = Triple(subject="dog", predicate="has", obj="lemon")
    assert knowledge_base.get_answer(t) == "I know some things about dog, but not that."

    t = Triple(subject="fadnfakn", predicate="has", obj="lemon")
    assert knowledge_base.get_answer(t) == "I don't know."

    t = Triple(subject="dog", predicate="has", obj="fur")
    assert knowledge_base.get_answer(t) == "Yes."


def test_inverse_answer():
    t = Triple(subject=None, predicate="has", obj="two legs")
    assert knowledge_base.get_inverse_answer(t) == "A bird has two legs."


def test_duplicate():
    t = Triple(subject="dog", predicate="is_a", obj="mammal")
    assert knowledge_base.set_facts(t) == "I already know that fact"
