# Devpost submission text — HelpMap (WarriorHacks 2.0)

## The community issue we solve

Every community has resources — food banks, free clinics, shelters, ESL classes, legal
aid — but the people who need them most often can't find them. The information is
scattered across PDFs and websites, written in bureaucratic language, or locked behind
English. A stressed parent looking for free food tonight doesn't need a search engine —
they need a warm, direct answer: *where, when, what to bring.*

In our community, that gap is real: newcomers and students often don't know that no ID is
required, that walk-ins are welcome, or that interpretation is available. HelpMap closes
that gap with an AI that answers from the community's own resource guide — and refuses to
invent anything.

## What it does

**HelpMap** turns a community's resource guide into a navigator that speaks:

- **Quick help buttons** — 🍎 Food · 🏥 Health · 🏠 Shelter · 📚 ESL · ⚖️ Legal — one tap
  answers the most urgent needs.
- **Warm, practical answers** — every recommendation gives the organization, address,
  hours, languages, and *what to bring* (including "no ID required"), cited to the exact
  line of the guide.
- **🔊 Spoken answers** — neural TTS reads every answer aloud: accessible for low-vision
  and low-literacy users, and usable one-handed in a hurry.
- **Browse mode** — the whole guide organized by category, with an "Ask about this"
  button on every organization.
- **Honest refusals** — needs the guide doesn't cover get an explicit "I couldn't find
  this in the resource guide." No invented addresses or phone numbers, ever.
- **Emergency first** — danger or medical emergencies are routed to 911 before anything else.

## How we built it

- **Python + FastAPI** backend; single-page web UI (no build step).
- **Guide ingestion**: PDF / TXT / MD → source-linked passages; a browse endpoint parses
  the guide into categorized organizations.
- **Retrieval**: scikit-learn TF-IDF (local, any language) + optional LLM re-ranking.
- **Grounding contract**: retrieval-scoped prompts + mandatory citations + explicit
  refusal token; a strict prompt keeps the tone warm and practical.
- **Audio**: edge-tts neural voices with content-hash caching.
- **LLM**: any OpenAI-compatible endpoint.

## Challenges

- Making the AI *refuse* to fill gaps from general knowledge — an invented address is
  worse than no answer for someone in crisis.
- Designing for dignity: surfacing "no ID needed", "no registration", and languages
  spoken, because those are the questions people are afraid to ask.
- Keeping answers short and actionable rather than encyclopedic.

## What we learned

For community resources, the AI's most important features are *grounding* and *tone*:
cite the guide, never invent, and sound like a neighbor who knows the system — not a
bureaucrat. Any community can deploy this with their own guide.

## What's next

- Multi-language UI and answers (Spanish, Vietnamese, and beyond).
- SMS interface for users without smartphones or data plans.
- Community-contributed guide updates with moderation.

## Built with

python, fastapi, scikit-learn, edge-tts, llm, rag, community, accessibility
