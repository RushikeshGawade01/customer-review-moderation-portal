import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task2", exist_ok=True)

def generate_figure_2_1():
    """
    Figure 2.1: Kanban Task Board & Sprint Execution Flow for CRMP
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 65)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 57), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 60.2, "CUSTOMER REVIEW MODERATION PORTAL (CRMP) - KANBAN TASK BOARD & SPRINT PROGRESSION", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    columns = [
        {"name": "1. PRODUCT BACKLOG", "sub": "Unscheduled Items", "wip": "Total: 15 Tasks", "x": 3, "color": "#475569", "bg": "#F8FAFC"},
        {"name": "2. SPRINT TO DO", "sub": "Sprint 1 & 2 Ready", "wip": "WIP: 3", "x": 25.5, "color": "#2563EB", "bg": "#EFF6FF"},
        {"name": "3. IN PROGRESS", "sub": "Active Development", "wip": "WIP: 2 (Cap)", "x": 48, "color": "#D97706", "bg": "#FFFBEB"},
        {"name": "4. CI TESTING / QA", "sub": "Automated Selenium Gate", "wip": "WIP: 2 (Cap)", "x": 70.5, "color": "#7C3AED", "bg": "#FAF5FF"},
        {"name": "5. DONE / RELEASED", "sub": "DoD Verified & Deployed", "wip": "Target: v1.0.0", "x": 93, "color": "#059669", "bg": "#ECFDF5"}
    ]

    col_width = 20
    for col in columns:
        # Header Box
        hdr = patches.FancyBboxPatch((col["x"], 48.5), col_width, 6.8, boxstyle="round,pad=0.4",
                                     facecolor=col["color"], edgecolor=col["color"], linewidth=1.2)
        ax.add_patch(hdr)
        ax.text(col["x"] + col_width/2, 53.2, col["name"], ha='center', va='center', color='white', fontsize=8.5, fontweight='bold')
        ax.text(col["x"] + col_width/2, 50.2, f"{col['sub']} | {col['wip']}", ha='center', va='center', color='#E2E8F0', fontsize=7.2)

        # Body Background
        body = patches.FancyBboxPatch((col["x"], 3), col_width, 44.5, boxstyle="round,pad=0.4",
                                      facecolor=col["bg"], edgecolor='#CBD5E1', linewidth=1.2)
        ax.add_patch(body)

    # Helper function to draw cards
    def draw_card(x, y, card_id, title, pts, prio, prio_color, assignee, status_color="#64748B"):
        c_box = patches.FancyBboxPatch((x + 1, y), 18, 9.2, boxstyle="round,pad=0.4",
                                       facecolor='white', edgecolor='#94A3B8', linewidth=1.2)
        ax.add_patch(c_box)
        # ID and Priority Pill
        ax.text(x + 2, y + 7.2, card_id, fontsize=7.5, fontweight='bold', color='#1E293B')
        pill = patches.FancyBboxPatch((x + 11.5, y + 6.3), 6.5, 2.2, boxstyle="round,pad=0.2",
                                      facecolor=prio_color, edgecolor=prio_color)
        ax.add_patch(pill)
        ax.text(x + 14.75, y + 7.4, prio, fontsize=6.2, fontweight='bold', color='white', ha='center', va='center')

        # Title
        ax.text(x + 2, y + 4.5, title, fontsize=7.2, color='#334155', linespacing=1.2)

        # Bottom info (Story points and assignee)
        ax.plot([x + 1.8, x + 18.2], [y + 2.4, y + 2.4], color='#E2E8F0', linewidth=0.8)
        ax.text(x + 2, y + 1.2, f"SP: {pts}", fontsize=6.8, fontweight='bold', color='#0284C7')
        ax.text(x + 18, y + 1.2, assignee, fontsize=6.5, color='#64748B', ha='right')

    # Column 1 Cards (Backlog)
    draw_card(3, 36, "TASK-11", "Docker Multi-stage\nContainer Image", "5", "P1-Must", "#DC2626", "Rushikesh G.")
    draw_card(3, 25, "TASK-12", "Automated Jenkins-\nDocker CD Pipeline", "8", "P1-Must", "#DC2626", "Rushikesh G.")
    draw_card(3, 14, "TASK-13", "Ansible Configuration\nPlaybook & Inventory", "5", "P2-Should", "#D97706", "Rushikesh G.")
    draw_card(3, 4,  "TASK-14", "Automated Provisioning\n& Idempotency Proof", "5", "P2-Should", "#D97706", "Rushikesh G.")

    # Column 2 Cards (Sprint To-Do)
    draw_card(25.5, 36, "TASK-04", "Git Repo Setup &\nSkeleton Commit", "3", "P1-Must", "#DC2626", "Rushikesh G.")
    draw_card(25.5, 25, "TASK-05", "Review Ingestion on\nFeature Branch (PR)", "5", "P1-Must", "#DC2626", "Rushikesh G.")
    draw_card(25.5, 14, "TASK-06", "Review Queue, Conflict\nResolution & v1.0.0", "8", "P1-Must", "#DC2626", "Rushikesh G.")

    # Column 3 Cards (In Progress)
    draw_card(48, 36, "TASK-03", "4-Tier Architecture &\nLocal Setup Baseline", "5", "P1-Must", "#DC2626", "Rushikesh G.")
    draw_card(48, 25, "US-02", "Review Status Workflow\nState Transitions", "5", "P1-Must", "#DC2626", "Rushikesh G.")

    # Column 4 Cards (CI Testing / QA)
    draw_card(70.5, 36, "TASK-09", "Selenium WebDriver\nHeadless Test Suite", "5", "P1-Must", "#DC2626", "Rushikesh G.")
    draw_card(70.5, 25, "TASK-10", "Jenkins Quality Gate\nDefect Abort Check", "5", "P1-Must", "#DC2626", "Rushikesh G.")

    # Column 5 Cards (Done / Released)
    draw_card(93, 36, "TASK-01", "Problem Definition &\n15-Task Scope Freeze", "3", "P1-Must", "#059669", "Rushikesh G.")
    draw_card(93, 25, "TASK-02", "Agile Backlog, User\nStories & DoD Specs", "5", "P1-Must", "#059669", "Rushikesh G.")
    draw_card(93, 14, "ARCH-01", "H2 Embedded In-Memory\nPersistence Schema", "3", "P1-Must", "#059669", "Rushikesh G.")

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task2\figure_2_1_kanban_board.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 2.1 generated at: {output_path}")

def generate_figure_2_2():
    """
    Figure 2.2: Comprehensive End-to-End DevOps Lifecycle (Dev to Ops)
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 70)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 62), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 65.2, "CUSTOMER REVIEW MODERATION PORTAL - END-TO-END DEVOPS LIFECYCLE (DEV TO OPS)", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    # Development Phases (Left side)
    dev_box = patches.FancyBboxPatch((3, 24), 52, 35, boxstyle="round,pad=0.6",
                                     facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=2)
    ax.add_patch(dev_box)
    ax.text(29, 56, "CONTINUOUS DEVELOPMENT (DEV)", ha='center', va='center', color='#1E40AF', fontsize=11, fontweight='bold')

    dev_stages = [
        {"title": "1. PLAN", "tool": "Jira / Markdown", "desc": "User Stories, Backlog,\nDefinition of Done (DoD),\n15-Task Sprint Roadmap", "x": 5, "y": 27, "w": 23, "h": 26, "c": "#1E3A8A", "bg": "#DBEAFE"},
        {"title": "2. CODE & SCM", "tool": "Git 2.51 / GitHub", "desc": "Feature Branching (feature/*),\nConventional Commits,\nPull Request Reviews", "x": 30, "y": 41, "w": 23, "h": 12, "c": "#065F46", "bg": "#D1FAE5"},
        {"title": "3. BUILD", "tool": "Apache Maven / Java 21", "desc": "Maven Wrapper (mvnw),\nDependency Resolution,\nBytecode Compilation", "x": 30, "y": 27, "w": 23, "h": 12, "c": "#92400E", "bg": "#FEF3C7"}
    ]

    for st in dev_stages:
        box = patches.FancyBboxPatch((st["x"], st["y"]), st["w"], st["h"], boxstyle="round,pad=0.4",
                                     facecolor=st["bg"], edgecolor=st["c"], linewidth=1.5)
        ax.add_patch(box)
        ax.text(st["x"] + st["w"]/2, st["y"] + st["h"] - 2.8, st["title"], ha='center', va='center', color=st["c"], fontsize=9, fontweight='bold')
        ax.text(st["x"] + st["w"]/2, st["y"] + st["h"] - 5.5, f"[{st['tool']}]", ha='center', va='center', color='#334155', fontsize=7.2, fontweight='bold')
        ax.text(st["x"] + st["w"]/2, st["y"] + (st["h"] - 7)/2, st["desc"], ha='center', va='center', color='#1E293B', fontsize=7.2, linespacing=1.2)

    # Operations Phases (Right side)
    ops_box = patches.FancyBboxPatch((60, 24), 52, 35, boxstyle="round,pad=0.6",
                                     facecolor='#ECFDF5', edgecolor='#10B981', linewidth=2)
    ax.add_patch(ops_box)
    ax.text(86, 56, "CONTINUOUS OPERATIONS (OPS)", ha='center', va='center', color='#065F46', fontsize=11, fontweight='bold')

    ops_stages = [
        {"title": "6. DEPLOY (CD)", "tool": "Docker Multi-Stage", "desc": "Temurin JRE Runtime,\nContainer Port 8080 Mapping,\nreview-app:v1.0.0 Container", "x": 62, "y": 41, "w": 23, "h": 12, "c": "#0369A1", "bg": "#E0F2FE"},
        {"title": "7. OPERATE & CM", "tool": "Ansible Automation", "desc": "hosts.ini & playbook.yml,\nDirectory & Port Config,\nIdempotency (changed=0)", "x": 62, "y": 27, "w": 23, "h": 12, "c": "#581C87", "bg": "#EDE9FE"},
        {"title": "8. MONITOR & PROBE", "tool": "Spring Boot Actuator", "desc": "HTTP GET /actuator/health,\nReal-Time Telemetry UP,\nSummary Metrics Dashboard", "x": 87, "y": 27, "w": 23, "h": 26, "c": "#065F46", "bg": "#DCFCE7"}
    ]

    for st in ops_stages:
        box = patches.FancyBboxPatch((st["x"], st["y"]), st["w"], st["h"], boxstyle="round,pad=0.4",
                                     facecolor=st["bg"], edgecolor=st["c"], linewidth=1.5)
        ax.add_patch(box)
        ax.text(st["x"] + st["w"]/2, st["y"] + st["h"] - 2.8, st["title"], ha='center', va='center', color=st["c"], fontsize=9, fontweight='bold')
        ax.text(st["x"] + st["w"]/2, st["y"] + st["h"] - 5.5, f"[{st['tool']}]", ha='center', va='center', color='#334155', fontsize=7.2, fontweight='bold')
        ax.text(st["x"] + st["w"]/2, st["y"] + (st["h"] - 7)/2, st["desc"], ha='center', va='center', color='#1E293B', fontsize=7.2, linespacing=1.2)

    # Middle Bridge: CI Quality Gate (Test & Release)
    bridge_box = patches.FancyBboxPatch((46, 12), 23, 10, boxstyle="round,pad=0.4",
                                        facecolor='#FFF7ED', edgecolor='#EA580C', linewidth=2)
    ax.add_patch(bridge_box)
    ax.text(57.5, 19.2, "4. TEST & 5. RELEASE GATE", ha='center', va='center', color='#C2410C', fontsize=8.8, fontweight='bold')
    ax.text(57.5, 16.5, "[Selenium WebDriver + Jenkins Pipeline]", ha='center', va='center', color='#334155', fontsize=7.2, fontweight='bold')
    ax.text(57.5, 14.0, "Headless CI Gate | Intentional Defect Halt | Tag v1.0.0", ha='center', va='center', color='#7C2D12', fontsize=6.8)

    # Connective Flow Arrows
    # Plan -> Code
    ax.annotate('', xy=(30, 47), xytext=(28, 47),
                arrowprops=dict(facecolor='#1E40AF', edgecolor='#1E40AF', width=2, headwidth=6))
    # Code -> Build
    ax.annotate('', xy=(41.5, 39), xytext=(41.5, 41),
                arrowprops=dict(facecolor='#1E40AF', edgecolor='#1E40AF', width=2, headwidth=6))
    # Build -> Test/Release Gate
    ax.annotate('', xy=(47, 22), xytext=(41.5, 27),
                arrowprops=dict(facecolor='#EA580C', edgecolor='#EA580C', width=2, headwidth=6))
    # Test/Release Gate -> Deploy
    ax.annotate('', xy=(73.5, 41), xytext=(68, 22),
                arrowprops=dict(facecolor='#0369A1', edgecolor='#0369A1', width=2, headwidth=6))
    # Deploy -> Operate
    ax.annotate('', xy=(73.5, 39), xytext=(73.5, 41),
                arrowprops=dict(facecolor='#065F46', edgecolor='#065F46', width=2, headwidth=6))
    # Operate -> Monitor
    ax.annotate('', xy=(87, 33), xytext=(85, 33),
                arrowprops=dict(facecolor='#065F46', edgecolor='#065F46', width=2, headwidth=6))

    # Bottom Continuous Feedback Loop Arrow (Monitor -> Plan)
    ax.annotate('', xy=(16, 24), xytext=(98, 24),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.18", 
                                color='#BE123C', linewidth=2.5, mutation_scale=15))
    ax.text(57.5, 3.8, "CONTINUOUS FEEDBACK LOOP: Health Telemetry, Defect Reports, User Analytics & SCM Issues -> Plan Next Sprint", 
            ha='center', va='center', color='#BE123C', fontsize=8.5, fontweight='bold')

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task2\figure_2_2_devops_lifecycle.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 2.2 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_2_1()
    generate_figure_2_2()
