def evaluate_answer(context, answer):
    if answer.lower() in context.lower():
        return "approved"
    else:
        return "rejected"


if __name__ == "__main__":
    context = "LangGraph is a framework for building stateful, multi-agent applications with LLMs."

    answer = "LangGraph was created by Google in 2025."

    result = evaluate_answer(context, answer)

    print("Critic Result:", result)