# HelpMap — find help in your community, in plain language

> WarriorHacks 2.0 — Theme: solve an issue in your community

**A community resource navigator that answers "where can I get help today?" — with cited
addresses, hours, languages, and what to bring. It refuses to invent anything, and it
speaks the answer aloud.**

## The problem

Every community has resources — food banks, free clinics, shelters, ESL classes, legal aid —
but the people who need them most often can't find them: the information is scattered,
written in bureaucratic language, or locked in English. A stressed parent looking for free
food tonight doesn't need a search engine; they need a warm, direct answer: *where, when,
what to bring.*

## What HelpMap does

| Feature | Detail |
|---|---|
| **Guide ingestion** | Upload your community's resource guide (PDF / TXT / MD) — every organization keeps its exact source |
| **Quick help buttons** | 🍎 Food · 🏥 Health · 🏠 Shelter · 📚 ESL · ⚖️ Legal — one tap answers the most urgent needs |
| **Warm, practical answers** | Each recommendation gives the organization, address, hours, languages, and what to bring — cited to the guide `[unit_id]` |
| **🔊 Spoken answers** | Every answer is read aloud (neural TTS, cached) — accessible for low-vision users, low-literacy users, and anyone in a hurry |
| **Browse mode** | The whole guide, organized by category, with a "Ask about this" button on every organization |
| **Honest refusals** | Needs the guide doesn't cover get `NOT_COVERED` — no invented addresses or phone numbers, ever |
| **Emergency safety** | Emergency situations are routed to 911 first, before any other guidance |

## Safety design

- **No invented resources.** Answers come only from the uploaded guide; off-guide questions
  are declined. An invented address is worse than no answer.
- **Emergency first.** Danger or medical emergencies → call 911 (stated clearly, first).
- **Dignity by default.** The tone is warm and non-judgmental; the app notes when no ID,
  no registration, or no documents are required — the questions people are afraid to ask.
- **Synthetic demo data.** The bundled guide ("Springfield") is entirely fictional.

## How it works

```
 upload ──► ingest (pdf/txt/md) ──► guide knowledge base (source-linked passages)
                                        │
                       /api/browse ──► categorized resource list
                                        │
 question ──► TF-IDF retrieval ──► grounded answer + citations ──► 🔊 TTS
```

- Retrieval: scikit-learn TF-IDF (local, any language).
- Grounding: retrieval-scoped prompts + mandatory citations + explicit refusal token.
- Audio: edge-tts neural voices, content-hash cached.
- LLM: any OpenAI-compatible endpoint.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config.example.env .env      # set LLM_BASE_URL / LLM_API_KEY / LLM_MODEL
uvicorn server:app --port 7865  # open http://127.0.0.1:7865
```

Upload `data/sample_course/community_resources.md` and press 🍎 Food.

## Impact

- **Access**: the people who need help most get direct, actionable answers.
- **Language**: audio + simple language lower barriers for non-native speakers and
  low-literacy users.
- **Trust**: cited answers and honest refusals make the tool safe to rely on.
- **Reusability**: any community can deploy it with their own guide — the data is a file,
  the app is free.

## Honest limitations

- Not for emergencies (911 first) and not a substitute for social services.
- Scanned guides need OCR first.
- The demo guide is fictional; real deployments should keep guides up to date.
