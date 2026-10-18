import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task8", exist_ok=True)

def generate_figure_8_1():
    """
    Figure 8.1: Declarative Jenkins Pipeline as Code Architecture, Parameterized Deployment & Server Targets
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 72)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 64), 111, 6.5, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 67.2, "JENKINS PIPELINE AS CODE (JENKINSFILE) & SERVER DEPLOYMENT (TASK 8)", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')

    # Left Box: Pipeline as Code & Parameter Matrix
    box_code = patches.FancyBboxPatch((3, 16), 26, 45, boxstyle="round,pad=0.5",
                                      facecolor='#F8FAFC', edgecolor='#3B82F6', linewidth=1.8)
    ax.add_patch(box_code)
    ax.text(16, 58, "Pipeline as Code", color='#1E40AF', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(16, 55.5, "(Root: Jenkinsfile)", color='#64748B', fontsize=7.2, ha='center')

    params_info = [
        ("DEPLOY_ENV", "production | staging | dev"),
        ("SERVER_PORT", "8080 (Configurable)"),
        ("DEPLOY_TARGET", "Apache-Tomcat-11"),
        ("APP_VERSION", "1.0.0 (Semantic Tag)"),
        ("STUDENT_NAME", "Rushikesh Gawade"),
        ("ROLL_NUMBER", "23102A0052")
    ]
    y_p = 50.5
    for name, val in params_info:
        p_badge = patches.FancyBboxPatch((5, y_p - 1.8), 22, 4.2, boxstyle="round,pad=0.2",
                                         facecolor='#EFF6FF', edgecolor='#BFDBFE')
        ax.add_patch(p_badge)
        ax.text(6, y_p + 0.3, name + ":", color='#1E40AF', fontsize=6.8, fontweight='bold')
        ax.text(6, y_p - 1.1, val, color='#1E293B', fontsize=6.2, fontfamily='monospace')
        y_p -= 5.4

    # Arrow from Code to Pipeline Execution
    ax.annotate('', xy=(33, 38), xytext=(29, 38),
                arrowprops=dict(facecolor='#059669', edgecolor='#059669', width=2, headwidth=6))

    # Center Box: Declarative Pipeline Execution Stages
    box_pipe = patches.FancyBboxPatch((34, 16), 46, 45, boxstyle="round,pad=0.6",
                                     facecolor='#F0FDF4', edgecolor='#10B981', linewidth=2.0)
    ax.add_patch(box_pipe)
    ax.text(57, 58, "Declarative Pipeline Stages (CRMP-Pipeline-Deploy)", color='#065F46', fontsize=10.0, fontweight='bold', ha='center')
    ax.text(57, 55.5, "Job: CRMP-Pipeline-Deploy | Build #2: SUCCESS (26.07 s)", color='#047857', fontsize=7.5, ha='center')

    stages = [
        {"y": 48.5, "name": "Stage 1: Checkout", "cmd": "checkout scm (dev @ 14be78f)", "color": "#E0F2FE", "border": "#0284C7"},
        {"y": 40.5, "name": "Stage 2: Build & Test", "cmd": "mvn clean test (10/10 Tests Passed)", "color": "#DCFCE7", "border": "#16A34A"},
        {"y": 32.5, "name": "Stage 3: Package", "cmd": "mvn package -> target/*.jar (53 MB)", "color": "#FEF3C7", "border": "#D97706"},
        {"y": 24.5, "name": "Stage 4: Deploy to Server", "cmd": "Deploy to Tomcat & D:\\deployments", "color": "#EDE9FE", "border": "#7C3AED"},
        {"y": 16.5, "name": "Stage 5: Health Probe", "cmd": "GET /actuator/health -> HTTP 200 UP", "color": "#FCE7F3", "border": "#DB2777"}
    ]

    for st in stages:
        st_box = patches.FancyBboxPatch((37, st["y"] - 1.8), 40, 5.8, boxstyle="round,pad=0.3",
                                        facecolor=st["color"], edgecolor=st["border"], linewidth=1.2)
        ax.add_patch(st_box)
        ax.text(57, st["y"] + 1.2, st["name"], color='#0F172A', fontsize=7.6, fontweight='bold', ha='center')
        ax.text(57, st["y"] - 0.8, st["cmd"], color='#334155', fontsize=6.6, fontfamily='monospace', ha='center')

    # Arrow from Pipeline to Deployment Targets
    ax.annotate('', xy=(84, 38), xytext=(80, 38),
                arrowprops=dict(facecolor='#7C3AED', edgecolor='#7C3AED', width=2, headwidth=6))

    # Right Box: Deployment Targets & Live Telemetry
    box_dep = patches.FancyBboxPatch((85, 16), 27, 45, boxstyle="round,pad=0.5",
                                     facecolor='#FAF5FF', edgecolor='#8B5CF6', linewidth=1.8)
    ax.add_patch(box_dep)
    ax.text(98.5, 58, "Server Deployment Targets", color='#5B21B6', fontsize=9.2, fontweight='bold', ha='center')
    ax.text(98.5, 55.5, "(Active Production)", color='#64748B', fontsize=7.2, ha='center')

    # Target 1: Apache Tomcat 11
    t1_box = patches.FancyBboxPatch((87, 42.5), 23, 10.5, boxstyle="round,pad=0.3",
                                    facecolor='#EDE9FE', edgecolor='#8B5CF6', linewidth=1.2)
    ax.add_patch(t1_box)
    ax.text(98.5, 50.5, "Apache Tomcat 11", color='#5B21B6', fontsize=7.6, fontweight='bold', ha='center')
    ax.text(98.5, 47.8, "webapps\\crmp.war", color='#0F172A', fontsize=6.8, fontfamily='monospace', ha='center')
    ax.text(98.5, 45.0, "D:\\apache-tomcat-11...", color='#4C1D95', fontsize=6.2, ha='center')

    # Target 2: Standalone / Embedded Target
    t2_box = patches.FancyBboxPatch((87, 29.5), 23, 10.5, boxstyle="round,pad=0.3",
                                    facecolor='#ECFDF5', edgecolor='#10B981', linewidth=1.2)
    ax.add_patch(t2_box)
    ax.text(98.5, 37.5, "Standalone Production", color='#065F46', fontsize=7.6, fontweight='bold', ha='center')
    ax.text(98.5, 34.8, "D:\\deployments\\crmp\\*.jar", color='#0F172A', fontsize=6.8, fontfamily='monospace', ha='center')
    ax.text(98.5, 32.0, "Port 8080 | Java 21", color='#047857', fontsize=6.2, ha='center')

    # Live Health Badge
    badge_health = patches.FancyBboxPatch((87, 18), 23, 8.5, boxstyle="round,pad=0.3",
                                          facecolor='#D1FAE5', edgecolor='#059669', linewidth=1.5)
    ax.add_patch(badge_health)
    ax.text(98.5, 23.5, "HEALTH STATUS: UP", color='#065F46', fontsize=7.8, fontweight='bold', ha='center')
    ax.text(98.5, 20.2, "http://localhost:8080/actuator/health\nHTTP 200 OK (Verified)", color='#047857', fontsize=6.2, ha='center', linespacing=1.2)

    # Bottom Foundation Info
    foot_box = patches.FancyBboxPatch((2, 2), 111, 8.5, boxstyle="round,pad=0.4",
                                      facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(foot_box)
    ax.text(57.5, 7.2, "CONTINUOUS DEPLOYMENT & PIPELINE AS CODE GOVERNANCE", 
            ha='center', va='center', color='#0F172A', fontsize=9.2, fontweight='bold')
    ax.text(57.5, 4.2, "Declarative Pipeline Syntax | Parameterized Runtime Environment | Automated Tomcat Staging | Live Health Gating", 
            ha='center', va='center', color='#334155', fontsize=8)

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task8\figure_8_1_pipeline_architecture.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 8.1 generated at: {output_path}")

if __name__ == "__main__":
    generate_figure_8_1()
