import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task1", exist_ok=True)

def generate_figure_1_1():
    """
    Figure 1.1: Architectural Context and Review Moderation Workflow
    """
    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Color Palette
    c_blue = '#1E3A8A'     # Deep blue
    c_light_blue = '#DBEAFE' # Light blue fill
    c_border_blue = '#3B82F6'
    c_green = '#065F46'
    c_light_green = '#D1FAE5'
    c_border_green = '#10B981'
    c_amber = '#92400E'
    c_light_amber = '#FEF3C7'
    c_border_amber = '#F59E0B'
    c_red = '#991B1B'
    c_light_red = '#FEE2E2'
    c_border_red = '#EF4444'
    c_purple = '#5B21B6'
    c_light_purple = '#EDE9FE'
    c_border_purple = '#8B5CF6'
    c_dark = '#1F2937'

    # Title Banner inside diagram
    title_box = patches.FancyBboxPatch((2, 52), 101, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(52.5, 55.2, "CUSTOMER REVIEW MODERATION PORTAL (CRMP) - SYSTEM CONTEXT & DATA FLOW", 
            ha='center', va='center', color='white', fontsize=12, fontweight='bold', fontfamily='sans-serif')

    # Component 1: End Customer (Review Ingestion)
    box_ingest = patches.FancyBboxPatch((3, 28), 22, 20, boxstyle="round,pad=0.6",
                                        facecolor=c_light_blue, edgecolor=c_border_blue, linewidth=2)
    ax.add_patch(box_ingest)
    ax.text(14, 44, "1. Ingestion Layer", ha='center', va='center', color=c_blue, fontsize=11, fontweight='bold')
    ax.text(14, 38, "- End Shoppers / Users\n- Star Rating (1 to 5)\n- Review Title & Body\n- Product ID & Timestamp\n- Input Validation Gate", 
            ha='center', va='center', color=c_dark, fontsize=8.5)

    # Arrow 1 -> 2
    ax.annotate('', xy=(29, 38), xytext=(25, 38),
                arrowprops=dict(facecolor=c_border_blue, edgecolor=c_border_blue, width=2.5, headwidth=8))
    ax.text(27, 40.5, "HTTP POST\n/reviews/submit", ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_blue)

    # Component 2: Core Spring Boot Application & Queue
    box_core = patches.FancyBboxPatch((30, 20), 38, 28, boxstyle="round,pad=0.6",
                                      facecolor='#F8FAFC', edgecolor='#64748B', linewidth=2)
    ax.add_patch(box_core)
    ax.text(49, 44.5, "2. Core Application & State Engine (Spring Boot)", ha='center', va='center', color='#0F172A', fontsize=11, fontweight='bold')

    # Sub-boxes inside Core
    box_queue = patches.FancyBboxPatch((32, 33), 34, 8, boxstyle="round,pad=0.4",
                                       facecolor=c_light_amber, edgecolor=c_border_amber, linewidth=1.5)
    ax.add_patch(box_queue)
    ax.text(49, 37, "Pending Moderation Queue\n(State: PENDING | Strict In-Memory H2 DB)", ha='center', va='center', color=c_amber, fontsize=8.5, fontweight='bold')

    box_rules = patches.FancyBboxPatch((32, 22), 34, 8, boxstyle="round,pad=0.4",
                                       facecolor=c_light_purple, edgecolor=c_border_purple, linewidth=1.5)
    ax.add_patch(box_rules)
    ax.text(49, 26, "Moderation State Machine & Validation Engine\n(Profanity Check | Length Limits | Status Transitions)", ha='center', va='center', color=c_purple, fontsize=8.5, fontweight='bold')

    # Arrow 2 -> 3 (Moderator Action)
    ax.annotate('', xy=(72, 38), xytext=(68, 38),
                arrowprops=dict(facecolor='#64748B', edgecolor='#64748B', width=2.5, headwidth=8))
    ax.text(70, 40.5, "Triage / Decision\nAction", ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_dark)

    # Component 3: Moderation Outcomes
    box_approved = patches.FancyBboxPatch((73, 38), 29, 10, boxstyle="round,pad=0.4",
                                          facecolor=c_light_green, edgecolor=c_border_green, linewidth=1.8)
    ax.add_patch(box_approved)
    ax.text(87.5, 44.5, "APPROVED (Status: APPROVED)", ha='center', va='center', color=c_green, fontsize=9.5, fontweight='bold')
    ax.text(87.5, 40.5, "Published to Public Store & Product Ratings", ha='center', va='center', color=c_dark, fontsize=8)

    box_flagged = patches.FancyBboxPatch((73, 26), 29, 9, boxstyle="round,pad=0.4",
                                         facecolor=c_light_amber, edgecolor=c_border_amber, linewidth=1.8)
    ax.add_patch(box_flagged)
    ax.text(87.5, 31.8, "FLAGGED (Status: FLAGGED)", ha='center', va='center', color=c_amber, fontsize=9.5, fontweight='bold')
    ax.text(87.5, 28.2, "Escalated for Compliance / Policy Audit", ha='center', va='center', color=c_dark, fontsize=8)

    box_rejected = patches.FancyBboxPatch((73, 14), 29, 9, boxstyle="round,pad=0.4",
                                          facecolor=c_light_red, edgecolor=c_border_red, linewidth=1.8)
    ax.add_patch(box_rejected)
    ax.text(87.5, 19.8, "REJECTED (Status: REJECTED)", ha='center', va='center', color=c_red, fontsize=9.5, fontweight='bold')
    ax.text(87.5, 16.2, "Quarantined Spam / Abusive Content / Sabotage", ha='center', va='center', color=c_dark, fontsize=8)

    # Bottom Monitoring & Telemetry Banner
    box_telemetry = patches.FancyBboxPatch((3, 3), 99, 8.5, boxstyle="round,pad=0.5",
                                           facecolor='#F1F5F9', edgecolor='#94A3B8', linewidth=1.5)
    ax.add_patch(box_telemetry)
    ax.text(52.5, 8.5, "3. Real-Time Telemetry, Governance & DevOps Readiness Gate", 
            ha='center', va='center', color='#0F172A', fontsize=10.5, fontweight='bold')
    ax.text(52.5, 5.0, "Summary KPI Dashboard (Total, Pending, Approved, Flagged, Avg Rating) | Actuator Health Probe (/actuator/health -> {\"status\":\"UP\"})", 
            ha='center', va='center', color='#334155', fontsize=8.5)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task1\figure_1_1_context_architecture.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 1.1 generated at: {output_path}")

def generate_figure_1_2():
    """
    Figure 1.2: 15-Task End-to-End DevOps Lifecycle Roadmap
    """
    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 70)
    ax.axis('off')

    # Title Banner
    title_box = patches.FancyBboxPatch((2, 62), 101, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(52.5, 65.2, "15-TASK DEVOPS CONTINUOUS LIFECYCLE & QUALITY GATE BLUEPRINT", 
            ha='center', va='center', color='white', fontsize=12, fontweight='bold', fontfamily='sans-serif')

    phases = [
        {"num": "PHASE 1", "title": "Requirements & Plan", "tasks": "Task 1: Problem Definition & Scope\nTask 2: Agile Backlog & Kanban\nTask 3: Architecture & Setup", "color": "#1E40AF", "fill": "#EFF6FF", "border": "#3B82F6", "x": 3},
        {"num": "PHASE 2", "title": "Source Control & Dev", "tasks": "Task 4: Git Repo & Skeleton Init\nTask 5: Branching & Pull Requests\nTask 6: MVP Release & Merge Conflict", "color": "#065F46", "fill": "#ECFDF5", "border": "#10B981", "x": 23.5},
        {"num": "PHASE 3", "title": "Continuous Integration", "tasks": "Task 7: Jenkins CI Job & Maven\nTask 8: Jenkinsfile Pipeline-as-Code\nTask 9: Selenium Local WebDriver", "color": "#92400E", "fill": "#FFFBEB", "border": "#F59E0B", "x": 44},
        {"num": "PHASE 4", "title": "Quality Gate & Docker", "tasks": "Task 10: Jenkins Quality Gate Halt\nTask 11: Multi-stage Dockerfile\nTask 12: Automated Docker CD", "color": "#7C2D12", "fill": "#FFF7ED", "border": "#EA580C", "x": 64.5},
        {"num": "PHASE 5", "title": "Config Mgmt & Release", "tasks": "Task 13: Ansible Config Playbook\nTask 14: Idempotency & Rollback\nTask 15: End-to-End Release & Viva", "color": "#581C87", "fill": "#FAF5FF", "border": "#A855F7", "x": 85}
    ]

    for p in phases:
        box = patches.FancyBboxPatch((p["x"], 20), 17, 39, boxstyle="round,pad=0.5",
                                     facecolor=p["fill"], edgecolor=p["border"], linewidth=2)
        ax.add_patch(box)
        
        # Phase header
        ax.text(p["x"] + 8.5, 55, p["num"], ha='center', va='center', color=p["color"], fontsize=10, fontweight='bold')
        ax.text(p["x"] + 8.5, 51.5, p["title"], ha='center', va='center', color='#1E293B', fontsize=9, fontweight='bold')
        
        # Separator line
        ax.plot([p["x"] + 1, p["x"] + 16], [48.5, 48.5], color=p["border"], linewidth=1.2)
        
        # Tasks description
        ax.text(p["x"] + 8.5, 33.5, p["tasks"], ha='center', va='center', color='#334155', fontsize=8.2, linespacing=1.6)

    # Arrows between phases
    arrow_xs = [20.2, 40.7, 61.2, 81.7]
    for ax_x in arrow_xs:
        ax.annotate('', xy=(ax_x + 3.0, 39.5), xytext=(ax_x, 39.5),
                    arrowprops=dict(facecolor='#475569', edgecolor='#475569', width=2.5, headwidth=7))

    # Bottom Foundation Bar
    found_box = patches.FancyBboxPatch((3, 3), 99, 13, boxstyle="round,pad=0.5",
                                       facecolor='#F8FAFC', edgecolor='#64748B', linewidth=1.5)
    ax.add_patch(found_box)
    ax.text(52.5, 12.5, "FOUNDATIONAL DEVOPS ASSURANCE & REPRODUCIBILITY GUARANTEES", 
            ha='center', va='center', color='#0F172A', fontsize=10.5, fontweight='bold')
    ax.text(52.5, 8.5, "Java 21 LTS | Spring Boot 3.x | Embedded In-Memory H2 DB | Headless Selenium WebDriver 4.x | Docker Containerization | Ansible Idempotency", 
            ha='center', va='center', color='#2563EB', fontsize=8.5, fontweight='bold')
    ax.text(52.5, 5.2, "Student: Rushikesh Gawade (Roll No: 23102A0052) | Academic Evaluator: Dr. Snehal Andhare | Dept of Computer Engineering", 
            ha='center', va='center', color='#475569', fontsize=8)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task1\figure_1_2_devops_roadmap.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 1.2 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_1_1()
    generate_figure_1_2()
