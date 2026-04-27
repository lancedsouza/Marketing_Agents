import ollama

def detect_hiring_quality(state):
    """
    Node to decide: Is this a Senior role in Fintech/GCC?
    """
    job_text = state["raw_scraped_text"]
    
    prompt = f"""
    Analyze the following job data: {job_text}
    
    Criteria:
    1. Is the role 'Senior' (VP, Director, Head, CXO)?
    2. Is the company in 'Fintech' or a 'GCC' (Global Capability Center)?
    
    Return JSON only: 
    {{ "is_senior": bool, "is_target_industry": bool, "reason": str }}
    """
    
    # Use your local Ollama
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    
    # Update the state based on LLM reasoning
    # If not senior, we will tell LangGraph to 'END' the process here.
    return {"analysis_result": response['message']['content']}