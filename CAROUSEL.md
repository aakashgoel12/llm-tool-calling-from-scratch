# LinkedIn Carousel Outline

A slide-by-slide outline for a LinkedIn carousel (PDF/image deck).
Keep each slide to one idea, large text, minimal words. 9 slides.

Design tips:
- Square (1080x1080) or portrait (1080x1350)
- Big bold headline + 1-2 supporting lines per slide
- Consistent colors; use a monospace font for code
- Slide numbers in a corner ("1/9")

---

## Slide 1 — Hook (cover)

**Title:** How does AI actually "use tools"?

**Subtitle:** I built it from scratch to find out.
~150 lines. Free local model. No magic.

**Visual:** A brain icon + a wrench icon, connected by an arrow.

---

## Slide 2 — The confusion

**Headline:** "The AI called a tool."

**Body:**
I said this for months before I actually understood it.
ChatGPT browses. Copilot runs code. Agents book flights.
But *how* does it decide what to use?

---

## Slide 3 — The one idea (the key slide)

**Headline:** The LLM is a brain. It has NO hands.

**Body:**
🧠 The model only *decides*: "use this tool, with these inputs."
🤖 Your code is the hands — it actually runs the tool.

**Visual:** Brain (decides) ➜ Code (executes)

---

## Slide 4 — What a "tool call" really is

**Headline:** A tool call is just... text.

**Body (code block):**
```
You: "What is 45 divided by 5?"

Model replies:
{"tool": "calculator",
 "params": {"a": 45, "b": 5, "operation": "divide"}}
```
The model didn't calculate. It just *suggested*. Your code runs it.

---

## Slide 5 — The 4-step loop

**Headline:** The entire flow is 4 moves

**Body:**
1️⃣ Show the model the tool menu + question
2️⃣ Model returns JSON: which tool + inputs
3️⃣ Your code runs the tool
4️⃣ Model turns the result into a sentence

That's it. That's tool calling.

---

## Slide 6 — The setup (no excuses)

**Headline:** Free. Local. No API keys.

**Body (code block):**
```
docker compose up -d ollama
docker compose run --rm ollama-init
python main.py
```
An open-source model (`llama3.2:3b`) running on a laptop.

---

## Slide 7 — The bug that taught me the most

**Headline:** My model FORGOT to use its own clock 😅

**Body:**
Asked "what time is it?" → it answered from memory and failed.
Small models do this a lot.

Fix: a few lines of fallback logic as a guardrail.

---

## Slide 8 — The real lesson

**Headline:** Real AI = model + guardrails

**Body:**
Production agents don't "trust the model blindly."
They add safety nets for when it slips.
My 10-line fallback is a tiny version of exactly that.

---

## Slide 9 — CTA

**Headline:** Want the full walkthrough?

**Body:**
I wrote a beginner-friendly, step-by-step article with all the code.
👉 Link in the comments.

Follow for more "build it to understand it" breakdowns.

**Visual:** Your name/handle + a small repo screenshot.

---

## Caption to post with the carousel

How does AI actually "use tools"? I built the smallest possible real version to find out 👇

The whole secret: 🧠 the LLM decides which tool to use, 🤖 your code runs it.

Free local model + 4 Python functions + ~150 lines. Swipe through ➡️

Full article + code in the comments.

#AI #LLM #Python #AIAgents #BuildInPublic #MachineLearning

---

## Alt-text for each slide (accessibility)

Add these as the image description for each slide when uploading.

1. Cover slide titled "How does AI actually use tools?" with a brain icon and a wrench icon connected by an arrow.
2. Slide showing the phrase "The AI called a tool" with text explaining the author didn't understand it for months.
3. Slide stating "The LLM is a brain. It has no hands." with a diagram: brain (decides) pointing to code (executes).
4. Slide showing a code block where a user asks "What is 45 divided by 5?" and the model replies with JSON specifying the calculator tool and its inputs.
5. Slide listing the four steps of tool calling: show tools, model returns JSON, code runs the tool, model explains the result.
6. Slide showing three terminal commands to start a local Ollama model and run the Python script, captioned "Free. Local. No API keys."
7. Slide titled "My model forgot to use its own clock" describing how a small model answered from memory and failed, fixed by fallback logic.
8. Slide stating "Real AI = model + guardrails" explaining production agents add safety nets for when the model slips.
9. Closing call-to-action slide inviting readers to see the full walkthrough, with a link-in-comments prompt and the author's handle.

---

## Screenshot suggestion (from `python main.py --mode demo`)

The best single screenshot for slide 7 (the "bug") is query 2, where the model
returns `{"tool": null}` and the fallback router rescues it:

```
USER QUERY: Tell me about user_001
[2] LLM Response: {"tool": null, "answer": "I don't have information about user_001"}
[3] Fallback Router Applied: chose tool deterministically
[4] Executing Tool: database_query  ->  {"found": true, "name": "Alice Johnson", ...}
```

This visually proves both the failure AND the guardrail in one frame.
