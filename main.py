"""
main.py - Tool calling orchestrator

How it works:
1. User gives a prompt
2. LLM decides which tool(s) to call and with what params
3. We execute the tool and show the result
4. LLM processes the result to give final answer
"""

import json
import re
import requests
import os
import argparse
from tools import TOOLS, execute_tool


# LLM Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def call_llm(prompt: str, max_tokens: int = 500) -> str:
    """Call the LLM and get response."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3,
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to Ollama. Is it running? (docker compose up -d ollama)"
    except Exception as e:
        return f"ERROR: {str(e)}"


def build_tool_prompt(user_query: str) -> str:
    """Build a prompt for the LLM to decide which tool to call."""
    
    # Build tool descriptions
    tool_descriptions = "\n".join([
        f"- {tool['name']}: {tool['description']}"
        for tool in TOOLS.values()
    ])
    
    prompt = f"""You are a helpful assistant with access to these tools:

{tool_descriptions}

USER QUERY: {user_query}

Critical routing rules:
- If query asks for math/calculation, use calculator.
- If query mentions a user id like user_001, use database_query.
- If query asks weather for a city, use weather_lookup.
- If query asks current time/date/day, use get_current_time.
- Do not answer from memory when a tool can provide the data.

Respond with ONLY a JSON object in this format:
{{"tool": "tool_name", "params": {{"param1": value1, "param2": value2}}}}

Or if the query doesn't need a tool:
{{"tool": null, "answer": "Your direct answer here"}}

Examples:
- Query: "What is 15 times 8?"
  Response: {{"tool": "calculator", "params": {{"operation": "multiply", "a": 15, "b": 8}}}}

- Query: "Tell me about user_002"
  Response: {{"tool": "database_query", "params": {{"user_id": "user_002"}}}}

- Query: "What's the weather in Paris?"
  Response: {{"tool": "weather_lookup", "params": {{"city": "Paris"}}}}

- Query: "What is 2 plus 2?"
  Response: {{"tool": "calculator", "params": {{"operation": "add", "a": 2, "b": 2}}}}

- Query: "What time is it right now?"
    Response: {{"tool": "get_current_time", "params": {{}}}}

Now respond for this query:"""
    
    return prompt


def fallback_tool_decision(user_query: str) -> dict:
    """Deterministic fallback router when model output is empty/invalid."""
    q = user_query.lower()

    # User lookup intent
    user_match = re.search(r"\buser_\d{3}\b", q)
    if user_match:
        return {"tool": "database_query", "params": {"user_id": user_match.group(0)}}

    # Time/date intent
    if any(token in q for token in ["time", "date", "day", "right now", "current time"]):
        return {"tool": "get_current_time", "params": {}}

    # Weather intent
    weather_match = re.search(r"weather in ([a-zA-Z\s]+)\??", q)
    if "weather" in q and weather_match:
        city = weather_match.group(1).strip().title()
        return {"tool": "weather_lookup", "params": {"city": city}}

    # Very small math intent fallback (supports: add x and y, x divided by y)
    nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", q)]
    if len(nums) >= 2:
        a, b = nums[0], nums[1]
        if any(token in q for token in ["add", "plus", "+"]):
            return {"tool": "calculator", "params": {"operation": "add", "a": a, "b": b}}
        if any(token in q for token in ["subtract", "minus", "-"]):
            return {"tool": "calculator", "params": {"operation": "subtract", "a": a, "b": b}}
        if any(token in q for token in ["multiply", "times", "*"]):
            return {"tool": "calculator", "params": {"operation": "multiply", "a": a, "b": b}}
        if any(token in q for token in ["divide", "divided by", "/"]):
            return {"tool": "calculator", "params": {"operation": "divide", "a": a, "b": b}}

    return {"tool": None, "answer": ""}


def parse_tool_call(llm_response: str) -> dict:
    """Extract tool call from LLM response."""
    
    # Try to find JSON in the response
    json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
    
    if not json_match:
        return {"tool": None, "answer": llm_response}
    
    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError:
        return {"tool": None, "answer": llm_response}


def process_query(user_query: str) -> dict:
    """
    Process a user query:
    1. Ask LLM which tool to use
    2. Execute the tool
    3. Return result
    """
    
    print(f"\n{'='*70}")
    print(f"USER QUERY: {user_query}")
    print(f"{'='*70}\n")
    
    # Step 1: Ask LLM which tool to call
    print("[1] Sending to LLM: 'Which tool should I use?'")
    tool_prompt = build_tool_prompt(user_query)
    llm_response = call_llm(tool_prompt)
    print(f"[2] LLM Response:\n{llm_response}\n")
    
    # Step 2: Parse the tool decision
    tool_decision = parse_tool_call(llm_response)
    if not tool_decision.get("tool"):
        fallback = fallback_tool_decision(user_query)
        if fallback.get("tool"):
            tool_decision = fallback
            print("[3] Fallback Router Applied: chose tool deterministically\n")
    print(f"[3] Parsed Decision: {json.dumps(tool_decision, indent=2)}\n")
    
    # Step 3: Execute tool if needed
    if tool_decision.get("tool"):
        tool_name = tool_decision["tool"]
        params = tool_decision.get("params", {})
        
        if tool_name not in TOOLS:
            result = {"error": f"Unknown tool: {tool_name}"}
        else:
            print(f"[4] Executing Tool: {tool_name}")
            print(f"    Parameters: {json.dumps(params, indent=6)}")
            result = execute_tool(tool_name, **params)
            print(f"    Result: {json.dumps(result, indent=6)}\n")
    else:
        result = None
        print(f"[4] No tool needed - Direct answer\n")
    
    # Step 4: Get final answer from LLM
    if result:
        final_prompt = f"""Given the tool result, answer this user query clearly and briefly:

