import json
import os
import subprocess
from typing import Any, Dict, List


def run_xurl(cmd: List[str], verbose_if_failed: bool = False) -> Dict[str, Any]:
    """
    Run `xurl` and return its JSON stdout as a Python dict.
    Currently extremely simple without any retry logic.
    """
    # Get Bearer Token from environment
    bearer_token = os.getenv('BEARER_TOKEN')
    if not bearer_token:
        raise ValueError("BEARER_TOKEN environment variable is required for xurl authentication")
    
    # Add Authorization header to the command
    auth_header = f"Authorization: Bearer {bearer_token}"
    full_cmd = cmd + ["-H", auth_header]
    
    try:
        completed = subprocess.run(full_cmd, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        if verbose_if_failed:
            print(exc.stderr)
            print(f"\n[ xurl failed with exit code {exc.returncode} ]", flush=True)
            if exc.stdout:
                print("── stdout ──")
                print(exc.stdout, end="", flush=True)
            if exc.stderr:
                print("── stderr ──")
                print(exc.stderr, end="", flush=True)
        raise
    return json.loads(completed.stdout)
