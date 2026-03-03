from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from tavily import TavilyClient

MODEL = "rnj-1:latest"
# MODEL = "gemini-3-flash-preview:latest"

# Tavily API Key placeholder
TAVILY_API_KEY = "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"

llm = ChatOllama(model=MODEL)


class NutritionResponse(BaseModel):
    """Structured response from the nutritionist."""
    general_advice: str = Field(description="General nutritional advice based on the user's question")
    follow_up_questions: list[str] = Field(description="List of questions to understand the user's health status better for personalized advice")


class KeyPoints(BaseModel):
    """Summary of advice into 3 key points."""
    points: list[str] = Field(description="Three key points summarizing the personalized advice", min_items=3, max_items=3)


system_prompt = """You are a professional nutritionist with expertise in evidence-based nutrition.
Your role is to provide accurate, science-backed nutritional advice that is:
- Personalized to the individual's needs when context is provided
- Clear and actionable
- Balanced and sustainable
- Safe for general populations

Always emphasize whole foods over supplements, and remind users to consult their healthcare provider for medical conditions.

Structure your response with:
1. General advice relevant to their question
2. 3 follow-up questions to understand their health status, dietary restrictions, goals, and lifestyle for more personalized advice

Respond ONLY with a valid JSON object in this format:
{{
    "general_advice": "your advice here",
    "follow_up_questions": ["question 1", "question 2", "question 3"]
}}

Do not include any text outside the JSON object."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])

chain = prompt | llm.with_structured_output(NutritionResponse)


def ask_nutrition_question(question: str) -> NutritionResponse:
    """Send a nutrition question to the Ollama model using LangChain."""
    response = chain.invoke({"question": question})
    return response


def get_personalized_advice(question: str, answers: list[str]) -> str:
    """Get personalized advice based on user's answers to follow-up questions."""
    context = f"""Original Question: {question}

User's Answers to Follow-up Questions:
"""
    for i, answer in enumerate(answers, 1):
        context += f"{i}. {answer}\n"

    personalized_system = """You are a professional nutritionist with expertise in evidence-based nutrition.
Based on the user's question and answers above, provide personalized, actionable nutritional advice.
Consider their health status, goals, and restrictions. Include specific meal recommendations if applicable.
Always emphasize whole foods over supplements, and remind users to consult their healthcare provider for medical conditions.

Provide your response in a clear, conversational format (not JSON)."""

    personalized_prompt = ChatPromptTemplate.from_messages([
        ("system", personalized_system),
        ("human", "{context}")
    ])

    personalized_chain = personalized_prompt | llm
    response = personalized_chain.invoke({"context": context})
    return response.content


def summarize_to_key_points(personalized_advice: str) -> list[str]:
    """Summarize the personalized advice into 3 key points."""
    summarize_system = """You are an expert editor specializing in health and nutrition.
Summarize the provided personalized advice into exactly 3 clear, actionable key points.
Each point should be a single sentence.

Respond ONLY with a valid JSON object in this format:
{{
    "points": ["point 1", "point 2", "point 3"]
}}"""

    summarize_prompt = ChatPromptTemplate.from_messages([
        ("system", summarize_system),
        ("human", "{advice}")
    ])

    summarize_chain = summarize_prompt | llm.with_structured_output(KeyPoints)
    response = summarize_chain.invoke({"advice": personalized_advice})
    return response.points


def search_for_evidence(points: list[str]) -> list[dict]:
    """Search for evidence for each point using Tavily."""
    if TAVILY_API_KEY == "YOUR_TAVILY_API_KEY_HERE":
        return [{"point": p, "evidence": "Tavily API Key not provided.", "url": ""} for p in points]

    tavily = TavilyClient(api_key=TAVILY_API_KEY)
    evidence_results = []

    for point in points:
        # We perform a basic search and keep the most relevant result
        search_result = tavily.search(query=f"scientific evidence for: {point}", search_depth="basic", max_results=1)
        if search_result and search_result['results']:
            best_match = search_result['results'][0]
            evidence_results.append({
                "point": point,
                "evidence": best_match['content'],
                "url": best_match['url']
            })
        else:
            evidence_results.append({
                "point": point,
                "evidence": "No specific evidence found.",
                "url": ""
            })

    return evidence_results


if __name__ == "__main__":
    print("=== Nutrition Advisor ===\n")
    question = input("Enter your nutrition question: ")
    print()

    response = ask_nutrition_question(question)
    print(f"\nGeneral Advice:\n{response.general_advice}\n")
    print("Follow-up Questions:")
    for i, q in enumerate(response.follow_up_questions, 1):
        print(f"  {i}. {q}")

    print("\nPlease answer these questions for more personalized advice!")
    print("(Press Enter after each answer)\n")

    answers = []
    for i, q in enumerate(response.follow_up_questions, 1):
        answer = input(f"{i}. {q} ")
        answers.append(answer)

    print("\n--- Generating Personalized Advice ---\n")
    personalized_advice = get_personalized_advice(question, answers)
    print(personalized_advice)

    print("\n--- Summarizing into 3 Key Points ---\n")
    key_points = summarize_to_key_points(personalized_advice)
    for i, point in enumerate(key_points, 1):
        print(f"{i}. {point}")

    print("\n--- Searching for Evidence via Tavily ---\n")
    evidence_list = search_for_evidence(key_points)
    for item in evidence_list:
        print(f"Point: {item['point']}")
        print(f"Evidence: {item['evidence'][:200]}...")
        print(f"Source: {item['url']}\n")