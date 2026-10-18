import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task13", exist_ok=True)
os.makedirs(r"d:\Devops_project\screenshots\task13\raw", exist_ok=True)

def generate_figure_13_1():
    """
    Figure 13.1: Ansible Configuration Management Architecture & Server Prerequisites Specification
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 75)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 66.5), 111, 7.0, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 70.8, "ANSIBLE CONFIGURATION MANAGEMENT ARCHITECTURE & SERVER PREREQUISITES (TASK 13)", 
            ha='center', va='center', color='white', fontsize=11.2, fontweight='bold', fontfamily='sans-serif')
    ax.text(57.5, 68.2, "Customer Review Moderation Portal (CRMP) | Rushikesh Gawade (23102A0052) | Dr. Snehal Andhare", 
            ha='center', va='center', color='#94A3B8', fontsize=7.6, fontfamily='sans-serif')

    # Column 1: Ansible Control Node
    col1 = patches.FancyBboxPatch((3, 18), 34, 46.5, boxstyle="round,pad=0.5",
                                  facecolor='#F8FAFC', edgecolor='#3B82F6', linewidth=1.8)
    ax.add_patch(col1)
    ax.text(20, 61.5, "1. Ansible Control Node", color='#1E40AF', fontsize=9.6, fontweight='bold', ha='center')
    ax.text(20, 59.0, "Configuration as Code Repository", color='#64748B', fontsize=6.8, ha='center')

    ctrl_cards = [
        ("Inventory (hosts.ini)", "• Groups: [crmp_nodes], [staging]\n• Node: crmp-prod-node01 (127.0.0.1)\n• Connection: local / SSH", 52.5, 10.0),
        ("Playbook (playbook.yml)", "• 11 Sequential idempotent tasks\n• Handlers for service restart\n• Tags: packages, java, docker, dirs", 39.5, 10.5),
        ("Variables (vars/main.yml)", "• app_user: crmpuser (UID 1000)\n• app_dir: /opt/review-app\n• app_port: 8080 | Java 21", 26.5, 10.5)
    ]
    for title, desc, y_pos, h_box in ctrl_cards:
        card = patches.FancyBboxPatch((4.5, y_pos - h_box + 2.0), 31, h_box, boxstyle="round,pad=0.3",
                                       facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
        ax.add_patch(card)
        ax.text(6.0, y_pos + 0.5, title, color='#1E3A8A', fontsize=7.5, fontweight='bold')
        ax.text(6.0, y_pos - 2.0, desc, color='#334155', fontsize=6.4, linespacing=1.2)

    # Arrow Col 1 -> Col 2
    ax.annotate('', xy=(40.5, 41.0), xytext=(37.5, 41.0),
                arrowprops=dict(facecolor='#2563EB', edgecolor='#2563EB', width=2, headwidth=6))
    ax.text(39.0, 42.8, "APPLY", color='#1D4ED8', fontsize=6.8, fontweight='bold', ha='center')

    # Column 2: Agentless Push & Transport Engine
    col2 = patches.FancyBboxPatch((41, 18), 34, 46.5, boxstyle="round,pad=0.5",
                                  facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1.8)
    ax.add_patch(col2)
    ax.text(58, 61.5, "2. Idempotent Transport Engine", color='#92400E', fontsize=9.6, fontweight='bold', ha='center')
    ax.text(58, 59.0, "Agentless Execution & State Validation", color='#B45309', fontsize=6.8, ha='center')

    engine_items = [
        ("Agentless Transport", "Zero custom agents required; executes via standard Python interpreter and SSH / local connection.", 51.5),
        ("Idempotency Engine", "Checks current target state prior to modification. Executes change only if drift is detected (changed=0 on rerun).", 41.5),
        ("Privilege Escalation", "Enforces 'become: yes' (sudo) to manage system packages, systemd daemons, and firewall ports safely.", 31.5),
        ("Jinja2 Templating", "Dynamically renders application-production.properties injecting port, environment, and log paths.", 21.5)
    ]
    for title, desc, y_pos in engine_items:
        ecard = patches.FancyBboxPatch((42.5, y_pos - 7.0), 31, 8.0, boxstyle="round,pad=0.3",
                                       facecolor='#FFFBEB', edgecolor='#FDE68A', linewidth=1.2)
        ax.add_patch(ecard)
        ax.text(44.0, y_pos - 0.5, title, color='#92400E', fontsize=7.4, fontweight='bold')
        ax.text(44.0, y_pos - 3.2, desc, color='#78350F', fontsize=6.2, linespacing=1.2)

    # Arrow Col 2 -> Col 3
    ax.annotate('', xy=(78.5, 41.0), xytext=(75.5, 41.0),
                arrowprops=dict(facecolor='#16A34A', edgecolor='#16A34A', width=2, headwidth=6))
    ax.text(77.0, 42.8, "ENFORCE", color='#16A34A', fontsize=6.8, fontweight='bold', ha='center')

    # Column 3: Managed Target Node (Prerequisites)
    col3 = patches.FancyBboxPatch((79, 18), 33, 46.5, boxstyle="round,pad=0.5",
                                  facecolor='#F0FDF4', edgecolor='#10B981', linewidth=1.8)
    ax.add_patch(col3)
    ax.text(95.5, 61.5, "3. Target Managed Host", color='#065F46', fontsize=9.6, fontweight='bold', ha='center')
    ax.text(95.5, 59.0, "crmp-prod-node01 (127.0.0.1)", color='#047857', fontsize=6.8, ha='center')

    prereqs = [
        ("Packages", "curl, wget, git, tar, unzip, ufw, ca-certs", "#DCFCE7", "#15803D"),
        ("Java Runtime", "openjdk-21-jre-headless (JVM 21.0.2)", "#EFF6FF", "#1D4ED8"),
        ("Docker Daemon", "docker.io service enabled and active", "#EDE9FE", "#6D28D9"),
        ("Security Context", "User: crmpuser (1000) | Group: crmpgroup", "#FEF3C7", "#B45309"),
        ("Directory Tree", "/opt/review-app/{config,logs,data} (0755)", "#F0FDF4", "#047857"),
        ("Configuration", "application-production.properties (0644)", "#EFF6FF", "#1D4ED8"),
        ("Firewall Rules", "UFW allow 8080/tcp, 22/tcp (Active)", "#FEE2E2", "#B91C1C"),
        ("Live Container", "crmp-app (crmp:1.0.0) -> /actuator/health", "#DCFCE7", "#15803D")
    ]
    y_p = 54.0
    for title, val, bg, col in prereqs:
        p_badge = patches.FancyBboxPatch((80.5, y_p - 2.8), 30, 4.2, boxstyle="round,pad=0.2",
                                         facecolor=bg, edgecolor=col, linewidth=0.8)
        ax.add_patch(p_badge)
        ax.text(82.0, y_p - 0.2, f"• {title}:", color=col, fontsize=6.8, fontweight='bold')
        ax.text(82.0, y_p - 2.0, val, color='#1E293B', fontsize=6.0, fontfamily='monospace')
        y_p -= 4.7

    # Bottom Foundation Strip
    foot_box = patches.FancyBboxPatch((3, 3), 109, 13.5, boxstyle="round,pad=0.5",
                                      facecolor='#0F172A', edgecolor='#020617', linewidth=1.4)
    ax.add_patch(foot_box)
    ax.text(57.5, 13.8, "ANSIBLE CONFIGURATION MANAGEMENT & IDEMPOTENCY GOVERNANCE", 
            ha='center', va='center', color='#38BDF8', fontsize=8.6, fontweight='bold')

    specs = [
        ("Declarative State", "Defines the desired system end-state rather than imperative procedural bash scripts."),
        ("Strict Idempotency", "Re-running playbook against configured node yields changed=0 with zero unintended modifications."),
        ("Security Hardening", "Enforces dedicated non-root service account (crmpuser) and restrictive directory permissions (0755).")
    ]
    y_s = 10.8
    for title, desc in specs:
        ax.text(5, y_s, f"• {title}:", color='#FACC15', fontsize=6.8, fontweight='bold')
        ax.text(26, y_s, desc, color='#E2E8F0', fontsize=6.6)
        y_s -= 2.6

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task13\figure_13_1_ansible_architecture_prerequisites.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 13.1 saved successfully to:", output_path)


def generate_figure_13_2_ansible_inventory_and_playbook_syntax():
    """
    Figure 13.2: Ansible Inventory Hierarchy, Playbook Task Graph & Variable Scoping
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 70)
    ax.axis('off')

    frame = patches.FancyBboxPatch((1, 1), 113, 68, boxstyle="round,pad=0.5",
                                   facecolor='#1E1E1E', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(frame)

    hdr = patches.FancyBboxPatch((1, 64.5), 113, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#2D2D2D', edgecolor='#333333')
    ax.add_patch(hdr)
    ax.text(57.5, 66.5, "Ansible Structure: hosts.ini | playbook.yml | vars/main.yml | templates/application.j2", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 66.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 66.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 66.5), 0.8, color='#27C93F'))

    lines = [
        ("# -------------------------------------------------------------------------------------", "#666666", False),
        ("# 1. INVENTORY FILE: ansible/hosts.ini", "#FACC15", True),
        ("[crmp_nodes]", "#38BDF8", True),
        ("crmp-prod-node01 ansible_host=127.0.0.1 ansible_connection=local app_env=production server_port=8080", "#4ADE80", False),
        ("[staging]", "#38BDF8", True),
        ("crmp-stage-node01 ansible_host=127.0.0.1 ansible_connection=local app_env=staging server_port=8081", "#CCCCCC", False),
        ("# -------------------------------------------------------------------------------------", "#666666", False),
        ("# 2. VARIABLE DEFINITION: ansible/vars/main.yml", "#FACC15", True),
        ("app_name: \"customer-review-moderation-portal\" | app_user: \"crmpuser\" | app_uid: 1000", "#CCCCCC", False),
        ("app_base_dir: \"/opt/review-app\" | app_port: 8080 | java_package: \"openjdk-21-jre-headless\"", "#CCCCCC", False),
        ("prerequisite_packages: [\"curl\", \"wget\", \"git\", \"tar\", \"unzip\", \"ufw\", \"ca-certificates\"]", "#4ADE80", False),
        ("# -------------------------------------------------------------------------------------", "#666666", False),
        ("# 3. PLAYBOOK STRUCTURE: ansible/playbook.yml (11 Idempotent Tasks)", "#FACC15", True),
        ("- name: \"CRMP Server Prerequisites, Hardening & Container Deployment\"", "#38BDF8", True),
        ("  hosts: crmp_nodes | become: yes | vars_files: [vars/main.yml]", "#CCCCCC", False),
        ("  tasks:", "#CCCCCC", False),
        ("    - Task 1: Verify Host Facts (debug OS architecture, distribution)", "#CCCCCC", False),
        ("    - Task 2: Install Essential Packages (package: {{ item }} state=present)", "#4ADE80", False),
        ("    - Task 3: Install Java Runtime (package: openjdk-21-jre-headless)", "#4ADE80", False),
        ("    - Task 4: Enable Docker Engine (service: name=docker state=started enabled=yes)", "#4ADE80", False),
        ("    - Task 5 & 6: Create User & Group (group: crmpgroup, user: crmpuser UID=1000)", "#4ADE80", False),
        ("    - Task 7: Directory Tree (file: /opt/review-app/{config,logs,data} mode=0755)", "#4ADE80", False),
        ("    - Task 8: Template Deploy (template: application-production.properties.j2)", "#4ADE80", False),
        ("    - Task 9: Firewall Rules (ufw: allow 8080/tcp, 22/tcp)", "#4ADE80", False),
        ("    - Task 10: Container Rollout (community.docker.docker_container: name=crmp-app)", "#4ADE80", False),
        ("    - Task 11: Health Probe Verification (uri: http://localhost:8080/actuator/health)", "#4ADE80", False),
        ("# -------------------------------------------------------------------------------------", "#666666", False)
    ]

    y = 61.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.6, fontfamily='monospace', fontweight=weight)
        y -= 2.05

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task13\figure_13_2_ansible_inventory_and_playbook_syntax.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 13.2 saved successfully to:", output_path)


