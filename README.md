Chimera (HEASI) - V2.5
A Self-Evolving Autonomous Agent Framework

Chimera is a Python-based framework for creating an autonomous agent that can recursively improve its own source code. It uses a modular architecture and a live generative AI (Google's Gemini model) to identify problems, generate solutions, validate them in a secure environment, and permanently commit the successful changes to its own codebase using a professional, git-based workflow.
How It Works

The agent operates in a continuous evolutionary loop, orchestrated by main.py. Each cycle consists of several distinct stages:

    Analysis (CAE): The Cognitive Analysis Engine consults its memory (evolution_log.json) and a backlog of problems to identify a task it has not yet solved.

    Generation (GSM): The Generative Synthesis Module connects to a live AI, sending it the current source code and the problem statement. The AI generates a proposed code modification and a new pytest unit test to validate the change.

    Validation (GVE): The Git-based Validation Environment creates a new feature branch, applies the new code and tests, and runs pytest. If the tests fail, the branch is discarded.

    Consensus (DCP): If validation succeeds, the Distributed Consensus Protocol simulates a network of peers voting on the change.

    Persistence (GPM): If consensus is reached, the Git Persistence Module merges the feature branch into main, creating a permanent record of the evolution. It then pushes the changes to the remote origin.

The agent then pauses and begins a new cycle, using its newly evolved code as the new baseline.
Setup

    Clone the Repository:

    git clone [https://github.com/Seymore-Bawts/chimera.git](https://github.com/Seymore-Bawts/chimera.git)
    cd chimera

    Create a Virtual Environment:

    python3 -m venv venv
    source venv/bin/activate

    Install Dependencies:

    pip install -r requirements.txt

    Set Your API Key:

        Get a free Google AI Studio API key at aistudio.google.com.

        Open the chimera/config.py file.

        Replace "YOUR_API_KEY_HERE" with your actual key.

Usage

To run the agent and start its evolutionary process, execute the main script from the project root:

python3 main.py

To reset the agent's memory and have it re-solve all problems from the beginning, use the --reset flag:

python3 main.py --reset

