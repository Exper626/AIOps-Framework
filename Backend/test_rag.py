from rag.pipeline import run_rag


if __name__ == "__main__":
    question = input("Question: ").strip()
    model = input("Vercel AI Gateway model ID: ").strip()

    print()
    print(run_rag(question, model))
