# Living Model

**Living Model** is an experimental cognitive-agent scaffold designed to explore
**continual learning, long-term memory, and wake/sleep consolidation** in language-model-based systems.

Instead of treating an LLM as a static chatbot, this project treats it as a
**living system** that:
- interacts with users,
- forms episodic memories,
- consolidates experiences during a “sleep” phase,
- and gradually changes its behavior over time.

This project focuses on **architecture and learning loops**, not just prompt engineering.

---

## Core Ideas

Inspired by human cognition, the system separates memory into layers:

- **Working Memory**  
  Short-term context used during active interaction.

- **Episodic Memory**  
  Raw experiences and interactions, stored with salience scores.

- **Semantic Memory**  
  Compressed, abstracted knowledge derived from episodic memory.

- **Sleep Phase**  
  An offline consolidation step where important experiences are abstracted
  and (eventually) used to update the model itself.

The long-term goal is to support **lifelong learning** with:
- bounded active computation,
- unbounded lifetime memory,
- and stable recall speed as memory grows.

---

## Project Status

🚧 **Early scaffold / research prototype**

Current features:
- Wake / sleep execution loop
- Working memory buffer
- Episodic memory with salience scoring
- Semantic consolidation placeholder
- Persistent storage (JSON-based for now)

Planned features:
- Local LLM integration (LLaMA / RWKV / Mamba)
- Semantic memory recall during inference
- Sleep-time synthetic data generation
- LoRA-based weight updates
- Forgetting and stability mechanisms
- Dockerized training / sleep runs

---

## Repository Structure

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai) installed and running locally
- Internet connection (for web search features)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd living-model
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama** (in a separate terminal):
   ```bash
   ollama serve
   ```

5. **Pull a model** (if you don't have one already):
   ```bash
   ollama pull llama3.2
   ```
   Available models: `llama3.2`, `llama3-chatqa`, `mannix/llama3.1-8b-lexi`, etc.

---

## Usage

### Run the Agent

Start an interactive conversation with the agent:

```bash
python -m scripts.run
```

The agent will:
- Load previous memories (if they exist)
- Enter an interactive chat loop
- Remember facts and preferences you tell it
- Search the internet for current information when needed

**Example conversation:**
```
> My favorite color is blue
I've noted that your favorite color is blue!

> What do you remember about me?
You've told me that your favorite color is blue.

> Tell me about current AI news
[Searches the internet and provides latest AI news]

> sleep
[Consolidates important facts into long-term memory and exits]
```

### Sleep & Consolidation

When you type `sleep`, the agent:
1. Samples high-salience events from episodic memory
2. Consolidates them into semantic abstractions
3. Removes outdated facts and keeps the latest versions
4. Saves everything to persistent storage
5. Exits the session

Type `sleep` to trigger consolidation and exit.

### Key Commands

- **Type normally**: Chat with the agent
- **Type `sleep`**: Trigger consolidation and save memories
- **Ctrl+C**: Force exit (memories are auto-saved)

---

## Features

### ✅ Implemented Features

- **Local LLM Integration**: Uses Ollama for all inference (private, no cloud)
- **Persistent Memory**: Saves episodic and semantic memories to `storage/agent_state.json`
- **Semantic Search**: Uses embedding-based retrieval (nomic-embed-text model)
- **Internet Search**: Free DuckDuckGo API for current information
- **Memory Consolidation**: Automatic abstraction of important events
- **Salience Scoring**: Intelligent detection of memorable moments
- **Working Memory Buffer**: Recent conversation context (8 turns)
- **Category-based Memory**: Tracks identity, preferences, behavior, facts

### 📋 Example Interactions

**Memory Test:**
```
> My name is Alice and I love coding
> sleep
[Consolidates memory]

> (New session) What's my name?
Your name is Alice. You also love coding!
```

**Internet Search:**
```
> What's the latest in AI?
[Searches DuckDuckGo and provides current news]
```

**Preference Tracking:**
```
> I prefer coffee to tea
> sleep

> (New session) Do I like coffee?
Yes, you prefer coffee to tea.

> Actually, I prefer tea now
> sleep

> (New session) Do I like tea?
Yes, you prefer tea (updated preference).
```

---

## Project Structure

```
living-model/
├── core/
│   ├── agent.py          # Main agent with LLM integration
│   ├── model.py          # (Empty, for future model implementations)
│   ├── search.py         # Internet search functionality
│   └── state.py          # Working memory buffer
├── memory/
│   ├── episodic.py       # Raw event storage
│   ├── semantic.py       # Long-term abstracted knowledge
│   ├── salience.py       # Importance scoring
│   └── consolidation.py  # Sleep consolidation logic
├── scripts/
│   ├── run.py            # Main interactive agent (with inline consolidation)
│   └── sleep.py          # Standalone consolidation script
├── storage/
│   ├── db.py             # Storage utilities
│   └── agent_state.json  # Persistent memory file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## Configuration

### Model Selection

Edit `scripts/run.py` to change the model:

```python
agent = LivingAgent(model="llama3-chatqa")  # Change to any Ollama model
```

Available models:
- `llama3.2` (2GB, fast, good for quick responses)
- `llama3-chatqa` (4.7GB, optimized for Q&A)
- `mannix/llama3.1-8b-lexi` (4.7GB, conversational)

### Memory Settings

In `scripts/run.py`, adjust consolidation threshold:

```python
events = agent.episodic.sample_for_sleep(threshold=0.15)  # Lower = more memories
```

### Ollama URL

Default: `http://localhost:11434`

If running Ollama on a different host/port:
```python
agent = LivingAgent(model="llama3.2", ollama_url="http://192.168.1.100:11434")
```

---

## Architecture Highlights

### Memory System
1. **Working Memory**: Recent conversation turns (max 8)
2. **Episodic Memory**: All events with timestamps and salience scores
3. **Semantic Memory**: Abstracted facts organized by category
4. **Retrieval**: Embedding-based similarity search

### Consolidation Logic
- Categorizes episodic events (identity, preference, behavior, memory, general)
- Keeps most recent fact per category (handles contradictions)
- Extracts quoted phrases and preferences
- Removes outdated facts when newer ones are added

### Search Integration
- Automatic detection of search-worthy queries
- DuckDuckGo API (no key needed, privacy-focused)
- Results integrated into LLM context
- Source attribution in responses

---

## Limitations & Future Work

### Current Limitations
- Simple keyword-based search trigger detection
- No actual model fine-tuning (consolidation stores but doesn't update weights)
- Memory only lives in JSON (no true database)
- No forgetting/pruning mechanism

### Planned Enhancements
- LoRA fine-tuning during sleep phase
- Vector database (e.g., Milvus, Weaviate) for memory
- Multi-user support with separate memory spaces
- Better salience detection (ML-based scoring)
- Semantic memory update detection (preventing outdated facts)
- Export/import of memory snapshots

---

## Repository Structure

