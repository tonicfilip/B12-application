import json
import hmac
import hashlib
import os
import requests # type: ignore
from datetime import datetime, timezone

def submit():

    name = "Filip Tonic"
    email = "tonicfilip@outlook.com"
    resume_link = "https://github.com/tonicfilip/B12-application/blob/main/Filip%20Toni%C4%87%20Resume.pdf"
    signing_secret = os.getenv("B12_SIGNING_SECRET", "hello-there-from-b12")
    
    repo_link = f"https://github.com/tonicfilip/B12-application"
    run_id = os.getenv("GITHUB_RUN_ID", "b12-12345")
    action_run_link = f"{repo_link}/actions/runs/{run_id}"

    payload = {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "name": name,
        "email": email,
        "resume_link": resume_link,
        "repository_link": repo_link,
        "action_run_link": action_run_link
    }

    json_body = json.dumps(
        payload, 
        sort_keys=True, 
        separators=(',', ':'), 
        ensure_ascii=False
    ).encode('utf-8')

    signature = hmac.new(
        signing_secret.encode('utf-8'),
        json_body,
        hashlib.sha256
    ).hexdigest()

    url = "https://b12.io/apply/submission"
    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}"
    }

    resp = requests.post(url, data=json_body, headers=headers)
    
    if resp and resp.status_code == 200:
        print("Submission successful!")
        print(resp.json().get("receipt"))
    else:
        print(f"Failed with status {resp.status_code}")
        exit(1)

if __name__ == "__main__":
    submit()