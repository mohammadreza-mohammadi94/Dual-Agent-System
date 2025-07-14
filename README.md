# Dual Agent System

An intelligent assistant based on LangGraph that performs tasks and then evaluates and corrects its own work using two distinct AI agents.

## 🚀 Core Concept

This project implements an agentic architecture where two AI agents collaborate to achieve the best possible result:

1.  **The Worker Agent:** This agent is responsible for the primary task. It uses a variety of tools (such as web Browse, running Python code, and managing files) to accomplish its goal.
2.  **The Evaluator Agent:** This agent acts as a critic. It compares the Worker Agent's output against the user-defined "success criteria." If the output doesn't meet the standards, it rejects the result and provides constructive feedback to the Worker Agent for revision.

This feedback loop allows the system to autonomously correct itself, significantly improving the quality of the final response.


## ✨ Features

  - **Dual-Agent Architecture:** A collaboration between a Worker and an Evaluator agent to ensure high-quality output.
  - **Self-Correction Loop:** The ability to autonomously review and revise responses before they are presented to the user.
  - **Powerful Toolset:** Includes web Browse, Python code execution, web search, and file management.
  - **Web-Based UI:** Implemented with Gradio for easy and intuitive interaction.
  - **Traceable:** All agent steps are fully traceable and debuggable using LangSmith.

## 🛠️ Tech Stack

  - Python 3.11+
  - LangChain / LangGraph
  - OpenAI
  - Gradio
  - Playwright
  - Google Serper API

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

**1. Clone the Repository**

```bash
git clone https://github.com/mohammadreza-mohammadi94/Dual-Agent-System.git
cd Dual-Agent-System
```

**2. Create and Activate a Virtual Environment**

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS or Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**

Create a file named `.env` in the root of the project and add your API keys. You can use the `env.example` file (if it exists) as a template.

```env
OPENAI_API_KEY="sk-..."
LANGSMITH_API_KEY="ls__..."
SERPER_API_KEY="..."

# Optional - for push notifications
PUSHOVER_TOKEN="..."
PUSHOVER_USER="..."
```

## ▶️ Running the Application

Once the setup is complete, run the application with the following command:

```bash
python app.py
```

Then, open your browser and navigate to `http://127.0.0.1:7860`.

