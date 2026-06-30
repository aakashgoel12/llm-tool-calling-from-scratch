# LinkedIn Posts

Pick whichever tone fits you. Three options below.

---

## Option A — The "I finally get it" story (recommended)

I finally understood how AI "uses tools" — so I built a tiny version from scratch. 🛠️

No frameworks. No API keys. No magic.
Just an open-source LLM running locally + 4 plain Python functions (calculator, database, weather, clock).

The realization that made it click:

👉 The LLM is a brain that decides — but it has NO hands.
It only outputs *"call this tool with these inputs."* Your code does the actual work.

So when I ask "what's 45 ÷ 5?", the model doesn't calculate anything. It just replies:
{"tool": "calculator", "params": {"operation": "divide", "a": 45, "b": 5}}

…and my code runs it. That's the entire "magic" behind ChatGPT plugins, Copilot, and AI agents.

The best part was the bug:
My small model kept FORGETTING to use its own clock tool for "what time is it?" 😅
Fix? A few lines of fallback logic as a guardrail.

That tiny fix is the real lesson: production AI isn't "trust the model" — it's "model + guardrails."

Full step-by-step write-up (with code) in the comments 👇

#AI #LLM #Python #MachineLearning #BuildInPublic #AIAgents

---

## Option B — Short and punchy

How does AI actually "use tools"? I built it from scratch to find out.

The whole secret in one line:
🧠 The LLM decides which tool to use. 🤖 Your code actually runs it.

That's it. That's tool calling.

I used a free, local open-source model + 4 tiny Python functions. ~150 lines total.

Biggest lesson: small models forget to use tools, so you add guardrails — exactly what real agents do.

Full walkthrough + code in comments 👇

#AI #LLM #Python #AIAgents #BuildInPublic

---

## Option C — Teaching hook for your network

"The AI called a tool." I said it for months before I actually understood it.

So I built the smallest possible real version:
• A free LLM running on my laptop (no API keys)
• 4 plain Python functions as "tools"
• ~150 lines of glue code

What I learned:
1️⃣ The model never runs anything — it just says WHICH tool + WHICH inputs.
2️⃣ Your code does the work and hands the result back.
3️⃣ Small models need guardrails (mine kept ignoring its own clock tool 😅).

Everything LangChain or the OpenAI tools API does is a fancier version of these same 4 steps:
describe tools → model picks one → you run it → model explains it.

Wrote the whole thing up as a beginner-friendly article. Link in comments 👇

#AI #LLM #Python #MachineLearning #AIAgents

---

## Tip for posting
- Put the article link in the FIRST COMMENT (not the post body) — LinkedIn favors posts that keep people on-platform.
- Add 1 screenshot of the live terminal output (the [1]…[5] trace). Visual proof = more engagement.
