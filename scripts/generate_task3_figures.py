import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task3", exist_ok=True)

def generate_figure_3_1():
    """
    Figure 3.1: Detailed Use-Case Diagram for Customer Review Moderation Portal
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 64), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 67.2, "USE-CASE MODEL - CUSTOMER REVIEW MODERATION PORTAL (CRMP)", 
            ha='center', va='center', color='white', fontsize=12, fontweight='bold', fontfamily='sans-serif')

    # System Boundary Box
    sys_box = patches.FancyBboxPatch((28, 4), 58, 57, boxstyle="round,pad=0.6",
                                     facecolor='#F8FAFC', edgecolor='#475569', linewidth=2, linestyle='--')
    ax.add_patch(sys_box)
    ax.text(57, 58.5, "SYSTEM BOUNDARY: Spring Boot 3.3.4 + Embedded H2 Database (Port 8080)", 
            ha='center', va='center', color='#1E293B', fontsize=9.5, fontweight='bold')

    # Actors (Left Side)
    # Actor 1: End Shopper
    act1_box = patches.FancyBboxPatch((3, 40), 20, 15, boxstyle="round,pad=0.5",
                                      facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.8)
    ax.add_patch(act1_box)
    ax.text(13, 51.5, "ACTOR: End Shopper", ha='center', va='center', color='#1E40AF', fontsize=9.2, fontweight='bold')
    ax.text(13, 45.5, "External Consumer\nSubmits authentic\nfeedback & ratings", ha='center', va='center', color='#334155', fontsize=8)

    # Actor 2: Content Moderator
    act2_box = patches.FancyBboxPatch((3, 12), 20, 20, boxstyle="round,pad=0.5",
                                      facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1.8)
    ax.add_patch(act2_box)
    ax.text(13, 27.5, "ACTOR: Content Moderator", ha='center', va='center', color='#92400E', fontsize=9.2, fontweight='bold')
    ax.text(13, 19.5, "Internal Operations\nTriages queue, evaluates\ncontent, executes status\ntransitions (Approve/Reject)", ha='center', va='center', color='#334155', fontsize=8)

    # Actors (Right Side)
    # Actor 3: Brand Merchant
    act3_box = patches.FancyBboxPatch((91, 40), 21, 15, boxstyle="round,pad=0.5",
                                      facecolor='#ECFDF5', edgecolor='#10B981', linewidth=1.8)
    ax.add_patch(act3_box)
    ax.text(101.5, 51.5, "ACTOR: Brand Merchant", ha='center', va='center', color='#065F46', fontsize=9.2, fontweight='bold')
    ax.text(101.5, 45.5, "Business Client\nMonitors product rating\n& sentiment analytics", ha='center', va='center', color='#334155', fontsize=8)

    # Actor 4: DevOps Engineer
    act4_box = patches.FancyBboxPatch((91, 12), 21, 20, boxstyle="round,pad=0.5",
                                      facecolor='#EDE9FE', edgecolor='#8B5CF6', linewidth=1.8)
    ax.add_patch(act4_box)
    act4_title = "ACTOR: DevOps Engineer"
    ax.text(101.5, 27.5, act4_title, ha='center', va='center', color='#5B21B6', fontsize=9.2, fontweight='bold')
    ax.text(101.5, 19.5, "Platform Operations\nAutomates CI/CD, runs\nheadless Selenium tests,\nprobes /actuator/health", ha='center', va='center', color='#334155', fontsize=8)

    # Use Cases (Ovals/Boxes inside System Boundary)
    use_cases = [
        {"id": "UC-01", "name": "Submit Product Review & Rating\n(POST /reviews/submit)", "y": 48, "c": "#2563EB", "bg": "#DBEAFE"},
        {"id": "UC-02", "name": "Search & Filter Review Queue\n(GET /reviews?query=&status=)", "y": 38, "c": "#D97706", "bg": "#FEF3C7"},
        {"id": "UC-03", "name": "Execute Status Transition\n(Approve | Reject | Flag)", "y": 28, "c": "#DC2626", "bg": "#FEE2E2"},
        {"id": "UC-04", "name": "View Real-Time KPI Dashboard\n(GET / or /dashboard)", "y": 18, "c": "#059669", "bg": "#D1FAE5"},
        {"id": "UC-05", "name": "Probe System Health & Liveness\n(GET /actuator/health)", "y": 8, "c": "#7C3AED", "bg": "#EDE9FE"}
    ]

    for uc in use_cases:
        box = patches.FancyBboxPatch((35, uc["y"]), 44, 7.5, boxstyle="round,pad=0.5",
                                     facecolor=uc["bg"], edgecolor=uc["c"], linewidth=1.5)
        ax.add_patch(box)
        ax.text(57, uc["y"] + 3.75, f"{uc['id']}: {uc['name']}", ha='center', va='center', color='#0F172A', fontsize=8.5, fontweight='bold')

    # Association Lines
    # End Shopper -> UC-01
    ax.annotate('', xy=(35, 51.75), xytext=(23, 48), arrowprops=dict(arrowstyle="-", color='#3B82F6', linewidth=1.5))
    # Content Moderator -> UC-02, UC-03
    ax.annotate('', xy=(35, 41.75), xytext=(23, 24), arrowprops=dict(arrowstyle="-", color='#F59E0B', linewidth=1.5))
    ax.annotate('', xy=(35, 31.75), xytext=(23, 24), arrowprops=dict(arrowstyle="-", color='#F59E0B', linewidth=1.5))
    # Brand Merchant -> UC-04
    ax.annotate('', xy=(79, 21.75), xytext=(91, 47), arrowprops=dict(arrowstyle="-", color='#10B981', linewidth=1.5))
    # DevOps Engineer -> UC-04, UC-05
    ax.annotate('', xy=(79, 21.75), xytext=(91, 23), arrowprops=dict(arrowstyle="-", color='#8B5CF6', linewidth=1.5))
    ax.annotate('', xy=(79, 11.75), xytext=(91, 23), arrowprops=dict(arrowstyle="-", color='#8B5CF6', linewidth=1.5))

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task3\figure_3_1_use_case_crmp.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 3.1 generated at: {output_path}")

def generate_figure_3_2():
    """
    Figure 3.2: 4-Tier Application Architecture Diagram for CRMP
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 64), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 67.2, "CUSTOMER REVIEW MODERATION PORTAL (CRMP) - 4-TIER APPLICATION ARCHITECTURE", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    tiers = [
        {
            "num": "TIER 1",
            "name": "PRESENTATION TIER",
            "tech": "Thymeleaf + HTML5 + Bootstrap 5.3 + Bootstrap Icons",
            "components": "- Responsive Navigation Bar & Global Brand Identity\n- Summary KPI Analytics Dashboard (index.html)\n- Review Directory & Moderation Queue Table (reviews.html)\n- Customer Review Ingestion Form (submit.html)\n- Distinct HTML Element IDs for Headless Selenium Targeting",
            "color": "#1E40AF", "bg": "#EFF6FF", "border": "#3B82F6", "y": 48.5, "h": 14
        },
        {
            "num": "TIER 2",
            "name": "CONTROLLER & INGESTION TIER",
            "tech": "Spring MVC REST & Web Controllers + Jakarta Validation",
            "components": "- DashboardController (Routes: /, /dashboard)\n- ReviewController (Routes: /reviews, /reviews/submit, /reviews/{id}/status)\n- Input Validation Engine (@NotNull, @Min, @Max, @NotBlank, @Size)\n- REST API Endpoints (/reviews/api/all, /reviews/api/submit)\n- Flash Attribute Notification & Model-View Binding",
            "color": "#065F46", "bg": "#ECFDF5", "border": "#10B981", "y": 32.5, "h": 14
        },
        {
            "num": "TIER 3",
            "name": "BUSINESS SERVICE & STATE MACHINE TIER",
            "tech": "Spring Service Components (@Service) + Transaction Management",
            "components": "- ReviewService (Core business orchestration & metrics calculation)\n- Moderation State Machine (PENDING -> APPROVED / REJECTED / FLAGGED)\n- Multi-attribute Search & Keyword Filter Engine\n- Seed Data Ingestion Engine (@PostConstruct)\n- Real-Time Summary Analytics Calculator (Avg Rating, Counts)",
            "color": "#92400E", "bg": "#FFFBEB", "border": "#F59E0B", "y": 16.5, "h": 14
        },
        {
            "num": "TIER 4",
            "name": "PERSISTENCE & TELEMETRY TIER",
            "tech": "Spring Data JPA + Hibernate + Embedded H2 DB + Actuator",
            "components": "- ReviewRepository (Spring Data JPA interface & custom JPQL queries)\n- Review Entity Model (Relational schema with status enum & timestamps)\n- Embedded In-Memory H2 Engine (Zero external dependencies; fast CI)\n- Spring Boot Actuator (/actuator/health returning HTTP 200 {\"status\":\"UP\"})\n- H2 Web Console (/h2-console) for runtime database inspection",
            "color": "#581C87", "bg": "#FAF5FF", "border": "#8B5CF6", "y": 0.5, "h": 14
        }
    ]

    for t in tiers:
        box = patches.FancyBboxPatch((4, t["y"]), 107, t["h"], boxstyle="round,pad=0.5",
                                     facecolor=t["bg"], edgecolor=t["border"], linewidth=1.8)
        ax.add_patch(box)
        # Header Badge
        badge = patches.FancyBboxPatch((6, t["y"] + t["h"] - 3.8), 28, 3.2, boxstyle="round,pad=0.2",
                                       facecolor=t["color"], edgecolor=t["color"])
        ax.add_patch(badge)
        ax.text(20, t["y"] + t["h"] - 2.2, f"{t['num']}: {t['name']}", ha='center', va='center', color='white', fontsize=8.2, fontweight='bold')
        
        # Tech subtitle
        ax.text(37, t["y"] + t["h"] - 2.2, f"Tech: {t['tech']}", ha='left', va='center', color=t["color"], fontsize=8.2, fontweight='bold')
        
        # Components
        ax.text(7, t["y"] + 4.8, t["components"], ha='left', va='center', color='#1E293B', fontsize=7.5, linespacing=1.25)

    # Downward connection arrows between tiers
    ax.annotate('', xy=(57.5, 48.5), xytext=(57.5, 46.5), arrowprops=dict(facecolor='#475569', edgecolor='#475569', width=2, headwidth=6))
    ax.annotate('', xy=(57.5, 32.5), xytext=(57.5, 30.5), arrowprops=dict(facecolor='#475569', edgecolor='#475569', width=2, headwidth=6))
    ax.annotate('', xy=(57.5, 16.5), xytext=(57.5, 14.5), arrowprops=dict(facecolor='#475569', edgecolor='#475569', width=2, headwidth=6))

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task3\figure_3_2_architecture_crmp.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 3.2 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_3_1()
    generate_figure_3_2()