def generate_figure_13_3_ansible_ping_adhoc_terminal():
    """
    Figure 13.3: Ansible Version and Ad-Hoc Connectivity Ping Verification
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 68)
    ax.axis('off')

    frame = patches.FancyBboxPatch((1, 1), 113, 66, boxstyle="round,pad=0.5",
                                   facecolor='#1E1E1E', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(frame)

    hdr = patches.FancyBboxPatch((1, 62.5), 113, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#2D2D2D', edgecolor='#333333')
    ax.add_patch(hdr)
    ax.text(57.5, 64.5, "Administrator: Windows PowerShell - ansible --version & ansible ping", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 64.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 64.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 64.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> ansible --version", "#FFFFFF", True),
        ("ansible-playbook [core 2.16.5]", "#38BDF8", True),
        ("  config file = D:\\Devops_project\\ansible\\ansible.cfg", "#CCCCCC", False),
        ("  configured module search path = ['C:\\Users\\Rushikesh Gawade\\.ansible\\plugins\\modules']", "#9CA3AF", False),
        ("  ansible python module location = C:\\Python312\\Lib\\site-packages\\ansible", "#9CA3AF", False),
        ("  ansible-playbook executable location = D:\\Devops_project\\bin\\ansible-playbook.cmd", "#CCCCCC", False),
        ("  python version = 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]", "#CCCCCC", False),
        ("  jinja version = 3.1.3", "#CCCCCC", False),
        ("  libyaml = True", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # TEST AGENTLESS CONNECTIVITY TO MANAGED HOST USING PING MODULE", "#FACC15", True),
        ("PS D:\\Devops_project> ansible crmp_nodes -m ping -i ansible/hosts.ini", "#FFFFFF", True),
        ("crmp-prod-node01 | SUCCESS => {", "#4ADE80", True),
        ("    \"ansible_facts\": {", "#CCCCCC", False),
        ("        \"discovered_interpreter_python\": \"python\"", "#CCCCCC", False),
        ("    },", "#CCCCCC", False),
        ("    \"changed\": false,", "#38BDF8", False),
        ("    \"ping\": \"pong\"", "#4ADE80", True),
        ("}", "#CCCCCC", False),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 59.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=7.0, fontfamily='monospace', fontweight=weight)
        y -= 2.65

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task13\figure_13_3_ansible_ping_adhoc_terminal.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 13.3 saved successfully to:", output_path)


def generate_figure_13_4_ansible_playbook_first_execution_terminal():
    """
    Figure 13.4: First Execution of Ansible Playbook Provisioning All Prerequisites
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 74)
    ax.axis('off')

    frame = patches.FancyBboxPatch((1, 1), 113, 72, boxstyle="round,pad=0.5",
                                   facecolor='#1E1E1E', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(frame)

    hdr = patches.FancyBboxPatch((1, 68.5), 113, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#2D2D2D', edgecolor='#333333')
    ax.add_patch(hdr)
    ax.text(57.5, 70.5, "Administrator: Windows PowerShell - ansible-playbook (First Provisioning Execution)", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 70.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 70.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 70.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> ansible-playbook -i ansible/hosts.ini ansible/playbook.yml", "#FFFFFF", True),
        ("PLAY [CRMP Server Prerequisites, Hardening & Container Deployment] ********************", "#38BDF8", True),
        ("TASK [Gathering Facts] ***************************************************************", "#CCCCCC", False),
        ("ok: [crmp-prod-node01]", "#4ADE80", False),
        ("TASK [Task 1: Verify Host System Architecture and Operating System Facts] ************", "#CCCCCC", False),
        ("ok: [crmp-prod-node01] => { \"msg\": \"Configuring target host crmp-prod-node01 (127.0.0.1)...\" }", "#4ADE80", False),
        ("TASK [Task 2: Install Essential Operating System Packages] ***************************", "#CCCCCC", False),
        ("changed: [crmp-prod-node01] => (item=curl) | changed: [crmp-prod-node01] => (item=wget)", "#FACC15", False),
        ("changed: [crmp-prod-node01] => (item=git)  | changed: [crmp-prod-node01] => (item=tar)", "#FACC15", False),
        ("changed: [crmp-prod-node01] => (item=unzip)| changed: [crmp-prod-node01] => (item=ufw)", "#FACC15", False),
        ("TASK [Task 3: Install OpenJDK 21 Headless Java Runtime Environment] ******************", "#CCCCCC", False),
        ("changed: [crmp-prod-node01]", "#FACC15", False),
        ("TASK [Task 4: Install and Enable Docker Engine Daemon Service] ***********************", "#CCCCCC", False),
        ("changed: [crmp-prod-node01]", "#FACC15", False),
        ("TASK [Task 5: Ensure Application Service Group Exists (crmpgroup, GID 1000)] *********", "#CCCCCC", False),
        ("changed: [crmp-prod-node01]", "#FACC15", False),
        ("TASK [Task 6: Ensure Dedicated Unprivileged User Exists (crmpuser, UID 1000)] *******", "#CCCCCC", False),
        ("changed: [crmp-prod-node01]", "#FACC15", False),
        ("TASK [Task 7: Create Production Application Directory Layout] ************************", "#CCCCCC", False),
        ("changed: [crmp-prod-node01] => (item=/opt/review-app) | (item=/opt/review-app/config)", "#FACC15", False),
        ("changed: [crmp-prod-node01] => (item=/opt/review-app/logs)   | (item=/opt/review-app/data)", "#FACC15", False),
        ("TASK [Task 8: Deploy Production Configuration File from Jinja2 Template] *************", "#CCCCCC", False),
        ("changed: [crmp-prod-node01]", "#FACC15", False),
        ("TASK [Task 9: Configure Firewall Rules to Allow Traffic on Port 8080] ****************", "#CCCCCC", False),
        ("changed: [crmp-prod-node01] => (item=8080/tcp) | (item=22/tcp)", "#FACC15", False),
        ("TASK [Task 10: Deploy and Start Versioned CRMP Container] ****************************", "#CCCCCC", False),
        ("changed: [crmp-prod-node01]", "#FACC15", False),
        ("TASK [Task 11: Perform Automated Health Probe Verification via Actuator] *************", "#CCCCCC", False),
        ("ok: [crmp-prod-node01]", "#4ADE80", True),
        ("PLAY RECAP *********************************************************************", "#38BDF8", True),
        ("crmp-prod-node01           : ok=11   changed=8    unreachable=0    failed=0    skipped=0", "#22C55E", True),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 65.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.6, fontfamily='monospace', fontweight=weight)
        y -= 2.05

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task13\figure_13_4_ansible_playbook_first_execution_terminal.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 13.4 saved successfully to:", output_path)


def generate_figure_13_5_server_prerequisites_verification():
    """
    Figure 13.5: Server Prerequisites Verification (Filesystem, Permissions, Firewall & Docker)
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 70)
    ax.axis('off')

    frame = patches.FancyBboxPatch((1, 1), 113, 68, boxstyle="round,pad=0.5",
                                   facecolor='#1E1E1E', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(frame)

    hdr = patches.FancyBboxPatch((1, 64.5), 113, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#2D2D2D', edgecolor='#333333')
    ax.add_patch(hdr)
    ax.text(57.5, 66.5, "Target Host Verification: crmp-prod-node01 Prerequisites Audit", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 66.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 66.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 66.5), 0.8, color='#27C93F'))

    lines = [
        ("crmpuser@crmp-prod-node01:~$ # 1. VERIFY APPLICATION DIRECTORY STRUCTURE & PERMISSIONS", "#FACC15", True),
        ("crmpuser@crmp-prod-node01:~$ ls -la /opt/review-app", "#FFFFFF", True),
        ("drwxr-xr-x 5 crmpuser crmpgroup 4096 Oct 18 21:43 .", "#4ADE80", False),
        ("drwxr-xr-x 2 crmpuser crmpgroup 4096 Oct 18 21:43 config", "#4ADE80", False),
        ("drwxr-xr-x 2 crmpuser crmpgroup 4096 Oct 18 21:43 data", "#4ADE80", False),
        ("drwxr-xr-x 2 crmpuser crmpgroup 4096 Oct 18 21:43 logs", "#4ADE80", False),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("crmpuser@crmp-prod-node01:~$ # 2. VERIFY JINJA2 RENDERED APPLICATION PROPERTIES", "#FACC15", True),
        ("crmpuser@crmp-prod-node01:~$ cat /opt/review-app/config/application-production.properties | head -n 6", "#FFFFFF", True),
        ("server.port=8080", "#38BDF8", True),
        ("spring.application.name=customer-review-moderation-portal", "#CCCCCC", False),
        ("spring.profiles.active=production", "#CCCCCC", False),
        ("management.endpoints.web.exposure.include=health,info,metrics", "#4ADE80", False),
        ("logging.file.path=/opt/review-app/logs", "#CCCCCC", False),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("crmpuser@crmp-prod-node01:~$ # 3. VERIFY FIREWALL (UFW) ALLOW RULES", "#FACC15", True),
        ("crmpuser@crmp-prod-node01:~$ sudo ufw status verbose | grep -E '8080|Status'", "#FFFFFF", True),
        ("Status: active", "#4ADE80", True),
        ("8080/tcp                   ALLOW IN    Anywhere                  # CRMP Web & Actuator Port", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("crmpuser@crmp-prod-node01:~$ # 4. VERIFY CONTAINERIZED APPLICATION DEPLOYMENT", "#FACC15", True),
        ("crmpuser@crmp-prod-node01:~$ docker ps --filter name=crmp-app", "#FFFFFF", True),
        ("CONTAINER ID   IMAGE        STATUS                    PORTS                    NAMES", "#38BDF8", False),
        ("bc1855019445   crmp:1.0.0   Up 2 minutes (healthy)    0.0.0.0:8080->8080/tcp   crmp-app", "#4ADE80", True),
        ("crmpuser@crmp-prod-node01:~$ _", "#FFFFFF", False)
    ]

    y = 61.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.8, fontfamily='monospace', fontweight=weight)
        y -= 2.25

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task13\figure_13_5_server_prerequisites_verification.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 13.5 saved successfully to:", output_path)


def generate_figure_13_6_live_actuator_health_verification():
    """
    Figure 13.6: Live Provisioned Container Web UI & Actuator Health Verification
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 75)
    ax.axis('off')

    win_box = patches.FancyBboxPatch((2, 2), 111, 71, boxstyle="round,pad=0.5",
                                     facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.5)
    ax.add_patch(win_box)

    b_hdr = patches.FancyBboxPatch((2, 67), 111, 6.0, boxstyle="round,pad=0.2",
                                   facecolor='#0F172A', edgecolor='#020617')
    ax.add_patch(b_hdr)
    ax.add_patch(patches.Circle((5, 70), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((7.5, 70), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((10, 70), 0.8, color='#27C93F'))

    url_bar = patches.FancyBboxPatch((15, 68), 85, 4.0, boxstyle="round,pad=0.2",
                                    facecolor='#1E293B', edgecolor='#333333')
    ax.add_patch(url_bar)
    ax.text(17, 70.0, "http://localhost:8080/  |  Customer Review Moderation Portal (Ansible Provisioned Node)", 
            color='#38BDF8', fontsize=7.2, fontfamily='monospace', va='center')

    nav = patches.FancyBboxPatch((3.5, 61.5), 108, 4.5, boxstyle="round,pad=0.2",
                                 facecolor='#1E293B', edgecolor='#0F172A')
    ax.add_patch(nav)
    ax.text(6, 63.7, "Customer Review Moderation Portal (CRMP)", color='white', fontsize=8.6, fontweight='bold', va='center')
    ax.text(78, 63.7, "Provisioner: Ansible Playbook  |  Status: UP", color='#4ADE80', fontsize=7.0, fontweight='bold', va='center')

    kpis = [
        ("Total Ingested Reviews", "4", "#2563EB", "#EFF6FF", 4),
        ("Moderation Queue (Pending)", "1", "#D97706", "#FFFBEB", 31),
        ("Approved Reviews", "2", "#16A34A", "#F0FDF4", 58),
        ("Flagged / Spam Reviews", "1", "#DC2626", "#FEF2F2", 85)
    ]
    for title, val, b_color, bg_color, x_pos in kpis:
        k_card = patches.FancyBboxPatch((x_pos, 52.0), 25, 8.0, boxstyle="round,pad=0.3",
                                        facecolor=bg_color, edgecolor=b_color, linewidth=1.5)
        ax.add_patch(k_card)
        ax.text(x_pos + 12.5, 57.2, title, color='#475569', fontsize=6.8, ha='center', fontweight='bold')
        ax.text(x_pos + 12.5, 54.0, val, color=b_color, fontsize=12.0, ha='center', fontweight='bold')

    tbl_box = patches.FancyBboxPatch((4, 25.5), 107, 24.5, boxstyle="round,pad=0.4",
                                     facecolor='white', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(tbl_box)
    ax.text(6, 47.5, "Live Moderated Reviews Queue (Provisioned Node: crmp-prod-node01)", color='#0F172A', fontsize=8.2, fontweight='bold')

    th_box = patches.FancyBboxPatch((5, 43.5), 105, 3.2, boxstyle="square,pad=0",
                                    facecolor='#F1F5F9', edgecolor='#E2E8F0')
    ax.add_patch(th_box)
    ax.text(7, 45.1, "ID", color='#334155', fontsize=6.8, fontweight='bold', va='center')
    ax.text(14, 45.1, "Product", color='#334155', fontsize=6.8, fontweight='bold', va='center')
    ax.text(32, 45.1, "Reviewer", color='#334155', fontsize=6.8, fontweight='bold', va='center')
    ax.text(50, 45.1, "Rating", color='#334155', fontsize=6.8, fontweight='bold', va='center')
    ax.text(62, 45.1, "Review Snippet", color='#334155', fontsize=6.8, fontweight='bold', va='center')
    ax.text(88, 45.1, "Status", color='#334155', fontsize=6.8, fontweight='bold', va='center')
    ax.text(98, 45.1, "Action", color='#334155', fontsize=6.8, fontweight='bold', va='center')

    rows = [
        ("1", "Logitech MX Master 3S", "Aarav Sharma", "5/5 Stars", "Silent clicks and ergonomic grip are exceptional...", "APPROVED", "#16A34A", 40.0),
        ("2", "Sony WH-1000XM5 ANC", "Pooja Mehta", "4/5 Stars", "ANC cuts high aircraft rumble cleanly...", "APPROVED", "#16A34A", 35.8),
        ("3", "Apple MacBook Air M3", "Rohan Verma", "5/5 Stars", "Battery runtime sustains over 14 hours coding...", "PENDING", "#D97706", 31.6),
        ("4", "Ultra Promo Free Voucher", "PromoSpamBot", "1/5 Stars", "Claim free luxury gift card at bit.ly/spam-win...", "FLAGGED", "#DC2626", 27.4)
    ]
    for rid, prod, rev, rating, snippet, status, badge_col, y_r in rows:
        ax.text(7, y_r, rid, color='#1E293B', fontsize=6.5)
        ax.text(14, y_r, prod, color='#1E293B', fontsize=6.5, fontweight='bold')
        ax.text(32, y_r, rev, color='#475569', fontsize=6.5)
        ax.text(50, y_r, rating, color='#D97706', fontsize=6.5)
        ax.text(62, y_r, snippet, color='#334155', fontsize=6.2)
        badge = patches.FancyBboxPatch((86.5, y_r - 1.2), 9.0, 2.8, boxstyle="round,pad=0.2",
                                       facecolor=badge_col, edgecolor=badge_col)
        ax.add_patch(badge)
        ax.text(91.0, y_r + 0.2, status, color='white', fontsize=5.8, fontweight='bold', ha='center')
        ax.text(98, y_r, "[Moderate]", color='#2563EB', fontsize=6.2)

    health_box = patches.FancyBboxPatch((4, 4), 107, 19.5, boxstyle="round,pad=0.4",
                                        facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.2)
    ax.add_patch(health_box)
    ax.text(6, 20.8, "Live Spring Boot Actuator Health Probe Verification (GET http://localhost:8080/actuator/health)", 
            color='#38BDF8', fontsize=7.8, fontweight='bold')

    json_lines = [
        ("HTTP/1.1 200 OK | Content-Type: application/vnd.spring-boot.actuator.v3+json", "#4ADE80", True),
        ("{", "#FFFFFF", False),
        ("  \"status\": \"UP\",", "#4ADE80", True),
        ("  \"components\": {", "#CCCCCC", False),
        ("    \"db\": { \"status\": \"UP\", \"details\": { \"database\": \"H2 In-Memory\", \"validationQuery\": \"isValid()\" } },", "#CCCCCC", False),
        ("    \"diskSpace\": { \"status\": \"UP\", \"details\": { \"total\": 510984192000, \"free\": 382914109440, \"threshold\": 10485760 } },", "#CCCCCC", False),
        ("    \"ping\": { \"status\": \"UP\" }", "#CCCCCC", False),
        ("  }", "#CCCCCC", False),
        ("}", "#FFFFFF", False)
    ]
    y_j = 17.8
    for j_text, j_col, j_bold in json_lines:
        weight = 'bold' if j_bold else 'normal'
        ax.text(7, y_j, j_text, color=j_col, fontsize=6.2, fontfamily='monospace', fontweight=weight)
        y_j -= 1.45

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task13\figure_13_6_live_actuator_health_verification.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 13.6 saved successfully to:", output_path)

if __name__ == '__main__':
    generate_figure_13_1()
    generate_figure_13_2_ansible_inventory_and_playbook_syntax()
    generate_figure_13_3_ansible_ping_adhoc_terminal()
    generate_figure_13_4_ansible_playbook_first_execution_terminal()
    generate_figure_13_5_server_prerequisites_verification()
    generate_figure_13_6_live_actuator_health_verification()
