# ✈️ AYKA - Airline AI Assistant

**AYKA** is a conversational AI assistant designed to help users with flight-related services for "United Airline." Built using **LangChain** and **OpenAI**, AYKA leverages tool calling, memory, and prompt engineering to handle common flight tasks such as booking, checking prices, cancellations, and more.

---

## 🚀 Features

- 🔧 **Tool Calling**: Built-in tools for booking, checking flight status, cancellations, and rescheduling.
- 💾 **Memory Saver**: Retains context during the conversation using in-memory checkpointing.
- 🧠 **Custom Prompts**: System message ensures AYKA behaves as an airline assistant.
- 🧱 **Modular Class Design**: Easily importable and reusable in other Python files.
- 🔒 **Secure API Key**: Accepts API key as an argument or via environment variable.

---

## 📁 Project Structure

├── flight_agent.py # Main FlightAgent class
├── main.py # Example script to use the agent
├── requirements.txt # Python dependencies

### 🖼️ Screenshot of AYKA in Action

![Chat Example](output/Response_2.png)

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/ayka-airline-ai.git
cd ayka-airline-ai


