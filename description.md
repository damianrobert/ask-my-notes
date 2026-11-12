# AskMyNotes 📚

**Chat with your own documents.** Upload your notes, PDFs, or study material and ask questions in plain language. AskMyNotes finds the relevant parts of your files and answers using only what's in them, showing you where each answer came from.

---

## Purpose

Notes pile up fast: lecture slides, PDFs, meeting notes, articles. When you need one specific detail, you end up scrolling through pages or searching for the exact keyword you hope you used.

AskMyNotes fixes that. Instead of searching by **words**, it searches by **meaning**, so you can ask a question the way you'd ask a friend who has read all your notes:

> "What were the three causes of the Industrial Revolution mentioned in lecture 4?"

and get a direct answer with a reference to the source.

The project also has a second purpose: it's a hands-on way to learn **AI engineering**, especially **RAG (Retrieval-Augmented Generation)**, one of the most widely used techniques in real-world AI apps.

---

## How It Works

Think of the app as a librarian for your notes.

1. **Load**: The app reads your uploaded PDF or text file.
2. **Chunk**: The text is split into small pieces, like index cards.
3. **Embed**: Each chunk is converted by Gemini into a list of numbers (an *embedding*) that represents its meaning. Chunks about similar topics end up close together, like books on the same shelf.
4. **Store**: The chunks and their embeddings are saved in a vector database (ChromaDB).
5. **Search**: When you ask a question, it's embedded the same way, and the app finds the chunks closest in meaning.
6. **Answer**: Those chunks and your question are sent to Gemini, which writes an answer based **only** on your notes and cites the sources it used.

```
Your PDF → Chunks → Embeddings → Vector DB
                                     ↓
Your question → Embedding → Find closest chunks → Gemini → Answer + sources
```

---

## Features

- 📄 Upload PDF and text files
- 💬 Ask questions in natural language
- 🎯 Answers grounded in your documents, not the AI's general knowledge
- 🔗 Source references for every answer
- 🚫 Says "I couldn't find that in your notes" instead of making things up

### Possible future features
- Support for multiple documents at once
- Chat history and follow-up questions
- Image and handwritten-note support
- Auto-generated quizzes or flashcards from your notes

---

## Tech Stack

| Part | Tool |
|------|------|
| Language | Python |
| AI model (chat + embeddings) | Google Gemini API (`google-genai`) |
| PDF reading | `pypdf` |
| Vector database | `chromadb` |
| User interface | `streamlit` |
| Secrets | `.env` file (`python-dotenv`) |

---

## What I'm Learning

- How to call an LLM API from code
- What embeddings are and how semantic search works
- How RAG reduces hallucinations by grounding answers in real data
- Prompt design for accurate, source-based answers
- Building and shipping a simple AI-powered web app

---

## Security Note

The Gemini API key is stored in a `.env` file and is **never** committed to version control. `.env` is listed in `.gitignore`.
