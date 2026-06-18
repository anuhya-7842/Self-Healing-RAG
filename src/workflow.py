from critic import evaluate_answer
from query_rewriter import rewrite_query

# User query
query = "What is LangGraph?"

# First retrieval
context = "LangGraph is a framework for building stateful, multi-agent applications with LLMs."

# First answer (bad answer)
answer = "LangGraph was created by Google in 2025."

result = evaluate_answer(context, answer)

if result == "approved":
    print("Final Answer:", answer)
else:
    print("Answer rejected by critic.")

    new_query = rewrite_query(query)

    print("Retrying with query:", new_query)

    # Simulated second retrieval
    context = "LangGraph is a framework for building stateful, multi-agent applications with LLMs."

    # Simulated second answer
    answer = "LangGraph is a framework for building stateful, multi-agent applications with LLMs."

    result = evaluate_answer(context, answer)

    if result == "approved":
        print("Final Answer:", answer)
    else:
        print("I don't have enough information.")