# dialogue_manager

**dialogue_manager** contains training data, stories, and action definitions for a natural language understanding (NLU)–powered dialogue system.  
It is designed to work with frameworks such as [Rasa](https://rasa.com/) to train models that can recognize user intents, extract entities, and trigger contextually appropriate actions.

---

## Features

- **NLU Training Data**: Define user intents and sample utterances for accurate intent classification.
- **Stories**: Example conversation flows demonstrating how the assistant should handle multi-turn interactions.
- **Actions**: Custom responses or backend functions triggered by detected intents and slot values.
- **Extensible Structure**: Easily expand with new intents, entities, slots, and stories as your bot’s capabilities grow.

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Installation](#installation)  
3. [Repository Structure](#repository-structure)  
4. [Usage](#usage)  
5. [Extending the Bot](#extending-the-bot)  
6. [Contributing](#contributing)  
7. [License](#license)

---

## 1. Prerequisites

- Python 3.8+  
- [Rasa](https://rasa.com/) installed (`pip install rasa` or `pip install rasa[full]`)
- Basic understanding of intents, entities, and stories in Rasa.

---

## 2. Installation

```bash
git clone https://github.com/toutia/dialogue_manager.git
cd dialogue_manager
pip install -r requirements.txt
