# AskMyNotes — Progress

Tracking doc for building the project described in [description.md](description.md).

**Status:** Milestone 1 complete — Gemini call works end to end. Next: Milestone 2 (load + chunk).
**Last updated:** 2026-11-12

---

## Environment (verified 2026-11-12)

| Item | Value |
|------|-------|
| Python | 3.14.7 (only version installed, no 3.12/3.13 fallback) |
| pip | 26.2.1 |
| uv | not installed |
| Platform | Windows 11 |

Dependency resolution was dry-run tested against Python 3.14 — the full stack installs
cleanly, so **no Python downgrade is needed**. Resolved versions:

| Package | Version |
|---------|---------|
| chromadb | 1.5.9 |
| google-genai | 3.2.0 |
| pypdf | 7.0.1 |
| streamlit | 1.67.0 |
| python-dotenv | 1.2.4 |

(107 packages total including transitive deps.)

---

## Build order

Terminal scripts first, Streamlit last. A UI added early hides where things break, and in
RAG most bugs live in the boring middle — chunking and metadata — not in the LLM call.

### Milestone 1 — Scaffold + prove the key works
- [x] Create venv (in `.venv/` — first attempt landed in the project root and was recreated)
- [x] `requirements.txt` (5 direct deps, exact pins)
- [x] `.gitignore` (covers `.env`, `chroma/`, `__pycache__/`, `.venv/`)
- [x] Install deps and verify all five import
- [x] `.env.example` committed; real `.env` never committed (verified: `.env` absent from all history)
- [x] Get a Gemini API key from Google AI Studio (free tier is plenty here)
- [x] ~10-line smoke test: send "hello" to Gemini, print the reply (`smoke-test.py`)
- [x] First git commit (`5bf0ccc`, pushed to `origin/main` on GitHub)

**Done when:** the smoke test prints a real model response.

### Milestone 2 — Load + chunk
- [ ] `ingest.py`: read a PDF with pypdf
- [ ] Split into chunks (~1000 chars, ~150 overlap)
- [ ] Attach page number to each chunk's metadata
- [ ] Print chunk count and chunk #0 to eyeball the result

**Zero AI involved in this step.** Don't rush it — chunk quality decides final answer
quality. Find a test PDF to use throughout (a lecture slide deck or article is ideal).

**Done when:** chunks look sane when printed and each carries a correct page number.

### Milestone 3 — Embed one chunk
- [ ] Call the embedding API on a single string
- [ ] Print `len(vector)`

Proves the API shape before looping over 400 chunks and burning quota on a typo.

**Done when:** a vector of the expected dimensionality comes back.

### Milestone 4 — Store + search
- [ ] Embed all chunks (`RETRIEVAL_DOCUMENT` task type)
- [ ] Write into a persistent Chroma collection
- [ ] Query with a question (`RETRIEVAL_QUERY` task type)
- [ ] Print top 3 matching chunks with distances

**The payoff moment** — semantic search working with no answer generation at all. Test it
by asking something worded completely differently from the source text and confirming it
still finds the right chunk.

**Done when:** a differently-worded question retrieves the correct chunk.

### Milestone 5 — Answer, then UI
- [ ] Prompt: retrieved chunks + question + grounding rules + cite sources
- [ ] Terminal Q&A loop
- [ ] Verify the refusal path: ask something genuinely absent from the notes and confirm it
      says "I couldn't find that in your notes" instead of inventing an answer
- [ ] Wrap the existing functions in `app.py` (Streamlit) — file upload + question box
- [ ] Show source citations in the UI

**Done when:** the app answers grounded questions with page citations and refuses
out-of-scope ones.

---

## Decisions made

**Do the embedding ourselves, not via Chroma.** Chroma will happily embed for us, but its
default is a small local ONNX model — the app would "work" while never touching Gemini
embeddings, skipping the exact thing this project is meant to teach. Call `google-genai`
directly and pass vectors into Chroma explicitly.

**Use asymmetric task types.** Gemini embeddings take a task type, and documents and
queries use *different* ones: `RETRIEVAL_DOCUMENT` when ingesting, `RETRIEVAL_QUERY` when
searching. Getting this wrong degrades retrieval silently — no error, just worse answers.
Probably the highest-value RAG detail in the whole project.

**Chunk by characters, not by pages.** ~1000 chars with ~150 overlap. Pages are far too
big and answers straddle page breaks — but page numbers still go in metadata, since that's
what turns citations from "chunk 47" into "p. 12", which is the feature the description
actually promises. Wrong chunk unit, right citation unit.

**Persist Chroma to disk from day one** (`PersistentClient` → `./chroma/`, gitignored).
Otherwise every run re-embeds everything, which is slow and eats the rate limit while
iterating on prompts.

**No LangChain / LlamaIndex.** They'd collapse this to ~20 lines and teach nothing — the
point is seeing the mechanism. The six-step pipeline in `description.md` is the right level
of abstraction.

**Flat file layout, no `src/` tree, no classes** — overhead at this size:

```
rag.py      plain functions: load_pdf, chunk, embed, search, answer
ingest.py   CLI entry for loading a document
app.py      thin Streamlit wrapper (milestone 5)
```

---

## Open questions

- [x] Chat model: `gemini-3.8-flash`, called via the Interactions API
      (`client.interactions.create(model=..., input=...)` → `.output_text`). Verified working
      in `smoke-test.py`.
- [ ] Embedding model: confirm the current name in the Gemini API docs before Milestone 3
      (look for `gemini-embedding-001`). Don't trust remembered model IDs; they go stale.
- [ ] Pick the test PDF for milestones 2–5.

---

## Deferred (post-MVP)

From `description.md`'s future features, plus notes from planning:

- Multiple documents at once (needs a doc id in metadata and a re-ingest skip check so
  existing documents aren't re-embedded on every run)
- Chat history and follow-up questions
- Image / handwritten-note support
- Auto-generated quizzes or flashcards
- Better chunking (semantic or heading-aware) once fixed-size chunking shows its limits
