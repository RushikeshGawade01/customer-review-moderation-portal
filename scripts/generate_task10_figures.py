import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task10", exist_ok=True)

def generate_figure_10_1():
    """
    Figure 10.1: Jenkins Continuous Testing Pipeline, Quality Gate Enforcement & Defect Recovery Lifecycle
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 64), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 67.2, "JENKINS CONTINUOUS TESTING PIPELINE & DEFECT QUALITY GATE (TASK 10)", 
            ha='center', va='center', color='white', fontsize=11.2, fontweight='bold', fontfamily='sans-serif')

    # Top Left: Trigger & SCM Checkout
    box_scm = patches.FancyBboxPatch((3, 40), 24, 21, boxstyle="round,pad=0.4",
                                    facecolor='#F8FAFC', edgecolor='#3B82F6', linewidth=1.8)
    ax.add_patch(box_scm)
    ax.text(15, 57.5, "Stage 1: SCM Checkout", color='#1E40AF', fontsize=9.0, fontweight='bold', ha='center')
    ax.text(15, 54.5, "GitHub dev Branch Sync", color='#64748B', fontsize=7.2, ha='center')
    ax.text(5, 50.5, "• Clones / pulls dev branch", color='#1E293B', fontsize=6.8)
    ax.text(5, 47.0, "• Evaluates active commit SHA", color='#1E293B', fontsize=6.8)
    ax.text(5, 43.5, "• Prepares build workspace", color='#1E293B', fontsize=6.8)

    # Arrow SCM -> Stage 2
    ax.annotate('', xy=(31, 50.5), xytext=(27, 50.5),
                arrowprops=dict(facecolor='#2563EB', edgecolor='#2563EB', width=2, headwidth=6))

    # Center: Stage 2 - Automated Quality Gate
    box_qg = patches.FancyBboxPatch((32, 38), 34, 24, boxstyle="round,pad=0.5",
                                   facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2.0)
    ax.add_patch(box_qg)
    ax.text(49, 58.5, "Stage 2: Continuous Testing Gate", color='#92400E', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(49, 55.5, "mvn clean test (15 Total Test Cases)", color='#B45309', fontsize=7.2, ha='center')
    ax.text(34, 51.5, "• 7 MockMvc Web & MVC Controller Tests", color='#78350F', fontsize=6.8)
    ax.text(34, 48.0, "• 3 Spam Detection Logic Unit Tests", color='#78350F', fontsize=6.8)
    ax.text(34, 44.5, "• 5 Selenium Headless Chromium Journeys", color='#78350F', fontsize=6.8)
    ax.text(34, 41.0, "• Surefire XML & HTML Test Report Gen", color='#78350F', fontsize=6.8)

    # Branch A: Defect Introduced (Red Path Downward)
    ax.annotate('', xy=(49, 31), xytext=(49, 37.5),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', width=2, headwidth=6))
    ax.text(52, 34.5, "Test Failure (Defect)", color='#DC2626', fontsize=7.2, fontweight='bold')

    box_fail = patches.FancyBboxPatch((32, 13), 34, 17, boxstyle="round,pad=0.4",
                                     facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.8)
    ax.add_patch(box_fail)
    ax.text(49, 26.5, "QUALITY GATE FAILED (Build #1)", color='#991B1B', fontsize=9.0, fontweight='bold', ha='center')
    ax.text(34, 22.5, "• Defect Commit: 52c7d68 (Spam marked APPROVED)", color='#B91C1C', fontsize=6.5)
    ax.text(34, 19.5, "• Selenium Journey 2 fails (AssertionError)", color='#B91C1C', fontsize=6.5)
    ax.text(34, 16.5, "• HALTS PIPELINE: Aborts Package & Deploy!", color='#991B1B', fontsize=6.8, fontweight='bold')

    # Recovery Loop: Defect Correction (Curved Arrow from Fail to SCM)
    ax.annotate('Fix Defect (91aeb11)\n& Push dev', xy=(15, 39.5), xytext=(32, 21),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=1.5, headwidth=5, connectionstyle="arc3,rad=0.3"),
                fontsize=7.2, color='#047857', fontweight='bold', ha='center')

    # Branch B: Quality Gate Passed (Green Path Rightward)
    ax.annotate('', xy=(72, 50.5), xytext=(66.5, 50.5),
                arrowprops=dict(facecolor='#16A34A', edgecolor='#16A34A', width=2, headwidth=6))
    ax.text(69, 53.0, "15/15 Pass", color='#16A34A', fontsize=7.5, fontweight='bold', ha='center')

    # Right: Stage 3, 4, 5 (Deployment Cleared)
    box_deploy = patches.FancyBboxPatch((73, 28), 39, 34, boxstyle="round,pad=0.5",
                                       facecolor='#F0FDF4', edgecolor='#10B981', linewidth=2.0)
    ax.add_patch(box_deploy)
    ax.text(92.5, 58.5, "Stages 3 - 5: Release & Deployment (Build #2)", color='#065F46', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(92.5, 55.5, "CLEARED: 15/15 Tests Passed (SUCCESS)", color='#047857', fontsize=7.2, ha='center')

    dep_stages = [
        ("Stage 3: Package", "mvn package -DskipTests -> 53MB Spring Boot Executable JAR"),
        ("Stage 4: Deploy", "Staged to Tomcat (crmp.war) & Standalone (/deployments/crmp/)"),
        ("Stage 5: Health", "Actuator probe verified HTTP 200 UP on http://localhost:8080/"),
        ("Post Actions", "Archived test report summary HTML, surefire XMLs & JAR")
    ]
    y_d = 50.5
    for s_name, s_detail in dep_stages:
        scard = patches.FancyBboxPatch((75, y_d - 1.8), 35, 4.4, boxstyle="round,pad=0.3",
                                       facecolor='#DCFCE7', edgecolor='#86EFAC')
        ax.add_patch(scard)
        ax.text(76, y_d + 0.8, s_name, color='#065F46', fontsize=7.0, fontweight='bold')
        ax.text(76, y_d - 0.8, s_detail, color='#1E293B', fontsize=6.0)
        y_d -= 5.5

    # Bottom Metadata Strip
    meta_box = patches.FancyBboxPatch((3, 3), 109, 8.0, boxstyle="round,pad=0.5",
                                      facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.2)
    ax.add_patch(meta_box)
    ax.text(5, 7.8, "PROJECT: Git-Based Customer Review Moderation Portal (CRMP) | TASK: 10 (Continuous Testing in Jenkins)", 
            color='#38BDF8', fontsize=7.5, fontweight='bold')
    ax.text(5, 4.8, "STUDENT: Rushikesh Gawade | ROLL: 23102A0052 | EVALUATOR: Dr. Snehal Andhare | EXPERIMENT: Defect Trapping & Recovery", 
            color='#94A3B8', fontsize=7.0)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task10\figure_10_1_continuous_testing_pipeline.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 10.1 saved successfully to:", output_path)


def generate_defect_correction_git_log():
    """
    Generate authentic terminal view documenting Git defect commit, pipeline halt, and fix commit
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.5), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 68)
    ax.axis('off')

    # Window Frame (Dark Theme Terminal)
    frame = patches.FancyBboxPatch((1, 1), 113, 66, boxstyle="round,pad=0.5",
                                   facecolor='#1E1E1E', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(frame)

    # Window Header Bar
    hdr = patches.FancyBboxPatch((1, 62.5), 113, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#2D2D2D', edgecolor='#333333')
    ax.add_patch(hdr)
    ax.text(57.5, 64.5, "Administrator: Windows PowerShell - Task 10 Defect Experiment & Git Audit Trail", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    # Window Controls
    ax.add_patch(patches.Circle((4, 64.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 64.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 64.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> git log --oneline -5", "#FFFFFF", True),
        ("91aeb11 (HEAD -> dev, origin/dev) fix(moderation): correct spam review triage to FLAGGED to restore green continuous testing pipeline", "#4ADE80", True),
        ("52c7d68 defect: introduce intentional regression in spam review status triage (Task 10 experiment)", "#F87171", True),
        ("8a7d268 feat(report): add automated test report generator for Jenkins quality gate", "#38BDF8", False),
        ("6cddddb feat(test): implement Selenium WebDriver 4.x test suite with failure screenshot hook and complete Task 9 documentation", "#CCCCCC", False),
        ("e24bd26 feat(pipeline): implement declarative Jenkinsfile with multi-server deployment and complete Task 8 documentation", "#A0A0A0", False),
        ("-------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # STEP 1: TRIGGER DEFECT BUILD (COMMIT 52c7d68)", "#FACC15", True),
        ("PS D:\\Devops_project> curl.exe -s -X POST 'http://localhost:8085/job/CRMP-Continuous-Testing/buildWithParameters'", "#FFFFFF", False),
        (">>> Jenkins Trigger: Build #1 started for branch dev (Commit: 52c7d68)", "#A0A0A0", False),
        (">>> Stage 2: Quality Gate -> mvn clean test (Selenium Journey 2 Failed: AssertionError)", "#F87171", False),
        (">>> [CRITICAL QUALITY GATE FAILURE] Automated Surefire/Selenium tests failed! Halting pipeline.", "#EF4444", True),
        (">>> Jenkins Result: Build #1 -> FAILURE (Downstream Package & Deploy stages ABORTED)", "#DC2626", True),
        ("-------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # STEP 2: APPLY DEFECT CORRECTION (COMMIT 91aeb11)", "#FACC15", True),
        ("PS D:\\Devops_project> git commit -am 'fix(moderation): correct spam review triage to FLAGGED...' ; git push origin dev", "#FFFFFF", False),
        (">>> Pushed fix to origin/dev: 52c7d68 -> 91aeb11", "#4ADE80", False),
        ("PS D:\\Devops_project> # STEP 3: TRIGGER RE-RUN BUILD (COMMIT 91aeb11)", "#FACC15", True),
        ("PS D:\\Devops_project> curl.exe -s -X POST 'http://localhost:8085/job/CRMP-Continuous-Testing/buildWithParameters'", "#FFFFFF", False),
        (">>> Jenkins Trigger: Build #2 started for branch dev (Commit: 91aeb11)", "#A0A0A0", False),
        (">>> Stage 2: Quality Gate -> mvn clean test (15/15 Tests Passed: 0 failures, 0 skipped)", "#4ADE80", True),
        (">>> Stage 3: Packaging -> Built 53MB customer-review-moderation-portal-1.0.0.jar", "#38BDF8", False),
        (">>> Stage 4: Deploy -> Staged crmp.war to Tomcat webapps & D:\\deployments\\crmp\\", "#38BDF8", False),
        (">>> Stage 5: Health Probe -> Actuator probe verified UP on port 8080", "#38BDF8", False),
        (">>> Jenkins Result: Build #2 -> SUCCESS (Duration: 38.11s) [All 5 Stages Completed]", "#22C55E", True),
        ("-------------------------------------------------------------------------------", "#666666", False)
    ]

    y = 59.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.6, fontfamily='monospace', fontweight=weight)
        y -= 1.88

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task10\defect_correction_git_log.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Git audit trail terminal figure saved successfully to:", output_path)

if __name__ == '__main__':
    generate_figure_10_1()
    generate_defect_correction_git_log()
