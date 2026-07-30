import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def ask_llm(prompt):
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"]


def main():
    question = "Can an employee work from home 2 days a week?"

    context = """
## Weekly Work From Home

Eligible employees can work from home up to 2 days per week.
The specific days should be agreed upon with the employee's manager.
"""

    prompt = f"""
You are a company policy assistant.

Answer the question using ONLY the information provided in the context.

If the context does not contain enough information to answer the question,
say: "The information is not available in the knowledge base."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = ask_llm(prompt)

    print("Question:")
    print(question)

    print("\nLLM response:")
    print(answer)


if __name__ == "__main__":
    main()