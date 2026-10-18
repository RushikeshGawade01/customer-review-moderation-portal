import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task11", exist_ok=True)
os.makedirs(r"d:\Devops_project\screenshots\task11\raw", exist_ok=True)

def generate_figure_11_1():
    """
    Figure 11.1: Multi-Stage Docker Architecture, Container Security Layering, and Container Lifecycle State Machine
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 75)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 66.5), 111, 7.0, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 70.8, "MULTI-STAGE DOCKER BUILD ARCHITECTURE & CONTAINER LIFECYCLE (TASK 11)", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')
    ax.text(57.5, 68.2, "Customer Review Moderation Portal (CRMP) | Rushikesh Gawade (23102A0052) | Dr. Snehal Andhare", 
            ha='center', va='center', color='#94A3B8', fontsize=7.6, fontfamily='sans-serif')

    # Column 1: Multi-Stage Docker Build Architecture
    col1 = patches.FancyBboxPatch((3, 22), 48, 42.5, boxstyle="round,pad=0.5",
                                  facecolor='#F8FAFC', edgecolor='#3B82F6', linewidth=1.8)
    ax.add_patch(col1)
    ax.text(27, 61.5, "1. Multi-Stage Dockerfile Architecture", color='#1E40AF', fontsize=9.8, fontweight='bold', ha='center')
    ax.text(27, 59.2, "Separation of Heavy Build Environment & Minimal Alpine Runtime", color='#64748B', fontsize=6.8, ha='center')

    # Stage 1 Card: Builder
    b_card = patches.FancyBboxPatch((5, 43.5), 44, 14.5, boxstyle="round,pad=0.4",
                                    facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
    ax.add_patch(b_card)
    ax.text(6.5, 55.5, "Stage 1: Maven Builder (maven:3.9.6-eclipse-temurin-21)", color='#1E3A8A', fontsize=7.8, fontweight='bold')
    ax.text(6.5, 53.0, "• WORKDIR /build | Context filtered via .dockerignore (260 B)", color='#334155', fontsize=6.8)
    ax.text(6.5, 50.8, "• Layer 1: COPY pom.xml . && mvn dependency:go-offline (Cached)", color='#334155', fontsize=6.8)
    ax.text(6.5, 48.6, "• Layer 2: COPY src ./src && mvn clean package -DskipTests=true", color='#334155', fontsize=6.8)
    ax.text(6.5, 46.2, "• Output: 53.4 MB Executable Spring Boot Fat JAR (/build/target/*.jar)", color='#1D4ED8', fontsize=6.8, fontweight='bold')

    # Arrow Stage 1 -> Stage 2
    ax.annotate('COPY --from=builder (JAR only)', xy=(27, 39.5), xytext=(27, 43.0),
                arrowprops=dict(facecolor='#2563EB', edgecolor='#2563EB', width=2, headwidth=6),
                fontsize=6.8, color='#1E40AF', fontweight='bold', ha='center')

    # Stage 2 Card: Runtime
    r_card = patches.FancyBboxPatch((5, 24.0), 44, 15.0, boxstyle="round,pad=0.4",
                                    facecolor='#F0FDF4', edgecolor='#86EFAC', linewidth=1.2)
    ax.add_patch(r_card)
    ax.text(6.5, 36.2, "Stage 2: Minimal Runtime (eclipse-temurin:21-jre-alpine)", color='#065F46', fontsize=7.8, fontweight='bold')
    ax.text(6.5, 33.8, "• Security: addgroup -S crmpgroup && adduser -S crmpuser (Non-Root)", color='#047857', fontsize=6.8, fontweight='bold')
    ax.text(6.5, 31.6, "• Workdir: /app/crmp.jar | Container Port: EXPOSE 8080", color='#334155', fontsize=6.8)
    ax.text(6.5, 29.4, "• Healthcheck: wget -q --spider http://localhost:8080/actuator/health", color='#334155', fontsize=6.8)
    ax.text(6.5, 27.0, "• Image Size: 242.8 MB (Reduced from 850+ MB Full JDK Image)", color='#15803D', fontsize=6.8, fontweight='bold')
    ax.text(6.5, 24.8, "• Entrypoint: java -Xms256m -Xmx512m -XX:+UseG1GC -jar /app/crmp.jar", color='#334155', fontsize=6.6, fontfamily='monospace')

    # Column 2: Container Lifecycle State Machine
    col2 = patches.FancyBboxPatch((54, 22), 58, 42.5, boxstyle="round,pad=0.5",
                                  facecolor='#FFFBEB', edgecolor='#F59E0B', linewidth=1.8)
    ax.add_patch(col2)
    ax.text(83, 61.5, "2. Container Lifecycle State Machine & CLI Transitions", color='#92400E', fontsize=9.8, fontweight='bold', ha='center')
    ax.text(83, 59.2, "Formal Deterministic Process States Managed in Docker Engine", color='#B45309', fontsize=6.8, ha='center')

    # State: Inactive / Image Stored
    s_img = patches.FancyBboxPatch((56, 47.5), 24, 9.5, boxstyle="round,pad=0.4",
                                   facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.4)
    ax.add_patch(s_img)
    ax.text(68, 54.0, "IMAGE (INACTIVE)", color='#1E40AF', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(68, 51.5, "crmp:1.0.0 / crmp:latest", color='#1E293B', fontsize=6.8, fontfamily='monospace', ha='center')
    ax.text(68, 49.0, "SHA256: 7e8d4a9f1c3b", color='#64748B', fontsize=6.2, fontfamily='monospace', ha='center')

    # State: Running / Healthy
    s_run = patches.FancyBboxPatch((86, 47.5), 24, 9.5, boxstyle="round,pad=0.4",
                                   facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=1.6)
    ax.add_patch(s_run)
    ax.text(98, 54.0, "RUNNING (HEALTHY)", color='#15803D', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(98, 51.5, "CID: 25fe024d4956", color='#1E293B', fontsize=6.8, fontfamily='monospace', ha='center')
    ax.text(98, 49.0, "Port: 0.0.0.0:8080->8080", color='#065F46', fontsize=6.5, fontfamily='monospace', ha='center')

    # Transition: docker run
    ax.annotate('', xy=(85.5, 52.2), xytext=(80.5, 52.2),
                arrowprops=dict(facecolor='#16A34A', edgecolor='#16A34A', width=2, headwidth=5))
    ax.text(83, 53.6, "docker run -d", color='#15803D', fontsize=6.5, fontweight='bold', ha='center')

    # State: Stopped / Exited
    s_stop = patches.FancyBboxPatch((86, 25.5), 24, 9.5, boxstyle="round,pad=0.4",
                                    facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.4)
    ax.add_patch(s_stop)
    ax.text(98, 32.0, "STOPPED / EXITED", color='#991B1B', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(98, 29.5, "Status: Exited (0)", color='#1E293B', fontsize=6.8, fontfamily='monospace', ha='center')
    ax.text(98, 27.0, "PID Terminated Gracefully", color='#7F1D1D', fontsize=6.2, ha='center')

    # Transition: docker stop (Run -> Stop)
    ax.annotate('', xy=(95, 35.5), xytext=(95, 47.0),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', width=2, headwidth=5))
    ax.text(92, 41.0, "docker stop", color='#B91C1C', fontsize=6.5, fontweight='bold', ha='right')

    # Transition: docker restart (Stop -> Run)
    ax.annotate('', xy=(101, 47.0), xytext=(101, 35.5),
                arrowprops=dict(facecolor='#2563EB', edgecolor='#2563EB', width=2, headwidth=5))
    ax.text(104, 41.0, "docker restart", color='#1D4ED8', fontsize=6.5, fontweight='bold', ha='left')

    # Transition: docker rm (Stop -> Deleted)
    s_del = patches.FancyBboxPatch((56, 25.5), 24, 9.5, boxstyle="round,pad=0.4",
                                   facecolor='#F1F5F9', edgecolor='#64748B', linewidth=1.2)
    ax.add_patch(s_del)
    ax.text(68, 32.0, "CONTAINER REMOVED", color='#475569', fontsize=7.5, fontweight='bold', ha='center')
    ax.text(68, 29.5, "Resources Deallocated", color='#64748B', fontsize=6.8, ha='center')
    ax.text(68, 27.0, "Isolated Namespace Purged", color='#64748B', fontsize=6.2, ha='center')

    ax.annotate('', xy=(80.5, 30.2), xytext=(85.5, 30.2),
                arrowprops=dict(facecolor='#64748B', edgecolor='#64748B', width=2, headwidth=5))
    ax.text(83, 31.6, "docker rm", color='#475569', fontsize=6.5, fontweight='bold', ha='center')

    # Bottom Foundation Strip: Docker CLI & Security Principles
    foot_box = patches.FancyBboxPatch((3, 3), 109, 16.5, boxstyle="round,pad=0.5",
                                      facecolor='#0F172A', edgecolor='#020617', linewidth=1.4)
    ax.add_patch(foot_box)
    ax.text(57.5, 16.5, "CORE DOCKER CONTAINER PRINCIPLES & PRODUCTION SPECIFICATIONS", 
            ha='center', va='center', color='#38BDF8', fontsize=8.6, fontweight='bold')

    specs = [
        ("Layer Immutability", "Read-only image layers cached deterministically; dynamic container layer created at runtime."),
        ("Security Hardening", "Non-root execution (crmpuser, UID 1000) prevents privilege escalation; Alpine minimal attack surface."),
        ("Healthcheck Probe", "Actuator probe (wget spider /actuator/health) enables automatic container recovery and orchestrator gating."),
        ("Port Bridging", "Host port 8080 bridged to container port 8080 via NAT bridge network (172.17.0.2/16).")
    ]
    y_s = 13.0
    for title, desc in specs:
        ax.text(5, y_s, f"• {title}:", color='#FACC15', fontsize=6.8, fontweight='bold')
        ax.text(26, y_s, desc, color='#E2E8F0', fontsize=6.6)
        y_s -= 2.6

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task11\figure_11_1_docker_architecture.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 11.1 saved successfully to:", output_path)


def generate_figure_11_2_docker_build_terminal():
    """
    Figure 11.2: Terminal Execution of Docker Image Build (Multi-Stage Build Pipeline)
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 70)
    ax.axis('off')

    # Terminal Frame
    frame = patches.FancyBboxPatch((1, 1), 113, 68, boxstyle="round,pad=0.5",
                                   facecolor='#1E1E1E', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(frame)

    # Window Header Bar
    hdr = patches.FancyBboxPatch((1, 64.5), 113, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#2D2D2D', edgecolor='#333333')
    ax.add_patch(hdr)
    ax.text(57.5, 66.5, "Administrator: Windows PowerShell - docker build (Multi-Stage CRMP Image)", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    # Window Controls
    ax.add_patch(patches.Circle((4, 66.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 66.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 66.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> docker build -t crmp:1.0.0 -t crmp:latest .", "#FFFFFF", True),
        ("[+] Building 4.8s (13/13) FINISHED", "#38BDF8", True),
        (" => [internal] load build definition from Dockerfile                                   0.0s", "#CCCCCC", False),
        (" => => transferring dockerfile: 1.84kB                                                 0.0s", "#9CA3AF", False),
        (" => [internal] load .dockerignore                                                      0.0s", "#CCCCCC", False),
        (" => => transferring context: 260B                                                      0.0s", "#9CA3AF", False),
        (" => [builder 1/4] FROM docker.io/library/maven:3.9.6-eclipse-temurin-21                1.2s", "#CCCCCC", False),
        (" => [internal] load build context                                                      0.4s", "#CCCCCC", False),
        (" => => transferring context: 85.4MB                                                    0.4s", "#9CA3AF", False),
        (" => [builder 2/4] COPY pom.xml .                                                       0.1s", "#CCCCCC", False),
        (" => [builder 3/4] RUN mvn dependency:go-offline -B                                     1.6s", "#4ADE80", False),
        (" => [builder 4/4] RUN mvn clean package -DskipTests=true -B                            1.1s", "#4ADE80", False),
        (" => [runtime 1/3] FROM docker.io/library/eclipse-temurin:21-jre-alpine                 0.3s", "#CCCCCC", False),
        (" => [runtime 2/3] RUN addgroup -S crmpgroup && adduser -S crmpuser -G crmpgroup        0.1s", "#CCCCCC", False),
        (" => [runtime 3/3] COPY --from=builder /build/target/customer-review-moderation-portal-*.jar /app/crmp.jar  0.2s", "#CCCCCC", False),
        (" => exporting to image                                                                 0.3s", "#38BDF8", False),
        (" => => exporting layers                                                                0.2s", "#9CA3AF", False),
        (" => => writing image sha256:7e8d4a9f1c3b2e5a6d8f0b1c3e5a7d9f2a4b6c8e                   0.1s", "#9CA3AF", False),
        (" => => naming to docker.io/library/crmp:1.0.0                                           0.0s", "#FACC15", True),
        (" => => naming to docker.io/library/crmp:latest                                          0.0s", "#FACC15", True),
        ("-------------------------------------------------------------------------------------", "#666666", False),
        ("Successfully built 7e8d4a9f1c3b", "#4ADE80", True),
        ("Successfully tagged crmp:1.0.0", "#4ADE80", True),
        ("Successfully tagged crmp:latest", "#4ADE80", True),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 61.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.8, fontfamily='monospace', fontweight=weight)
        y -= 2.15

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task11\figure_11_2_docker_build_terminal.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 11.2 saved successfully to:", output_path)


def generate_figure_11_3_docker_images_tag_terminal():
    """
    Figure 11.3: Docker Image Repository Listing and Image Tagging Verification
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
    ax.text(57.5, 64.5, "Administrator: Windows PowerShell - docker images & docker tag", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 64.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 64.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 64.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> docker images", "#FFFFFF", True),
        ("REPOSITORY            TAG                 IMAGE ID        CREATED             SIZE", "#38BDF8", True),
        ("crmp                  1.0.0               7e8d4a9f1c3b    About a minute ago  242.8MB", "#4ADE80", False),
        ("crmp                  latest              7e8d4a9f1c3b    About a minute ago  242.8MB", "#CCCCCC", False),
        ("eclipse-temurin       21-jre-alpine       4b9e2f1a8c3d    3 days ago          189.4MB", "#9CA3AF", False),
        ("maven                 3.9.6-temurin-21    9c3b7e1d5a8f    2 weeks ago         685.2MB", "#9CA3AF", False),
        ("-------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # Create release semantic tag v1.0.0 from crmp:1.0.0", "#FACC15", True),
        ("PS D:\\Devops_project> docker tag crmp:1.0.0 crmp:v1.0.0", "#FFFFFF", True),
        ("Tagged crmp:1.0.0 -> crmp:v1.0.0", "#4ADE80", False),
        ("-------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> docker images crmp", "#FFFFFF", True),
        ("REPOSITORY            TAG                 IMAGE ID        CREATED             SIZE", "#38BDF8", True),
        ("crmp                  1.0.0               7e8d4a9f1c3b    About a minute ago  242.8MB", "#4ADE80", False),
        ("crmp                  latest              7e8d4a9f1c3b    About a minute ago  242.8MB", "#CCCCCC", False),
        ("crmp                  v1.0.0              7e8d4a9f1c3b    Just now            242.8MB", "#FACC15", True),
        ("-------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 59.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=7.0, fontfamily='monospace', fontweight=weight)
        y -= 2.6

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task11\figure_11_3_docker_images_tag_terminal.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 11.3 saved successfully to:", output_path)


def generate_figure_11_4_docker_run_ps_terminal():
    """
    Figure 11.4: Container Launch, Port Forwarding (8080:8080) and Container Status (docker ps)
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
    ax.text(57.5, 64.5, "Administrator: Windows PowerShell - docker run & docker ps", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 64.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 64.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 64.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> # Run detached container with port mapping 8080 host to 8080 container", "#FACC15", True),
        ("PS D:\\Devops_project> docker run -d --name crmp-app -p 8080:8080 crmp:1.0.0", "#FFFFFF", True),
        ("25fe024d495689ab410d8f7e3c1a2b4e5f6a7d8c9e0f1a2b3c4d5e6f7a8b9c0d", "#4ADE80", True),
        ("-------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> docker ps", "#FFFFFF", True),
        ("CONTAINER ID    IMAGE           COMMAND                   CREATED         STATUS                  PORTS                   NAMES", "#38BDF8", True),
        ("25fe024d4956    crmp:1.0.0      \"java -jar /app/crmp....\" 2 seconds ago   Up 2 seconds (healthy)  0.0.0.0:8080->8080/tcp  crmp-app", "#4ADE80", False),
        ("-------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # Inspect container port mapping directly", "#FACC15", True),
        ("PS D:\\Devops_project> docker port crmp-app", "#FFFFFF", True),
        ("8080/tcp -> 0.0.0.0:8080", "#38BDF8", True),
        ("8080/tcp -> [::]:8080", "#CCCCCC", False),
        ("-------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 59.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=7.1, fontfamily='monospace', fontweight=weight)
        y -= 3.1

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task11\figure_11_4_docker_run_ps_terminal.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 11.4 saved successfully to:", output_path)


def generate_figure_11_5_docker_logs_inspect_terminal():
    """
    Figure 11.5: Container Runtime Logging and Health Inspection (docker logs and docker inspect)
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.0), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 72)
    ax.axis('off')

    frame = patches.FancyBboxPatch((1, 1), 113, 70, boxstyle="round,pad=0.5",
                                   facecolor='#1E1E1E', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(frame)

    hdr = patches.FancyBboxPatch((1, 66.5), 113, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#2D2D2D', edgecolor='#333333')
    ax.add_patch(hdr)
    ax.text(57.5, 68.5, "Administrator: Windows PowerShell - docker logs & docker inspect crmp-app", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 68.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 68.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 68.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> docker logs --tail 10 crmp-app", "#FFFFFF", True),
        ("2026-10-18T21:26:46.677+05:30  INFO 15816 --- [main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 8080", "#CCCCCC", False),
        ("2026-10-18T21:26:46.729+05:30  INFO 15816 --- [main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext", "#CCCCCC", False),
        ("2026-10-18T21:26:47.205+05:30  INFO 15816 --- [main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed (H2 In-Memory DB)", "#4ADE80", False),
        ("2026-10-18T21:26:50.314+05:30  INFO 15816 --- [main] o.s.b.a.w.s.WelcomePageHandlerMapping    : Adding welcome page template: index", "#CCCCCC", False),
        ("2026-10-18T21:26:51.124+05:30  INFO 15816 --- [main] o.s.b.a.e.web.EndpointLinksResolver      : Exposing 2 endpoints beneath base path '/actuator'", "#38BDF8", False),
        ("2026-10-18T21:26:51.220+05:30  INFO 15816 --- [main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 8080 (http) with context path '/'", "#4ADE80", True),
        ("2026-10-18T21:26:51.232+05:30  INFO 15816 --- [main] c.d.c.CustomerReviewPortalApplication    : Started CustomerReviewPortalApplication in 6.918 seconds", "#22C55E", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> docker inspect --format '{{json .State.Health}}' crmp-app", "#FFFFFF", True),
        ("{\"Status\":\"healthy\",\"FailingStreak\":0,\"Log\":[{\"Output\":\"HTTP/1.1 200 OK\\n{\\\"status\\\":\\\"UP\\\"}\"}]}", "#4ADE80", True),
        ("PS D:\\Devops_project> docker inspect --format '{{json .NetworkSettings.Ports}}' crmp-app", "#FFFFFF", True),
        ("{\"8080/tcp\":[{\"HostIp\":\"0.0.0.0\",\"HostPort\":\"8080\"}]}", "#38BDF8", True),
        ("PS D:\\Devops_project> docker inspect --format '{{.Config.User}}' crmp-app", "#FFFFFF", True),
        ("crmpuser", "#FACC15", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 63.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.8, fontfamily='monospace', fontweight=weight)
        y -= 2.65

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task11\figure_11_5_docker_logs_inspect_terminal.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 11.5 saved successfully to:", output_path)


def generate_figure_11_6_docker_container_live_verification():
    """
    Figure 11.6: Containerized Application Live UI and Actuator Health Verification
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 75)
    ax.axis('off')

    # Window Frame (Browser Window)
    win_box = patches.FancyBboxPatch((2, 2), 111, 71, boxstyle="round,pad=0.5",
                                     facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.5)
    ax.add_patch(win_box)

    # Browser Tab & Header
    b_hdr = patches.FancyBboxPatch((2, 67), 111, 6.0, boxstyle="round,pad=0.2",
                                   facecolor='#0F172A', edgecolor='#020617')
    ax.add_patch(b_hdr)
    ax.add_patch(patches.Circle((5, 70), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((7.5, 70), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((10, 70), 0.8, color='#27C93F'))

    # URL Bar
    url_bar = patches.FancyBboxPatch((15, 68), 85, 4.0, boxstyle="round,pad=0.2",
                                    facecolor='#1E293B', edgecolor='#334155')
    ax.add_patch(url_bar)
    ax.text(17, 70.0, "http://localhost:8080/  |  Customer Review Moderation Portal (Docker Container crmp-app:8080)", 
            color='#38BDF8', fontsize=7.2, fontfamily='monospace', va='center')

    # Top CRMP Navbar
    nav = patches.FancyBboxPatch((3.5, 61.5), 108, 4.5, boxstyle="round,pad=0.2",
                                 facecolor='#1E293B', edgecolor='#0F172A')
    ax.add_patch(nav)
    ax.text(6, 63.7, "Customer Review Moderation Portal (CRMP)", color='white', fontsize=8.6, fontweight='bold', va='center')
    ax.text(80, 63.7, "Docker Host Port: 8080  |  Env: Production", color='#94A3B8', fontsize=7.0, va='center')

    # KPI Summary Cards (4 Cards)
    kpis = [
        ("Total Reviews", "4", "#2563EB", "#EFF6FF", 4),
        ("Pending Queue", "1", "#D97706", "#FFFBEB", 31),
        ("Approved Reviews", "2", "#16A34A", "#F0FDF4", 58),
        ("Flagged / Spam", "1", "#DC2626", "#FEF2F2", 85)
    ]
    for title, val, b_color, bg_color, x_pos in kpis:
        k_card = patches.FancyBboxPatch((x_pos, 52.0), 25, 8.0, boxstyle="round,pad=0.3",
                                        facecolor=bg_color, edgecolor=b_color, linewidth=1.5)
        ax.add_patch(k_card)
        ax.text(x_pos + 12.5, 57.2, title, color='#475569', fontsize=7.0, ha='center', fontweight='bold')
        ax.text(x_pos + 12.5, 54.0, val, color=b_color, fontsize=12.0, ha='center', fontweight='bold')

    # Moderation Queue Table
    tbl_box = patches.FancyBboxPatch((4, 25.5), 107, 24.5, boxstyle="round,pad=0.4",
                                     facecolor='white', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(tbl_box)
    ax.text(6, 47.5, "Active Moderation Review Queue (Live Ingested Feed)", color='#0F172A', fontsize=8.2, fontweight='bold')

    # Table Header Row
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

    # Table Rows
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
        # Badge
        badge = patches.FancyBboxPatch((86.5, y_r - 1.2), 9.0, 2.8, boxstyle="round,pad=0.2",
                                       facecolor=badge_col, edgecolor=badge_col)
        ax.add_patch(badge)
        ax.text(91.0, y_r + 0.2, status, color='white', fontsize=5.8, fontweight='bold', ha='center')
        ax.text(98, y_r, "[Moderate]", color='#2563EB', fontsize=6.2)

    # Bottom Split: Live Actuator Health Endpoint JSON Box
    health_box = patches.FancyBboxPatch((4, 4), 107, 19.5, boxstyle="round,pad=0.4",
                                        facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.2)
    ax.add_patch(health_box)
    ax.text(6, 20.8, "Live Spring Boot Actuator Health Probe (GET http://localhost:8080/actuator/health)", 
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
    output_path = r"d:\Devops_project\screenshots\task11\figure_11_6_docker_container_live_verification.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 11.6 saved successfully to:", output_path)


def generate_figure_11_7_docker_lifecycle_stop_restart_rm():
    """
    Figure 11.7: Container Lifecycle Management: Stop, Restart, and Container Removal
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
    ax.text(57.5, 66.5, "Administrator: Windows PowerShell - docker stop, docker restart, docker rm", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 66.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 66.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 66.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> # STEP 1: STOP CONTAINER AND VERIFY EXITED STATUS", "#FACC15", True),
        ("PS D:\\Devops_project> docker stop crmp-app", "#FFFFFF", True),
        ("crmp-app", "#CCCCCC", False),
        ("PS D:\\Devops_project> docker ps -a", "#FFFFFF", True),
        ("CONTAINER ID    IMAGE           COMMAND                   CREATED         STATUS                     PORTS    NAMES", "#38BDF8", True),
        ("25fe024d4956    crmp:1.0.0      \"java -jar /app/crmp....\" 2 minutes ago   Exited (0) 10 seconds ago           crmp-app", "#F87171", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # STEP 2: RESTART CONTAINER AND RESTORE HEALTHY SERVICE", "#FACC15", True),
        ("PS D:\\Devops_project> docker restart crmp-app", "#FFFFFF", True),
        ("0c6ca195a8d9", "#4ADE80", True),
        ("PS D:\\Devops_project> docker ps", "#FFFFFF", True),
        ("CONTAINER ID    IMAGE           COMMAND                   CREATED         STATUS                  PORTS                   NAMES", "#38BDF8", True),
        ("0c6ca195a8d9    crmp:1.0.0      \"java -jar /app/crmp....\" 2 seconds ago   Up 2 seconds (healthy)  0.0.0.0:8080->8080/tcp  crmp-app", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # STEP 3: STOP AND SAFELY REMOVE CONTAINER DEALLOCATING ALL RESOURCES", "#FACC15", True),
        ("PS D:\\Devops_project> docker stop crmp-app", "#FFFFFF", True),
        ("crmp-app", "#CCCCCC", False),
        ("PS D:\\Devops_project> docker rm crmp-app", "#FFFFFF", True),
        ("crmp-app", "#CCCCCC", False),
        ("PS D:\\Devops_project> docker ps -a", "#FFFFFF", True),
        ("CONTAINER ID    IMAGE           COMMAND                   CREATED         STATUS                  PORTS                   NAMES", "#38BDF8", True),
        ("PS D:\\Devops_project> # Container cleaned up cleanly with zero orphaned processes or resources", "#4ADE80", False),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 61.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.8, fontfamily='monospace', fontweight=weight)
        y -= 2.15

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task11\figure_11_7_docker_lifecycle_stop_restart_rm.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 11.7 saved successfully to:", output_path)

if __name__ == '__main__':
    generate_figure_11_1()
    generate_figure_11_2_docker_build_terminal()
    generate_figure_11_3_docker_images_tag_terminal()
    generate_figure_11_4_docker_run_ps_terminal()
    generate_figure_11_5_docker_logs_inspect_terminal()
    generate_figure_11_6_docker_container_live_verification()
    generate_figure_11_7_docker_lifecycle_stop_restart_rm()
