from crewai import Task
from agents import create_agents

def create_tasks(agents: tuple, job_data):
    """Creates the 4 tasks, now incorporating freelancer profile context."""
    lead_scout, proposal_architect, project_manager, finance_officer = agents

    task1 = Task(
        description=f"""
        Analyze the following freelance job description carefully:
        {job_data.description}
        
        Freelancer Profile:
        Skills: {job_data.skills}
        Experience: {job_data.experience}
        
        1. Give a 'Fit Score' out of 10 based on how well the freelancer's profile matches the job requirements.
        2. List potential red flags in the post.
        3. Make a definitive GO or NO-GO recommendation based on their skills and the job.
        """,
        expected_output="A brief markdown report detailing the fit score, red flags, and GO/NO-GO decision.",
        agent=lead_scout
    )

    task2 = Task(
        description=f"""
        Based on the Lead Scout's analysis, draft a winning proposal for this job.
        
        Context to use in proposal:
        - Freelancer Name: {job_data.name}
        - Key Skills: {job_data.skills}
        - Experience: {job_data.experience}
        
        The tone must be: {job_data.tone}.
        Keep it strictly under 300 words. Sign off using the freelancer's name. Highlight how their specific skills and experience solve the client's problem.
        """,
        expected_output="A tailored, concise proposal (under 300 words) signed by the freelancer.",
        agent=proposal_architect
    )

    task3 = Task(
        description=f"""
        Review the job description and the proposal. 
        Freelancer availability: {job_data.availability}
        
        1. Create a detailed Milestones table (Milestone, Deliverable, Estimated Days). Ensure the timeline matches the freelancer's availability.
        2. Provide an overall timeline.
        3. Document 3 potential project risks and mitigations.
        """,
        expected_output="A markdown document containing a milestones table, timeline, and risk analysis.",
        agent=project_manager
    )

    task4 = Task(
        description=f"""
        Based on the milestones and project scope, determine the financials.
        
        Pricing Context:
        - Freelancer Target Hourly Rate: ${job_data.rate}/hr
        
        1. Estimate total hours required, then suggest a total project price (in USD) using the target hourly rate.
        2. Provide a payment schedule.
        3. Draft standard terms of service regarding revisions.
        
        CRITICAL INSTRUCTION: At the very end of your output, you MUST include a raw JSON block enclosed in ```json ... ``` that contains these exact keys:
        {{
            "fit_score_1_to_10": <int>,
            "decision": "<GO or NO-GO>",
            "estimated_hours": <int>,
            "recommended_price_usd": <int>
        }}
        """,
        expected_output="Financial terms and a strictly formatted JSON block at the end with the requested metrics.",
        agent=finance_officer
    )

    return [task1, task2, task3, task4]