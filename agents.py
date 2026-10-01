from crewai import Agent, LLM

def get_llm(api_key: str, model_name: str = "gemini/gemini-3.5-flash") -> LLM:
    return LLM(
        model=model_name,
        api_key=api_key,
        temperature=0.4
    )

def create_agents(api_key: str, model_name: str):
    llm = get_llm(api_key, model_name)

    lead_scout = Agent(
        role='Lead Scout & Analyst',
        goal='Analyze the freelance job description, calculate a fit score (1-10), identify red flags, and make a GO/NO-GO decision.',
        backstory='You are a seasoned freelance strategist. You have an eagle eye for scope creep, difficult clients, and highly profitable opportunities.',
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

    proposal_architect = Agent(
        role='Proposal Architect',
        goal='Write a highly converting, concise proposal (under 300 words) tailored to the job description.',
        backstory='You are a master copywriter who specializes in winning freelance bids. You know clients hate reading long essays, so you get straight to the value proposition.',
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

    project_manager = Agent(
        role='Project Manager',
        goal='Break the job down into a clear milestones table, define a timeline, and identify potential project risks.',
        backstory='You are an agile project manager. You create realistic timelines and protect the freelancer by clearly defining what is out of scope.',
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

    finance_officer = Agent(
        role='Finance Officer',
        goal='Determine competitive pricing, payment schedules, and terms. Output a final JSON summary block at the end.',
        backstory='You are a freelance CFO. You ensure projects are priced profitably and payment terms protect against non-payment.',
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

    return lead_scout, proposal_architect, project_manager, finance_officer