# Setup: Local LLM with Ollama

This project defaults to a lightweight local model, not a heavy one.

Default model in code: `llama3.2:3b`.
This is a good balance of quality and speed for laptop-level CPUs.

## Fast Path (recommended)

1. Install Ollama from https://ollama.ai
2. Pull model:
   ```bash
   ollama pull llama3.2:3b
   ```
3. Verify:
   ```bash
   ollama list
   ```
4. Run project:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

Optional API check (PowerShell-safe):
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -ContentType "application/json" -Body (@{ model = "llama3.2:3b"; prompt = "Hello"; stream = $false } | ConvertTo-Json -Compress)
```

Alternative with `curl.exe`:
```powershell
curl.exe -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d "{\"model\":\"llama3.2:3b\",\"prompt\":\"Hello\",\"stream\":false}"
```

If you see JSON output, you're ready.

## Model choice for learning

- `llama3.2:3b` - lightweight default, solid quality/speed for local runs
- `qwen2.5:3b` - lightweight, often strong for coding-style prompts
- `mistral` (7B) - stronger but heavier than 3B options

For reproducible learning on most local machines, `llama3.2:3b` is recommended.

## Reproducible setup with Docker Compose

This gives readers a consistent environment without manual Ollama setup.

1. Start Ollama container:
   ```bash
   docker compose up -d ollama
   ```
2. Pull default model inside container:
   ```bash
   docker compose run --rm ollama-init
   ```
3. Optional: use custom model by creating `.env` from `.env.example` and changing `OLLAMA_MODEL`.
4. Verify model is present (works everywhere):
   ```bash
   docker compose exec ollama ollama list
   ```
5. Verify generate endpoint:

   Linux/macOS (`curl`):
   ```bash
   curl -s http://localhost:11434/api/generate \
     -H "Content-Type: application/json" \
     -d '{"model":"llama3.2:3b","prompt":"hello","stream":false}'
   ```

   Windows PowerShell:
   ```powershell
   Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -ContentType "application/json" -Body (@{ model = "llama3.2:3b"; prompt = "hello"; stream = $false } | ConvertTo-Json -Compress)
   ```

Then run the demo as usual:
```bash
python main.py
```

To stop:
```bash
docker compose down
```

---

If Ollama is not available, all scripts will gracefully fail with a helpful message.
