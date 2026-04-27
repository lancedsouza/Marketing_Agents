from app.scrapers.selenium_jobs import get_driver # Reuse your driver logic
from selenium.webdriver.common.by import By
import ollama
import time

def find_founder_details(state):
    """
    Agent Node: Finds the name and title of the decision maker.
    """
    company = state["company"]
    print(f"🕵️ Searching for decision makers at {company}...")

    driver = get_driver()
    search_query = f'site:linkedin.com/in "{company}" ("Founder" OR "CEO" OR "Talent Acquisition")'
    
    try:
        # 1. Search Google for the person
        driver.get(f"https://www.google.com/search?q={search_query}")
        time.sleep(2)

        # 2. Extract the first 3 search results
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        raw_people_data = ""
        for res in results[:3]: # Take top 3 to be sure
            raw_people_data += res.text + "\n---\n"

        # 3. Use Ollama to pick the BEST person from the snippets
        # This is where the 'Agent' part happens
        prompt = f"""
        Analyze these search results for the company '{company}':
        {raw_people_data}

        Identify the most senior person (Founder, CEO, or Head of HR).
        Return ONLY a JSON object:
        {{
            "contact_name": "Full Name",
            "contact_title": "Exact Title",
            "linkedin_url": "URL from the snippet"
        }}
        """
        
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        contact_info = response['message']['content']
        
        # In a real app, you'd parse the JSON string here
        return {
            "contact_details": contact_info,
            "status": "Contact Found"
        }

    except Exception as e:
        print(f"Error finding contact: {e}")
        return {"status": "Contact Search Failed"}
    finally:
        driver.quit()