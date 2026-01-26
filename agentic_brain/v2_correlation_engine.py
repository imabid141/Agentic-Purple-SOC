import requests
import urllib3
import ollama
import json

# --- Configuration ---
INDEXER_HOST = 'https://127.0.0.1:9200'
INDEXER_USER = 'admin'
INDEXER_PASS = 'REDACTED' # Use your real password here
MODEL = 'llama3.2'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_event_chain(size=10):
    url = f"{INDEXER_HOST}/wazuh-alerts-*/_search"
    # We query the last 10 alerts to find a pattern
    query = {
        "size": size,
        "sort": [{"timestamp": {"order": "desc"}}],
        "query": {"range": {"rule.level": {"gte": 3}}}
    }
    
    try:
        print(f"[*] Extracting the last {size} security events for correlation...")
        response = requests.get(url, auth=(INDEXER_USER, INDEXER_PASS), json=query, verify=False)
        response.raise_for_status()
        hits = response.json().get('hits', {}).get('hits', [])
        return [hit['_source'] for hit in hits]
    except Exception as e:
        print(f"[!] Intelligence Extraction Failed: {e}")
        return []

def ai_correlate_events(events):
    # Format the events into a readable timeline for the AI
    timeline = ""
    for i, event in enumerate(reversed(events)):
        desc = event.get('rule', {}).get('description')
        ts = event.get('timestamp')
        timeline += f"{i+1}. [{ts}] - {desc}\n"

    prompt = f"""
    SYSTEM: You are an Expert Cyber Threat Hunter.
    TASK: Analyze the following timeline of events for a 'Chain of Attack'.
    
    TIMELINE:
    {timeline}
    
    INSTRUCTIONS: 
    1. Identify if these events are related or isolated.
    2. Determine if there is a 'Kill Chain' progression (e.g., multiple failed logins followed by a success).
    3. Provide a 'Final Verdict' and 'Response Strategy'.
    """
    
    print(f"[*] Analyzing Timeline with {MODEL}...")
    response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

if __name__ == "__main__":
    event_chain = get_event_chain(10)
    
    if event_chain:
        analysis = ai_correlate_events(event_chain)
        print("\n" + "="*40)
        print("🕵️ AI THREAT CORRELATION REPORT")
        print("="*40)
        print(analysis)
    else:
        print("[!] No events found to analyze.")

