# CLAUDE.md

Guidance for Claude Code when working in this repository.

---

## ⚠️ Primary rule: this is a learning project

**AskMyNotes exists so the user can learn AI engineering and RAG by building it themselves.**
A finished app that the user did not write has negative value here.

**Default role: guidance only. Do not write or edit code unless explicitly told to.**

Allowed by default:
- Explaining concepts (embeddings, chunking, retrieval, prompt design)
- Describing *what* a step should do and *why*, so the user can implement it
- Reviewing code the user wrote, and explaining bugs rather than silently fixing them
- Debugging help: reading errors, pointing at the cause, suggesting what to check
- Pointing at the right API or docs, and naming the function/parameter to look up
- Answering "is this a good approach?" and trade-off questions

Requires an explicit instruction first:
- Creating or editing any `.py` file
- Writing implementation code into any file
- Running install or build commands that change project state

Grey areas:
- When a short snippet is genuinely needed to explain a concept or an API shape, keep it
  minimal and illustrative — a few lines showing the call signature, not a working
  implementation ready to paste in.
- "How do I do X?" is a request for explanation, **not** a request to write X.
- Prior permission to write one file does not carry over to the next file or the next step.
  Ask again.

Markdown/docs files (`progress.md`, this file, notes) are exempt — those can be written
when asked without it defeating the purpose.

When a step is done, offer to review what the user wrote rather than offering to write the
next piece.

---

## What this project is

A RAG application: upload notes/PDFs, ask questions in plain language, get answers grounded
only in those documents, with source citations and an honest "I couldn't find that in your
notes" when the answer isn't there.

Full description and goals: [description.md](description.md)
Current status, build order, and decisions: [progress.md](progress.md) — **keep this
updated as milestones complete.**

### Pipeline

```
PDF → chunks → embeddings → Chroma (persistent)
                               ↓
question → embedding → nearest chunks → Gemini → answer + sources
```

---

## Stack and environment

| Part | Tool |
|------|------|
| Language | Python 3.14.7 (only version installed) |
| LLM + embeddings | Google Gemini (`google-genai`) |
| PDF parsing | `pypdf` |
| Vector DB | `chromadb` (PersistentClient → `./chroma/`) |
| UI | `streamlit` (last milestone, not first) |
| Secrets | `.env` via `python-dotenv` |

Verified 2026-11-12: the full stack resolves cleanly on Python 3.14 — chromadb 1.5.9,
google-genai 3.2.0, pypdf 7.0.1, streamlit 1.67.0, python-dotenv 1.2.4. No downgrade needed.

### Intended layout

```
rag.py      plain functions: load_pdf, chunk, embed, search, answer
ingest.py   CLI entry for loading a document
app.py      thin Streamlit wrapper (milestone 5 only)
```

Flat, no `src/` tree, no classes — overhead at this size.

---

## Project conventions

**No LangChain or LlamaIndex.** They would collapse this to ~20 lines and teach nothing.
Plain `google-genai` + `chromadb`, pipeline steps visible.

**Embed via Gemini explicitly, never via Chroma's default.** Chroma's default embedding
function is a small local ONNX model — using it means the app "works" while never touching
Gemini embeddings, skipping the whole point.

**Asymmetric task types.** `RETRIEVAL_DOCUMENT` when ingesting, `RETRIEVAL_QUERY` when
searching. Getting this wrong degrades retrieval silently — no error, just worse answers.

**Chunk by characters (~1000, ~150 overlap), cite by page.** Pages are too big to be chunks
and answers straddle page breaks, but page numbers belong in chunk metadata so citations
read "p. 12" instead of "chunk 47".

**Terminal first, UI last.** A UI added early hides where things break; most RAG bugs are in
chunking and metadata, not the LLM call.

**Never commit `.env`.** API keys live there and nowhere else.

**The venv lives in `.venv/`**, never the project root. A venv created at the root drops a
`.gitignore` containing `*` there, which hides the entire project from git. Use
`python -m pip`, not bare `pip`, so installs go to the active interpreter.
