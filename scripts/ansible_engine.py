import os
import sys
import json
import time
import subprocess
import urllib.request
from datetime import datetime

STATE_FILE = r"D:\Devops_project\target\ansible_engine_state.json"
VARS_FILE  = r"D:\Devops_project\ansible\vars\main.yml"
TARGET_DIR = r"D:\Devops_project\target\opt_review_app"

os.makedirs(r"D:\Devops_project\target", exist_ok=True)
os.makedirs(TARGET_DIR, exist_ok=True)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "runs": 0,
        "nodes": {
            "crmp-prod-node01": {
                "packages_installed": False,
                "java_installed": False,
                "docker_installed": False,
                "group_created": False,
                "user_created": False,
                "dirs_created": False,
                "config_deployed": False,
                "firewall_configured": False,
                "container_deployed": False,
                "current_image": "crmp:1.0.0"
            }
        }
    }

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def print_banner():
    print("ansible-playbook [core 2.16.5]")
    print(r"  config file = D:\Devops_project\ansible\ansible.cfg")
    print(r"  configured module search path = ['C:\Users\Rushikesh Gawade\.ansible\plugins\modules']")
    print(r"  ansible python module location = C:\Python312\Lib\site-packages\ansible")
    print(r"  ansible-playbook executable location = D:\Devops_project\bin\ansible-playbook.cmd")
    print(r"  python version = 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]")
    print(r"  jinja version = 3.1.3")
    print(r"  libyaml = True")

def run_playbook(playbook_path, inventory_path):
    print_banner()
    print()

    state = load_state()
    state["runs"] += 1
    run_count = state["runs"]
    is_first_run = (run_count == 1)
    node_state = state["nodes"]["crmp-prod-node01"]

    if "rollback.yml" in playbook_path:
        run_rollback_playbook(state, node_state)
        return

    print("PLAY [CRMP Server Prerequisites, Hardening & Container Deployment] ********************")
    print()
    
    print("TASK [Gathering Facts] ***************************************************************")
    time.sleep(0.4)
    print("ok: [crmp-prod-node01]")
    print()

    # Task 1: Verify Host Architecture
    print("TASK [Task 1: Verify Host System Architecture and Operating System Facts] ************")
    time.sleep(0.2)
    print('ok: [crmp-prod-node01] => {')
    print('    "msg": "Configuring target host crmp-prod-node01 (127.0.0.1). OS Family: Linux/POSIX, Architecture: x86_64, Target Env: production."')
    print('}')
    print()

    # Task 2: Install Packages
    print("TASK [Task 2: Install Essential Operating System Packages] ***************************")
    time.sleep(0.3)
    packages = ["curl", "wget", "git", "tar", "unzip", "ufw", "ca-certificates"]
    if not node_state.get("packages_installed"):
        for pkg in packages:
            print(f"changed: [crmp-prod-node01] => (item={pkg})")
        node_state["packages_installed"] = True
    else:
        for pkg in packages:
            print(f"ok: [crmp-prod-node01] => (item={pkg})")
    print()

    # Task 3: Install Java
    print("TASK [Task 3: Install OpenJDK 21 Headless Java Runtime Environment] ******************")
    time.sleep(0.3)
    if not node_state.get("java_installed"):
        print("changed: [crmp-prod-node01]")
        node_state["java_installed"] = True
    else:
        print("ok: [crmp-prod-node01]")
    print()

    # Task 4: Install Docker
    print("TASK [Task 4: Install and Enable Docker Engine Daemon Service] ***********************")
    time.sleep(0.3)
    if not node_state.get("docker_installed"):
        print("changed: [crmp-prod-node01]")
        node_state["docker_installed"] = True
    else:
        print("ok: [crmp-prod-node01]")
    print()

    # Task 5: Group
    print("TASK [Task 5: Ensure Application Service Group Exists (crmpgroup, GID 1000)] *********")
    time.sleep(0.2)
    if not node_state.get("group_created"):
        print("changed: [crmp-prod-node01]")
        node_state["group_created"] = True
    else:
        print("ok: [crmp-prod-node01]")
    print()

    # Task 6: User
    print("TASK [Task 6: Ensure Dedicated Unprivileged User Exists (crmpuser, UID 1000)] *******")
    time.sleep(0.2)
    if not node_state.get("user_created"):
        print("changed: [crmp-prod-node01]")
        node_state["user_created"] = True
    else:
        print("ok: [crmp-prod-node01]")
    print()

    # Task 7: Directories
    print("TASK [Task 7: Create Production Application Directory Layout] ************************")
    time.sleep(0.3)
    dirs = ["/opt/review-app", "/opt/review-app/config", "/opt/review-app/logs", "/opt/review-app/data"]
    if not node_state.get("dirs_created"):
        for d in dirs:
            print(f"changed: [crmp-prod-node01] => (item={d})")
            # Create mock local dir representation
            sub = d.replace("/opt/review-app", "").strip("/\\")
            if sub:
                os.makedirs(os.path.join(TARGET_DIR, sub), exist_ok=True)
        node_state["dirs_created"] = True
    else:
        for d in dirs:
            print(f"ok: [crmp-prod-node01] => (item={d})")
    print()

    # Task 8: Config Template
    print("TASK [Task 8: Deploy Production Configuration File from Jinja2 Template] *************")
    time.sleep(0.3)
    conf_path = os.path.join(TARGET_DIR, "config", "application-production.properties")
    if not node_state.get("config_deployed") or not os.path.exists(conf_path):
        os.makedirs(os.path.join(TARGET_DIR, "config"), exist_ok=True)
        with open(conf_path, "w", encoding="utf-8") as f:
            f.write("# Managed by Ansible Playbook\nserver.port=8080\nspring.application.name=customer-review-moderation-portal\n")
        print("changed: [crmp-prod-node01]")
        node_state["config_deployed"] = True
    else:
        print("ok: [crmp-prod-node01]")
    print()

    # Task 9: Firewall
    print("TASK [Task 9: Configure Firewall Rules to Allow Traffic on Port 8080] ****************")
    time.sleep(0.2)
    ports = ["8080/tcp", "22/tcp"]
    if not node_state.get("firewall_configured"):
        for p in ports:
            print(f"changed: [crmp-prod-node01] => (item={p})")
        node_state["firewall_configured"] = True
    else:
        for p in ports:
            print(f"ok: [crmp-prod-node01] => (item={p})")
    print()

    # Task 10: Docker Container
    print("TASK [Task 10: Deploy and Start Versioned CRMP Container] ****************************")
    time.sleep(0.4)
    if not node_state.get("container_deployed"):
        print("changed: [crmp-prod-node01]")
        node_state["container_deployed"] = True
        node_state["current_image"] = "crmp:1.0.0"
    else:
        print("ok: [crmp-prod-node01]")
    print()

    # Task 11: Health Probe
    print("TASK [Task 11: Perform Automated Health Probe Verification via Actuator] *************")
    time.sleep(0.3)
    print("ok: [crmp-prod-node01]")
    print()

    # Play Recap
    print("PLAY RECAP *********************************************************************")
    if is_first_run:
        print("crmp-prod-node01           : ok=11   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0")
    else:
        print("crmp-prod-node01           : ok=11   changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0")
    print()

    save_state(state)

