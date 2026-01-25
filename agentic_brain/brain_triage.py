import requests
import urllib3
import ollama
import json

# --- Verified Configuration ---
INDEXER_HOST = 'https://127.0.0.1:9200'
INDEXER_USER = 'admin'
INDEXER_PASS = 'REDACTED'
MODEL = 'llama3.2'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_latest_alerts_from_indexer():
    url = f"{INDEXER_HOST}/wazuh-alerts-*/_search"
    # Looking for the most recent alert level 3 or higher
    query = {
        "size": 1,
        "sort": [{"timestamp": {"order": "desc"}}],
        "query": {"range": {"rule.level": {"gte": 3}}}
    }
    
    try:
        print(f"[*] Querying Indexer for the latest security events...")
        response = requests.get(
            url, 
            auth=(INDEXER_USER, INDEXER_PASS), 
            json=query, 
            verify=False
        )
        response.raise_for_status()
        hits = response.json().get('hits', {}).get('hits', [])
        return [hit['_source'] for hit in hits]
    except Exception as e:
        print(f"[!] Indexer Query Failed: {e}")
        return []

def ai_analyze_threat(alert):
    description = alert.get('rule', {}).get('description', 'Unknown')
    level = alert.get('rule', {}).get('level', 0)
    # Some alerts use 'full_log', others use 'message'
    log_content = alert.get('full_log') or alert.get('message') or "No raw log available"
    agent_name = alert.get('agent', {}).get('name', 'Unknown')

    prompt = f"""
    SYSTEM: You are a Senior Cyber Security Analyst.
    TASK: Analyze this alert from agent '{agent_name}'.
    
    ALERT: {description} (Level: {level})
    RAW DATA: {log_content}
    
    INSTRUCTIONS: Provide a brief summary, threat level, and one immediate action.
    """
    
    print(f"[*] Alert found! Asking {MODEL} to investigate...")
    response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

if __name__ == "__main__":
    alerts = get_latest_alerts_from_indexer()
    
    if alerts:
        print(f"[+] Found Alert: {alerts[0].get('rule', {}).get('description')}")
        analysis = ai_analyze_threat(alerts[0])
        print("\n" + "="*30)
        print("🛡️ AI SECURITY ANALYSIS REPORT")
        print("="*30)
        print(analysis)
    else:
        print("[!] No alerts found in the Indexer yet. Try triggering an alert with 'sudo ls /root'.")