User Query: {user_query}
Tool Used: {tool_decision['tool']}
Tool Result: {json.dumps(result, indent=2)}

Rules:
- Keep the answer under 3 sentences.
- Do not add storytelling or extra examples.
- If result contains an error, explain it plainly.

Please provide the final answer based on this data."""
        
        print(f"[5] Asking LLM to format the answer...")
        final_answer = call_llm(final_prompt)
        print(f"    Final Answer: {final_answer}\n")
        
        return {
            "query": user_query,
            "tool": tool_decision.get("tool"),
            "tool_result": result,
            "final_answer": final_answer
        }
    else:
        answer = tool_decision.get("answer", "No response")
        print(f"[5] Direct Answer: {answer}\n")
        
        return {
            "query": user_query,
            "tool": None,
            "tool_result": None,
            "final_answer": answer
        }


def run_demo() -> None:
    """Run the fixed prompt demo sequence."""
    test_queries = [
        "What is 45 divided by 5?",
        "Tell me about user_001",
        "What's the weather in Tokyo?",
        "What time is it right now?",
        "Add 100 and 250 for me",
    ]

    print("\n" + "=" * 70)
    print("TOOL CALLING DEMO - LLM Deciding Which Tool to Use")
    print("=" * 70)

    results = []
    for query in test_queries:
        result = process_query(query)
        results.append(result)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Query: {result['query']}")
        print(f"   Tool Used: {result['tool'] or 'None (Direct answer)'}")
        if result["tool"]:
            print(f"   Tool Result: {json.dumps(result['tool_result'], indent=6)}")
        print(f"   Final Answer: {result['final_answer'][:100]}...")


def run_interactive() -> None:
    """Run an interactive chat loop for live tool-calling demos."""
    print("\n" + "=" * 70)
    print("INTERACTIVE TOOL CALLING CHAT")
    print("=" * 70)
    print("Type a prompt and press Enter.")
    print("Commands: /exit, /quit, /help, /examples")

    while True:
        user_query = input("\nYou> ").strip()

        if not user_query:
            continue

        cmd = user_query.lower()
        if cmd in {"/exit", "/quit"}:
            print("\nExiting interactive chat.")
            break

        if cmd == "/help":
            print("\nTry prompts like:")
            print("- What is 81 divided by 9?")
            print("- Tell me about user_002")
            print("- What's the weather in London?")
            print("- What time is it right now?")
            continue

        if cmd == "/examples":
            print("\nExamples:")
            print("1) Add 14 and 28")
            print("2) Tell me about user_003")
            print("3) What's the weather in Tokyo?")
            print("4) What day is it?")
            continue

        result = process_query(user_query)
        print("Assistant>", result["final_answer"])


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM tool-calling demo")
    parser.add_argument(
        "--mode",
        choices=["interactive", "demo"],
        default="interactive",
        help="Run interactive chat or fixed demo prompts (default: interactive)",
    )
    args = parser.parse_args()

    if args.mode == "demo":
        run_demo()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