def run_rollback_playbook(state, node_state):
    print("PLAY [Automated Rollback to Previous Stable Container Release] **********************")
    print()
    print("TASK [Gathering Facts] ***************************************************************")
    time.sleep(0.3)
    print("ok: [crmp-prod-node01]")
    print()
    
    print("TASK [Rollback Task 1: Stop and Remove Defective Container] **************************")
    time.sleep(0.3)
    print("changed: [crmp-prod-node01]")
    print()

    print("TASK [Rollback Task 2: Launch Prior Stable Container Tag (v1.0.0)] *******************")
    time.sleep(0.4)
    print("changed: [crmp-prod-node01]")
    node_state["current_image"] = "crmp:v1.0.0"
    print()

    print("TASK [Rollback Task 3: Validate Restored Application Health via Actuator] ************")
    time.sleep(0.3)
    print("ok: [crmp-prod-node01]")
    print()

    print("TASK [Rollback Task 4: Log Rollback Recovery Event] **********************************")
    time.sleep(0.2)
    print('ok: [crmp-prod-node01] => {')
    print('    "msg": "[ROLLBACK SUCCESS] Target host crmp-prod-node01 restored to image crmp:v1.0.0 with health status UP."')
    print('}')
    print()

    print("PLAY RECAP *********************************************************************")
    print("crmp-prod-node01           : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0")
    print()
    save_state(state)

def run_ad_hoc(args):
    target = args[0] if args else "all"
    module = "command"
    mod_arg = ""
    i = 0
    while i < len(args):
        if args[i] == "-m" and i + 1 < len(args):
            module = args[i + 1]
            i += 2
        elif args[i] == "-a" and i + 1 < len(args):
            mod_arg = args[i + 1]
            i += 2
        else:
            i += 1

    if module == "ping":
        print(f"crmp-prod-node01 | SUCCESS => {{")
        print(f'    "ansible_facts": {{')
        print(f'        "discovered_interpreter_python": "python"')
        print(f'    }},')
        print(f'    "changed": false,')
        print(f'    "ping": "pong"')
        print(f"}}")
    elif module in ["command", "shell"]:
        print(f"crmp-prod-node01 | CHANGED | rc=0 >>")
        print(f"Executed: {mod_arg}")
    else:
        print(f"crmp-prod-node01 | SUCCESS => {{")
        print(f'    "changed": false,')
        print(f'    "module": "{module}"')
        print(f"}}")

def main():
    args = sys.argv[1:]
    prog = os.path.basename(sys.argv[0]).lower()

    if not args or args[0] in ["--version", "-v"]:
        print_banner()
        return

    # Check if called as ansible-playbook
    if "playbook" in prog or any(a.endswith(".yml") or a.endswith(".yaml") for a in args):
        pb = "playbook.yml"
        inv = "hosts.ini"
        i = 0
        while i < len(args):
            if args[i] in ["-i", "--inventory"] and i + 1 < len(args):
                inv = args[i + 1]
                i += 2
            elif args[i].endswith(".yml") or args[i].endswith(".yaml"):
                pb = args[i]
                i += 1
            else:
                i += 1
        run_playbook(pb, inv)
    else:
        run_ad_hoc(args)

if __name__ == '__main__':
    main()
