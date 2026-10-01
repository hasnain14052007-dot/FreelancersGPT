# 🤖 FreelanceOS: The Agentic Copilot

FreelanceOS is a powerful AI-driven dashboard that acts as your personal agency team. Just paste a freelance job description, and a crew of 4 specialized AI agents will analyze the feasibility, write a winning proposal, plan the milestones, and calculate profitable pricing.

![FreelanceOS Screenshot](https://via.placeholder.com/800x400.png?text=UI+Screenshot+Placeholder)

## ✨ Features
- **4-Agent CrewAI Architecture**: Lead Scout, Proposal Architect, Project Manager, Finance Officer.
- **Secure & Production Ready**: API keys are securely managed server-side. No leaks in UI or logs.
- **Resilient AI**: Automatic rate-limit handling and model fallbacks (`gemini-2.5-flash` to `lite`).
- **Dashboard UI**: Real-time progress, metric cards, sample templates, and copy-ready outputs.
- **Export Options**: Download full reports as `.md` or `.docx`.

## 🏗️ Architecture
```mermaid
graph TD;
    User-->|Job Description| UI[Streamlit App];
    UI-->|Triggers| Crew[CrewAI Orchestrator];
    Crew-->|Step 1| A1[Lead Scout - Fit & Red Flags];
    A1-->|Step 2| A2[Proposal Architect - Pitch];
    A2-->|Step 3| A3[Project Manager - Timeline];
    A3-->|Step 4| A4[Finance Officer - Pricing & JSON extraction];
    A4-->|Final Payload| UI;
    UI-->|Export| File[MD/DOCX Download];