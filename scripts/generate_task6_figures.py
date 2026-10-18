import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task6", exist_ok=True)

def generate_figure_6_1():
    """
    Figure 6.1: Git Merge Conflict Creation, Resolution Lifecycle & Semantic Release Baseline (v1.0.0)
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 64), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 67.2, "GIT MERGE CONFLICT LIFECYCLE, RESOLUTION & RELEASE TAGGING (TASK 6)", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    # Main Branch Line (Top)
    ax.plot([10, 106], [53, 53], color='#1E40AF', linewidth=3.5, zorder=1)
    ax.text(5, 53, "main", color='#1E40AF', fontsize=11, fontweight='bold', va='center')
    ax.text(5, 50, "(Production)", color='#64748B', fontsize=7.2, va='center')

    # Dev Branch Line (Middle)
    ax.plot([10, 106], [36, 36], color='#059669', linewidth=3, zorder=1)
    ax.text(5, 36, "dev", color='#059669', fontsize=11, fontweight='bold', va='center')
    ax.text(5, 33, "(Integration)", color='#64748B', fontsize=7.2, va='center')

    # Feature Branch Line (Bottom)
    ax.plot([25, 68], [19, 19], color='#D97706', linewidth=2.5, linestyle='--', zorder=1)
    ax.text(5, 19, "feature/*", color='#D97706', fontsize=10, fontweight='bold', va='center')
    ax.text(5, 16, "(moderation-queue)", color='#64748B', fontsize=7.2, va='center')

    # Dev Baseline Commit
    circle_d0 = plt.Circle((18, 36), 1.8, color='#059669', zorder=2)
    ax.add_patch(circle_d0)
    ax.text(18, 36, "6bcf46d", color='white', fontsize=5.8, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(18, 39.5, "Task 5 baseline", color='#065F46', fontsize=7.0, ha='center')

    # Fork Arrow to feature branch
    ax.annotate('', xy=(27, 21), xytext=(20, 34),
                arrowprops=dict(facecolor='#D97706', edgecolor='#D97706', width=1.5, headwidth=5))
    ax.text(20, 26, "git checkout -b\nfeature/moderation-queue-dashboard", fontsize=6.5, color='#B45309', fontweight='bold')

    # Commit on Feature Branch: da03b1e
    circle_f1 = plt.Circle((42, 19), 2.0, color='#D97706', zorder=2)
    ax.add_patch(circle_f1)
    ax.text(42, 19, "da03b1e", color='white', fontsize=5.8, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(42, 13.5, "feat: moderation audit notes\n& queue settings (90 days)", color='#92400E', fontsize=6.8, ha='center', linespacing=1.1)

    # Conflicting Commit on dev: 18b322a
    circle_d1 = plt.Circle((42, 36), 2.0, color='#059669', zorder=2)
    ax.add_patch(circle_d1)
    ax.text(42, 36, "18b322a", color='white', fontsize=5.8, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(42, 40.5, "feat: dev retention policy\n& verbose audit (180 days)", color='#065F46', fontsize=6.8, ha='center', linespacing=1.1)

    # Conflict Lightning Indicator
    ax.annotate('', xy=(58, 36), xytext=(45, 20.5),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', width=2, headwidth=6))
    
    conflict_box = patches.FancyBboxPatch((48, 23), 22, 9.5, boxstyle="round,pad=0.3",
                                         facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.5)
    ax.add_patch(conflict_box)
    ax.text(59, 29.8, "GIT MERGE CONFLICT!", color='#991B1B', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(59, 27.2, "application.properties", color='#7F1D1D', fontsize=6.8, fontfamily='monospace', ha='center')
    ax.text(59, 24.8, "<<<<<<< HEAD vs >>>>>>>", color='#991B1B', fontsize=6.5, fontweight='bold', ha='center')

    # Resolution Box
    res_box = patches.FancyBboxPatch((52, 12), 26, 8.5, boxstyle="round,pad=0.3",
                                    facecolor='#EDE9FE', edgecolor='#7C3AED', linewidth=1.2)
    ax.add_patch(res_box)
    ax.text(65, 17.5, "MANUAL CONFLICT RESOLUTION", color='#5B21B6', fontsize=6.8, fontweight='bold', ha='center')
    ax.text(65, 14.5, "Unified retention: 180 days\nUnified threshold: 3 flags + VERBOSE", color='#4C1D95', fontsize=6.2, ha='center')

    # Connecting arrow to resolved merge commit
    ax.annotate('', xy=(78, 34.5), xytext=(66, 21),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=2, headwidth=6))

    # Merge Commit on dev: beaf728
    circle_merge = plt.Circle((80, 36), 2.2, color='#059669', zorder=2)
    ax.add_patch(circle_merge)
    ax.text(80, 36, "beaf728", color='white', fontsize=5.8, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(80, 40.5, "Merge Commit beaf728\n(Conflict Resolved)", color='#065F46', fontsize=7.0, fontweight='bold', ha='center')

    # Release Arrow to main (Tagged baseline)
    ax.annotate('', xy=(96, 51), xytext=(82, 38),
                arrowprops=dict(facecolor='#1E40AF', edgecolor='#1E40AF', width=2.2, headwidth=6))
    ax.text(94, 43, "Production Merge\n(Fast-Forward)", color='#1E40AF', fontsize=6.8, fontweight='bold')

    # Release Commit node on main
    circle_rel = plt.Circle((98, 53), 2.5, color='#1E40AF', zorder=2)
    ax.add_patch(circle_rel)
    ax.text(98, 53, "beaf728", color='white', fontsize=6.0, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(98, 57.5, "Production Release", color='#0F172A', fontsize=7.5, fontweight='bold', ha='center')

    # Release Tag Badge
    tag_badge = patches.FancyBboxPatch((90, 60), 16, 4.5, boxstyle="round,pad=0.2",
                                       facecolor='#DC2626', edgecolor='#991B1B', linewidth=1.5)
    ax.add_patch(tag_badge)
    ax.text(98, 62.2, "TAG: v1.0.0", color='white', fontsize=7.8, fontweight='bold', ha='center', va='center')

    # Bottom Foundation Info
    foot_box = patches.FancyBboxPatch((2, 2), 111, 7.5, boxstyle="round,pad=0.4",
                                      facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(foot_box)
    ax.text(57.5, 6.5, "COLLABORATIVE SCM GOVERNANCE & SEMANTIC RELEASE ENGINEERING", 
            ha='center', va='center', color='#0F172A', fontsize=9.2, fontweight='bold')
    ax.text(57.5, 3.8, "Isolated Topic Branching | Real Conflict Marker Triage | Clean Unified Resolution | Tagged v1.0.0 Production Baseline", 
            ha='center', va='center', color='#334155', fontsize=8)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task6\figure_6_1_conflict_resolution_lifecycle.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 6.1 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_6_1()
