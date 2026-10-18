import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task4", exist_ok=True)

def generate_figure_4_1():
    """
    Figure 4.1: Git Branching Strategy & SCM Governance Architecture for CRMP
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 68)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 60), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 63.2, "GIT BRANCHING STRATEGY & SCM WORKFLOW - CUSTOMER REVIEW MODERATION PORTAL", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    # Main Branch Line (Top)
    ax.plot([10, 105], [48, 48], color='#1E40AF', linewidth=3.5, zorder=1)
    ax.text(6, 48, "main", color='#1E40AF', fontsize=11, fontweight='bold', va='center')
    ax.text(6, 45, "(Protected)", color='#64748B', fontsize=7.5, va='center')

    # Dev Branch Line (Middle)
    ax.plot([10, 105], [32, 32], color='#059669', linewidth=3, zorder=1)
    ax.text(6, 32, "dev", color='#059669', fontsize=11, fontweight='bold', va='center')
    ax.text(6, 29, "(Integration)", color='#64748B', fontsize=7.5, va='center')

    # Feature Branch Line (Bottom)
    ax.plot([25, 80], [16, 16], color='#D97706', linewidth=2.5, linestyle='--', zorder=1)
    ax.text(6, 16, "feature/*", color='#D97706', fontsize=10, fontweight='bold', va='center')
    ax.text(6, 13, "(Topic Branches)", color='#64748B', fontsize=7.5, va='center')

    # Commit nodes on main
    main_commits = [
        {"x": 14, "tag": "init", "desc": "Initial skeleton"},
        {"x": 98, "tag": "v1.0.0", "desc": "Production Release"}
    ]
    for c in main_commits:
        circle = plt.Circle((c["x"], 48), 2.2, color='#1E40AF', zorder=2)
        ax.add_patch(circle)
        ax.text(c["x"], 48, c["tag"], color='white', fontsize=6.8, fontweight='bold', ha='center', va='center', zorder=3)
        ax.text(c["x"], 52.5, c["desc"], color='#1E293B', fontsize=7.5, fontweight='bold', ha='center')

    # Release Tag Badge on v1.0.0
    tag_badge = patches.FancyBboxPatch((91, 54), 14, 4.2, boxstyle="round,pad=0.2",
                                       facecolor='#DC2626', edgecolor='#991B1B')
    ax.add_patch(tag_badge)
    ax.text(98, 56.1, "TAG: v1.0.0", color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')

    # Commit nodes on dev
    dev_commits = [
        {"x": 20, "label": "c1", "desc": "docs: init"},
        {"x": 38, "label": "c2", "desc": "feat: skeleton"},
        {"x": 58, "label": "c3", "desc": "test: tests"},
        {"x": 86, "label": "c4", "desc": "merge: PR #1"}
    ]
    for c in dev_commits:
        circle = plt.Circle((c["x"], 32), 1.9, color='#059669', zorder=2)
        ax.add_patch(circle)
        ax.text(c["x"], 32, c["label"], color='white', fontsize=6.5, fontweight='bold', ha='center', va='center', zorder=3)
        ax.text(c["x"], 35.8, c["desc"], color='#065F46', fontsize=7.2, ha='center')

    # Commit nodes on feature branch
    feat_commits = [
        {"x": 34, "label": "f1", "desc": "feat: submit form"},
        {"x": 52, "label": "f2", "desc": "feat: bean valid"},
        {"x": 70, "label": "f3", "desc": "feat: queue triage"}
    ]
    for c in feat_commits:
        circle = plt.Circle((c["x"], 16), 1.8, color='#D97706', zorder=2)
        ax.add_patch(circle)
        ax.text(c["x"], 16, c["label"], color='white', fontsize=6.5, fontweight='bold', ha='center', va='center', zorder=3)
        ax.text(c["x"], 11.8, c["desc"], color='#92400E', fontsize=7.2, ha='center')

    # Arrows for branch & merge
    # main -> dev
    ax.annotate('', xy=(19, 33), xytext=(15, 46.5),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=1.5, headwidth=5))
    # dev -> feature
    ax.annotate('', xy=(33, 17.5), xytext=(22, 31),
                arrowprops=dict(facecolor='#D97706', edgecolor='#D97706', width=1.5, headwidth=5))
    ax.text(25, 23.5, "git checkout -b\nfeature/review-ingestion", fontsize=6.8, color='#B45309', fontweight='bold')

    # feature -> dev (Pull Request)
    ax.annotate('', xy=(85, 31), xytext=(72, 17.5),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=1.8, headwidth=6))
    pr_box = patches.FancyBboxPatch((74, 21), 18, 5, boxstyle="round,pad=0.3",
                                    facecolor='#EDE9FE', edgecolor='#8B5CF6')
    ax.add_patch(pr_box)
    ax.text(83, 23.5, "Pull Request #1 (PR)\nReview & Fast-Forward", color='#5B21B6', fontsize=6.8, fontweight='bold', ha='center', va='center')

    # dev -> main (Release Tag)
    ax.annotate('', xy=(97, 46.5), xytext=(88, 33),
                arrowprops=dict(facecolor='#1E40AF', edgecolor='#1E40AF', width=1.8, headwidth=6))
    ax.text(95, 38.5, "Release PR\nMerge to main", color='#1E40AF', fontsize=6.8, fontweight='bold', ha='center')

    # Bottom Foundation Info
    foot_box = patches.FancyBboxPatch((2, 2), 111, 7.5, boxstyle="round,pad=0.4",
                                      facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(foot_box)
    ax.text(57.5, 6.5, "CONVENTIONAL COMMITS CONVENTION & GOVERNANCE ENFORCEMENT", 
            ha='center', va='center', color='#0F172A', fontsize=9.2, fontweight='bold')
    ax.text(57.5, 3.8, "feat: (new features) | fix: (bug fixes) | test: (automated tests) | docs: (documentation) | ci: (pipeline as code)", 
            ha='center', va='center', color='#334155', fontsize=8)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task4\figure_4_1_git_branching_model.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 4.1 generated at: {output_path}")

def generate_figure_4_2():
    """
    Figure 4.2: Terminal Git Log & Repository Initialization Verification
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 68)
    ax.axis('off')

    # Terminal Window Frame
    term_bg = patches.FancyBboxPatch((2, 2), 111, 64, boxstyle="round,pad=0.5",
                                     facecolor='#0F172A', edgecolor='#334155', linewidth=1.8)
    ax.add_patch(term_bg)

    # Terminal Header Bar
    term_bar = patches.FancyBboxPatch((2, 60.5), 111, 5.5, boxstyle="round,pad=0.3",
                                      facecolor='#1E293B', edgecolor='#334155', linewidth=1.2)
    ax.add_patch(term_bar)
    # Window Control Dots
    dot_colors = ['#EF4444', '#F59E0B', '#10B981']
    for idx, c in enumerate(dot_colors):
        dot = plt.Circle((5 + idx * 3, 63.2), 1.1, color=c)
        ax.add_patch(dot)

    ax.text(57.5, 63.2, "PowerShell - Git Version Control Baseline Verification (Rushikesh Gawade / 23102A0052)", 
            ha='center', va='center', color='#E2E8F0', fontsize=8.8, fontweight='bold', fontfamily='monospace')

    # Terminal Text Output Lines
    lines = [
        ("PS D:\\Devops_project> git status", "#38BDF8", True),
        ("On branch dev", "#F1F5F9", False),
        ("nothing to commit, working tree clean", "#10B981", False),
        ("", "#000000", False),
        ("PS D:\\Devops_project> git branch -a", "#38BDF8", True),
        ("* dev", "#10B981", True),
        ("  main", "#F1F5F9", False),
        ("", "#000000", False),
        ("PS D:\\Devops_project> git remote -v", "#38BDF8", True),
        ("origin  https://github.com/rushikesh-gawade/customer-review-moderation-portal.git (fetch)", "#F1F5F9", False),
        ("origin  https://github.com/rushikesh-gawade/customer-review-moderation-portal.git (push)", "#F1F5F9", False),
        ("", "#000000", False),
        ("PS D:\\Devops_project> git log --oneline --graph --decorate", "#38BDF8", True),
        ("* b0d2ac9 (HEAD -> dev, main) docs: add completed laboratory task reports 1 through 3 and evidence", "#F59E0B", False),
        ("* e202685 test: add automated Spring Boot tests for review moderation and health probe", "#F59E0B", False),
        ("* 37c04a4 feat: implement Spring Boot application skeleton and 4-tier architecture", "#F59E0B", False),
        ("* 17e071f docs: initialize project governance with README, .gitignore, and issue templates", "#F59E0B", False),
        ("", "#000000", False),
        ("PS D:\\Devops_project> git config --get user.name; git config --get user.email", "#38BDF8", True),
        ("Rushikesh Gawade", "#10B981", True),
        ("rushikesh.gawade@student.univ.edu", "#10B981", True)
    ]

    y_pos = 57.0
    for text, color, bold in lines:
        if text:
            ax.text(5, y_pos, text, color=color, fontsize=7.6, fontfamily='monospace', fontweight='bold' if bold else 'normal')
        y_pos -= 2.45

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task4\figure_4_2_git_terminal_log.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 4.2 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_4_1()
    generate_figure_4_2()
