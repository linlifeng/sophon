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

