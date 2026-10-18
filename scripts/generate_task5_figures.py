import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task5", exist_ok=True)

def generate_figure_5_1():
    """
    Figure 5.1: Feature Branching & Pull Request Collaboration Lifecycle
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 68)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 60), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 63.2, "FEATURE BRANCHING WORKFLOW & PULL REQUEST LIFECYCLE (TASK 5)", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    # Main Branch Line (Top)
    ax.plot([10, 105], [50, 50], color='#1E40AF', linewidth=3.5, zorder=1)
    ax.text(5, 50, "main", color='#1E40AF', fontsize=11, fontweight='bold', va='center')
    ax.text(5, 47, "(Protected)", color='#64748B', fontsize=7.2, va='center')

    # Dev Branch Line (Middle)
    ax.plot([10, 105], [33, 33], color='#059669', linewidth=3, zorder=1)
    ax.text(5, 33, "dev", color='#059669', fontsize=11, fontweight='bold', va='center')
    ax.text(5, 30, "(Integration)", color='#64748B', fontsize=7.2, va='center')

    # Feature Branch Line (Bottom)
    ax.plot([25, 82], [16, 16], color='#D97706', linewidth=2.5, linestyle='--', zorder=1)
    ax.text(5, 16, "feature/*", color='#D97706', fontsize=10, fontweight='bold', va='center')
    ax.text(5, 13, "(review-ingest)", color='#64748B', fontsize=7.2, va='center')

    # Dev Commits
    circle_d0 = plt.Circle((18, 33), 1.8, color='#059669', zorder=2)
    ax.add_patch(circle_d0)
    ax.text(18, 33, "d0", color='white', fontsize=6.5, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(18, 36.5, "Task 4 baseline", color='#065F46', fontsize=7.2, ha='center')

    # Branching fork arrow (dev -> feature/review-ingestion)
    ax.annotate('', xy=(27, 18), xytext=(20, 31),
                arrowprops=dict(facecolor='#D97706', edgecolor='#D97706', width=1.5, headwidth=5))
    ax.text(22, 23.5, "git checkout -b\nfeature/review-ingestion", fontsize=6.8, color='#B45309', fontweight='bold')

    # Feature Commits
    f_commits = [
        {"x": 35, "label": "f1", "desc": "SpamDetectionService\nheuristics (72a6fa7)"},
        {"x": 55, "label": "f2", "desc": "submit.html UI\ncounter (47c7d84)"},
        {"x": 72, "label": "f3", "desc": "100% test pass\n(mvn test green)"}
    ]
    for fc in f_commits:
        circle = plt.Circle((fc["x"], 16), 1.8, color='#D97706', zorder=2)
        ax.add_patch(circle)
        ax.text(fc["x"], 16, fc["label"], color='white', fontsize=6.5, fontweight='bold', ha='center', va='center', zorder=3)
        ax.text(fc["x"], 11.5, fc["desc"], color='#92400E', fontsize=6.8, ha='center', linespacing=1.1)

    # Connecting line on feature branch
    ax.annotate('', xy=(53, 16), xytext=(37, 16), arrowprops=dict(facecolor='#D97706', edgecolor='#D97706', width=1.2, headwidth=4))
    ax.annotate('', xy=(70, 16), xytext=(57, 16), arrowprops=dict(facecolor='#D97706', edgecolor='#D97706', width=1.2, headwidth=4))

    # Pull Request Box & Merge Arrow
    ax.annotate('', xy=(88, 31.5), xytext=(74, 18),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=2, headwidth=6))
    
    pr_box = patches.FancyBboxPatch((72, 21.5), 22, 6.5, boxstyle="round,pad=0.3",
                                    facecolor='#EDE9FE', edgecolor='#8B5CF6', linewidth=1.5)
    ax.add_patch(pr_box)
    ax.text(83, 25.2, "Pull Request #1 (PR)", color='#5B21B6', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(83, 22.8, "Reviewer: Dr. Snehal Andhare\nStatus: APPROVED", color='#4C1D95', fontsize=6.5, ha='center')

    # Merge Commit on dev
    circle_merge = plt.Circle((90, 33), 2.2, color='#059669', zorder=2)
    ax.add_patch(circle_merge)
    ax.text(90, 33, "merge", color='white', fontsize=6.2, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(90, 37.5, "Merge Commit 9b09e9c\n(git merge --no-ff)", color='#065F46', fontsize=7.2, fontweight='bold', ha='center')

    # Bottom Foundation Info
    foot_box = patches.FancyBboxPatch((2, 2), 111, 7.5, boxstyle="round,pad=0.4",
                                      facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(foot_box)
    ax.text(57.5, 6.5, "SCM BRANCHING GOVERNANCE & AUDIT ASSURANCE", 
            ha='center', va='center', color='#0F172A', fontsize=9.2, fontweight='bold')
    ax.text(57.5, 3.8, "Isolated Feature Development | Peer Review & Acceptance Checklist | Non-Fast-Forward Merge History Preservation", 
            ha='center', va='center', color='#334155', fontsize=8)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task5\figure_5_1_feature_branching_workflow.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 5.1 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_5_1()
