import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task7", exist_ok=True)

def generate_figure_7_1():
    """
    Figure 7.1: Jenkins Continuous Integration Architecture & Automated Maven Build Pipeline
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 64), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 67.2, "JENKINS CONTINUOUS INTEGRATION ARCHITECTURE & MAVEN PIPELINE (TASK 7)", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    # Stage 1: GitHub Remote Repository (Left)
    box_git = patches.FancyBboxPatch((4, 28), 24, 30, boxstyle="round,pad=0.5",
                                    facecolor='#F8FAFC', edgecolor='#3B82F6', linewidth=1.8)
    ax.add_patch(box_git)
    ax.text(16, 54, "GitHub Remote SCM", color='#1E40AF', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(16, 51.5, "(Source of Truth)", color='#64748B', fontsize=7.2, ha='center')
    ax.text(16, 46, "Repository:\ncustomer-review-\nmoderation-portal", color='#0F172A', fontsize=7.8, ha='center', fontweight='bold', linespacing=1.2)
    ax.text(16, 38.5, "Branch: dev\nCommit: 14be78f\nAuthor: Rushikesh Gawade", color='#334155', fontsize=7.0, ha='center', linespacing=1.2)
    
    tag_box = patches.FancyBboxPatch((7, 30.5), 18, 4.5, boxstyle="round,pad=0.2",
                                     facecolor='#DC2626', edgecolor='#991B1B')
    ax.add_patch(tag_box)
    ax.text(16, 32.7, "Baseline: v1.0.0", color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')

    # Trigger Arrow (SCM Polling)
    ax.annotate('', xy=(34, 43), xytext=(28, 43),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=2, headwidth=6))
    ax.text(31, 45.5, "SCM Poll\n(H/5 * * * *)", color='#065F46', fontsize=6.8, fontweight='bold', ha='center')

    # Stage 2: Jenkins Server Container / Host (Center Box)
    box_jenkins = patches.FancyBboxPatch((35, 16), 46, 44, boxstyle="round,pad=0.6",
                                        facecolor='#F0FDF4', edgecolor='#10B981', linewidth=2.0)
    ax.add_patch(box_jenkins)
    ax.text(58, 56.5, "Jenkins CI Server (v2.580.1)", color='#065F46', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(58, 54, "Port: 8085 | Home: D:\\jenkins_home | Job: CRMP-Maven-CI", color='#047857', fontsize=7.5, ha='center')

    # Internal Pipeline Steps in Jenkins
    steps = [
        {"y": 46.5, "title": "Step 1: Workspace Git Sync", "desc": "git clone -b dev ... / git pull", "color": "#E0F2FE", "border": "#0284C7"},
        {"y": 38.0, "title": "Step 2: Automated Quality Gate", "desc": "mvn clean test (10/10 Tests Passed)", "color": "#DCFCE7", "border": "#16A34A"},
        {"y": 29.5, "title": "Step 3: Maven Package & Build", "desc": "mvn package -> target/*.jar (53 MB)", "color": "#FEF3C7", "border": "#D97706"},
        {"y": 21.0, "title": "Step 4: Artifact Archiving Action", "desc": "Archive target/*.jar to build/1/archive", "color": "#EDE9FE", "border": "#7C3AED"}
    ]

    for s in steps:
        s_box = patches.FancyBboxPatch((38, s["y"] - 2.5), 40, 6.2, boxstyle="round,pad=0.3",
                                       facecolor=s["color"], edgecolor=s["border"], linewidth=1.2)
        ax.add_patch(s_box)
        ax.text(58, s["y"] + 1.2, s["title"], color='#0F172A', fontsize=7.8, fontweight='bold', ha='center')
        ax.text(58, s["y"] - 1.0, s["desc"], color='#334155', fontsize=6.8, fontfamily='monospace', ha='center')

    # Arrow to Artifact Store
    ax.annotate('', xy=(88, 43), xytext=(81, 43),
                arrowprops=dict(facecolor='#7C3AED', edgecolor='#7C3AED', width=2, headwidth=6))
    ax.text(84.5, 45.5, "Post-Build\nArchive", color='#5B21B6', fontsize=6.8, fontweight='bold', ha='center')

    # Stage 3: Artifact Repository & Feedback (Right)
    box_art = patches.FancyBboxPatch((88, 28), 23, 30, boxstyle="round,pad=0.5",
                                    facecolor='#FAF5FF', edgecolor='#8B5CF6', linewidth=1.8)
    ax.add_patch(box_art)
    ax.text(99.5, 54, "Jenkins Artifact Store", color='#5B21B6', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(99.5, 51.5, "(Build #1 Output)", color='#64748B', fontsize=7.2, ha='center')
    
    ax.text(99.5, 45.5, "Archived JAR:\ncustomer-review-\nmoderation-portal-\n1.0.0-SNAPSHOT.jar", 
            color='#0F172A', fontsize=7.2, fontfamily='monospace', fontweight='bold', ha='center', linespacing=1.2)
    ax.text(99.5, 36.5, "Status: SUCCESS\nDuration: 40.8 s\nSize: 53.0 MB", color='#4C1D95', fontsize=7.2, ha='center', linespacing=1.2)
    
    badge_green = patches.FancyBboxPatch((91, 30), 17, 4.5, boxstyle="round,pad=0.2",
                                         facecolor='#10B981', edgecolor='#059669')
    ax.add_patch(badge_green)
    ax.text(99.5, 32.2, "BUILD: SUCCESS", color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')

    # Bottom Foundation Info
    foot_box = patches.FancyBboxPatch((2, 2), 111, 8.5, boxstyle="round,pad=0.4",
                                      facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(foot_box)
    ax.text(57.5, 7.2, "CONTINUOUS INTEGRATION & AUTOMATED FEEDBACK ASSURANCE", 
            ha='center', va='center', color='#0F172A', fontsize=9.2, fontweight='bold')
    ax.text(57.5, 4.2, "Git Remote SCM Trigger | Clean Workspace Isolation | Surefire Quality Gate (10/10 Green) | Immutable Artifact Archiving", 
            ha='center', va='center', color='#334155', fontsize=8)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task7\figure_7_1_jenkins_ci_architecture.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 7.1 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_7_1()
