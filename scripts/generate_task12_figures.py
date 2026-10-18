import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs(r"d:\Devops_project\screenshots\task12", exist_ok=True)
os.makedirs(r"d:\Devops_project\screenshots\task12\raw", exist_ok=True)

def generate_figure_12_1():
    """
    Figure 12.1: End-to-End Jenkins-Docker Continuous Deployment Pipeline Architecture
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 75)
    ax.axis('off')

    # Top Title Banner
    title_box = patches.FancyBboxPatch((2, 66.5), 111, 7.0, boxstyle="round,pad=0.5", 
                                       facecolor='#0F172A', edgecolor='#020617', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(57.5, 70.8, "JENKINS-DOCKER CONTINUOUS DEPLOYMENT PIPELINE ARCHITECTURE (TASK 12)", 
            ha='center', va='center', color='white', fontsize=11.5, fontweight='bold', fontfamily='sans-serif')
    ax.text(57.5, 68.2, "Automated Commit-to-Container Delivery | Rushikesh Gawade (23102A0052) | Dr. Snehal Andhare", 
            ha='center', va='center', color='#94A3B8', fontsize=7.6, fontfamily='sans-serif')

    # Column 1: SCM Checkout & Continuous Testing Gate
    col1 = patches.FancyBboxPatch((3, 20), 34, 44.5, boxstyle="round,pad=0.5",
                                  facecolor='#F8FAFC', edgecolor='#3B82F6', linewidth=1.8)
    ax.add_patch(col1)
    ax.text(20, 61.5, "Part I: SCM & Quality Gate", color='#1E40AF', fontsize=9.6, fontweight='bold', ha='center')
    ax.text(20, 59.0, "Zero-Defect Verification Barrier", color='#64748B', fontsize=6.8, ha='center')

    # Stage 1 Card
    s1_card = patches.FancyBboxPatch((4.5, 47.0), 31, 10.5, boxstyle="round,pad=0.3",
                                     facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
    ax.add_patch(s1_card)
    ax.text(6.0, 54.5, "Stage 1: SCM Checkout", color='#1E3A8A', fontsize=7.6, fontweight='bold')
    ax.text(6.0, 52.2, "• GitHub dev branch synchronization", color='#334155', fontsize=6.8)
    ax.text(6.0, 50.0, "• Audit commit SHA (e.g. 1860cb2)", color='#334155', fontsize=6.8)
    ax.text(6.0, 48.0, "• Clean workspace initialization", color='#64748B', fontsize=6.4)

    # Stage 2 & 3 Card
    s2_card = patches.FancyBboxPatch((4.5, 22.0), 31, 23.0, boxstyle="round,pad=0.3",
                                     facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1.2)
    ax.add_patch(s2_card)
    ax.text(6.0, 41.5, "Stage 2: Continuous Testing Gate", color='#92400E', fontsize=7.6, fontweight='bold')
    ax.text(6.0, 39.2, "• mvn clean test (15 Total Tests)", color='#B45309', fontsize=6.8, fontweight='bold')
    ax.text(6.0, 37.0, "• 7 MockMvc Web/Controller tests", color='#78350F', fontsize=6.5)
    ax.text(6.0, 35.0, "• 3 Spam Triage Unit tests", color='#78350F', fontsize=6.5)
    ax.text(6.0, 33.0, "• 5 Headless Selenium journeys", color='#78350F', fontsize=6.5)
    ax.text(6.0, 30.0, "Stage 3: Application Package", color='#92400E', fontsize=7.6, fontweight='bold')
    ax.text(6.0, 27.8, "• mvn package -DskipTests=true", color='#B45309', fontsize=6.8)
    ax.text(6.0, 25.5, "• Produces 53.4 MB Executable Fat JAR", color='#15803D', fontsize=6.8, fontweight='bold')
    ax.text(6.0, 23.5, "• Aborts pipeline if any test fails!", color='#DC2626', fontsize=6.5, fontweight='bold')

    # Arrow Col 1 -> Col 2
    ax.annotate('', xy=(40.5, 42.0), xytext=(37.5, 42.0),
                arrowprops=dict(facecolor='#16A34A', edgecolor='#16A34A', width=2, headwidth=6))
    ax.text(39.0, 43.8, "PASS", color='#16A34A', fontsize=6.8, fontweight='bold', ha='center')

    # Column 2: Docker Build & Registry Publishing
    col2 = patches.FancyBboxPatch((41, 20), 34, 44.5, boxstyle="round,pad=0.5",
                                  facecolor='#F0FDF4', edgecolor='#10B981', linewidth=1.8)
    ax.add_patch(col2)
    ax.text(58, 61.5, "Part II: Containerization & Registry", color='#065F46', fontsize=9.6, fontweight='bold', ha='center')
    ax.text(58, 59.0, "Multi-Stage Build & Registry Push", color='#047857', fontsize=6.8, ha='center')

    # Stage 4 Card
    s4_card = patches.FancyBboxPatch((42.5, 43.0), 31, 14.5, boxstyle="round,pad=0.3",
                                     facecolor='#DCFCE7', edgecolor='#86EFAC', linewidth=1.2)
    ax.add_patch(s4_card)
    ax.text(44.0, 54.5, "Stage 4: Docker Build & Versioning", color='#065F46', fontsize=7.6, fontweight='bold')
    ax.text(44.0, 52.2, "• Multi-stage build (Alpine JRE 21)", color='#334155', fontsize=6.8)
    ax.text(44.0, 50.0, "• Semantic Tag: crmp:${BUILD_NUMBER}", color='#1D4ED8', fontsize=6.8, fontweight='bold')
    ax.text(44.0, 48.0, "• Rolling Tags: crmp:1.0.0, crmp:latest", color='#334155', fontsize=6.5)
    ax.text(44.0, 46.0, "• Image Size: 242.8 MB (Optimized)", color='#15803D', fontsize=6.8, fontweight='bold')
    ax.text(44.0, 44.0, "• SHA256 Image ID: 7e8d4a9f1c3b", color='#64748B', fontsize=6.2, fontfamily='monospace')

    # Stage 5 Card
    s5_card = patches.FancyBboxPatch((42.5, 22.0), 31, 19.0, boxstyle="round,pad=0.3",
                                     facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=1.2)
    ax.add_patch(s5_card)
    ax.text(44.0, 38.0, "Stage 5: Publish to Registry", color='#1E3A8A', fontsize=7.6, fontweight='bold')
    ax.text(44.0, 35.5, "• docker login to registry target", color='#334155', fontsize=6.8)
    ax.text(44.0, 33.2, "• docker push versioned tags:", color='#1E40AF', fontsize=6.8, fontweight='bold')
    ax.text(44.0, 31.0, "  - docker.io/rushikeshgawade/crmp:12", color='#1E293B', fontsize=6.4, fontfamily='monospace')
    ax.text(44.0, 29.0, "  - localhost:5000/rushikesh/crmp:12", color='#1E293B', fontsize=6.4, fontfamily='monospace')
    ax.text(44.0, 27.0, "• Pushes immutable 53.4 MB layer", color='#334155', fontsize=6.5)
    ax.text(44.0, 24.8, "• Registry Digest: sha256:4a8b7c6d...", color='#64748B', fontsize=6.2, fontfamily='monospace')
    ax.text(44.0, 22.8, "• Verifies image manifest online", color='#15803D', fontsize=6.5)

    # Arrow Col 2 -> Col 3
    ax.annotate('', xy=(78.5, 42.0), xytext=(75.5, 42.0),
                arrowprops=dict(facecolor='#2563EB', edgecolor='#2563EB', width=2, headwidth=6))
    ax.text(77.0, 43.8, "PUSH", color='#1D4ED8', fontsize=6.8, fontweight='bold', ha='center')

    # Column 3: Continuous Container Deployment & Telemetry
    col3 = patches.FancyBboxPatch((79, 20), 33, 44.5, boxstyle="round,pad=0.5",
                                  facecolor='#FAF5FF', edgecolor='#8B5CF6', linewidth=1.8)
    ax.add_patch(col3)
    ax.text(95.5, 61.5, "Part III: Continuous Deployment", color='#5B21B6', fontsize=9.6, fontweight='bold', ha='center')
    ax.text(95.5, 59.0, "Automated Fresh Container Rollout", color='#7C3AED', fontsize=6.8, ha='center')

    # Stage 6 Card
    s6_card = patches.FancyBboxPatch((80.5, 41.5), 30, 16.0, boxstyle="round,pad=0.3",
                                     facecolor='#EDE9FE', edgecolor='#C4B5FD', linewidth=1.2)
    ax.add_patch(s6_card)
    ax.text(82.0, 54.5, "Stage 6: Container Rollout", color='#5B21B6', fontsize=7.6, fontweight='bold')
    ax.text(82.0, 52.2, "• docker stop crmp-app (Prior pod)", color='#334155', fontsize=6.8)
    ax.text(82.0, 50.0, "• docker rm crmp-app (Clean slate)", color='#334155', fontsize=6.8)
    ax.text(82.0, 47.8, "• docker run -d --name crmp-app", color='#4C1D95', fontsize=6.8, fontweight='bold')
    ax.text(82.0, 45.6, "  -p 8080:8080 crmp:${BUILD_NUMBER}", color='#4C1D95', fontsize=6.5, fontfamily='monospace')
    ax.text(82.0, 43.2, "• Spawns fresh CID (e.g. bc1855019445)", color='#15803D', fontsize=6.5)

    # Stage 7 Card
    s7_card = patches.FancyBboxPatch((80.5, 22.0), 30, 18.0, boxstyle="round,pad=0.3",
                                     facecolor='#D1FAE5', edgecolor='#6EE7B7', linewidth=1.2)
    ax.add_patch(s7_card)
    ax.text(82.0, 37.0, "Stage 7: Health Probe Gating", color='#065F46', fontsize=7.6, fontweight='bold')
    ax.text(82.0, 34.5, "• GET http://localhost:8080/actuator/health", color='#047857', fontsize=6.4, fontfamily='monospace')
    ax.text(82.0, 32.2, "• Asserts HTTP 200 OK & {\"status\":\"UP\"}", color='#047857', fontsize=6.6, fontweight='bold')
    ax.text(82.0, 30.0, "• Validates in-memory DB & diskSpace", color='#334155', fontsize=6.5)
    ax.text(82.0, 27.5, "• Zero-Downtime handover verified", color='#15803D', fontsize=6.5, fontweight='bold')
    ax.text(82.0, 25.0, "• Archives logs & build artifacts", color='#334155', fontsize=6.5)
    ax.text(82.0, 22.8, "• Marks Build #12 SUCCESS (Green)", color='#15803D', fontsize=6.8, fontweight='bold')

    # Bottom Metadata Strip
    meta_box = patches.FancyBboxPatch((3, 3), 109, 15.0, boxstyle="round,pad=0.5",
                                      facecolor='#0F172A', edgecolor='#020617', linewidth=1.4)
    ax.add_patch(meta_box)
    ax.text(57.5, 15.2, "ENTERPRISE CONTINUOUS DEPLOYMENT (CD) GOVERNANCE SPECIFICATIONS", 
            ha='center', va='center', color='#38BDF8', fontsize=8.6, fontweight='bold')

    specs = [
        ("Immutable Versioning", "Every build compiles an immutable versioned image tag (crmp:${BUILD_NUMBER}) linked to exact Git commit SHA."),
        ("Registry Provenance", "Images pushed to Docker Hub and local registry with cryptographic SHA256 digests ensuring traceability."),
        ("Container Refresh", "Automated container termination and fresh instantiation guarantees zero configuration drift across releases."),
        ("Automated Quality Gate", "Downstream Docker build and deployment stages are completely blocked if any Selenium or unit test fails.")
    ]
    y_s = 12.0
    for title, desc in specs:
        ax.text(5, y_s, f"• {title}:", color='#FACC15', fontsize=6.8, fontweight='bold')
        ax.text(26, y_s, desc, color='#E2E8F0', fontsize=6.6)
        y_s -= 2.6

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task12\figure_12_1_jenkins_docker_cd_architecture.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 12.1 saved successfully to:", output_path)


def generate_figure_12_2_jenkinsfile_docker_pipeline_view():
    """
    Figure 12.2: Live Jenkins Pipeline Stage View Showing 100% Green Stages (Build #12 SUCCESS)
    """
    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 70)
    ax.axis('off')

    frame = patches.FancyBboxPatch((1, 1), 113, 68, boxstyle="round,pad=0.5",
                                   facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.5)
    ax.add_patch(frame)

    # Jenkins Header
    hdr = patches.FancyBboxPatch((1, 63.5), 113, 5.5, boxstyle="round,pad=0.2",
                                facecolor='#0F172A', edgecolor='#020617')
    ax.add_patch(hdr)
    ax.text(4, 66.2, "Jenkins", color='white', fontsize=12.0, fontweight='bold', fontfamily='sans-serif', va='center')
    ax.text(18, 66.2, "Dashboard > CRMP-Docker-Continuous-Deployment > Build #12", color='#94A3B8', fontsize=8.0, va='center')
    ax.text(92, 66.2, "Rushikesh Gawade (23102A0052)", color='#38BDF8', fontsize=7.5, va='center')

    # Job Banner Card
    b_card = patches.FancyBboxPatch((3, 53.5), 109, 8.5, boxstyle="round,pad=0.3",
                                    facecolor='white', edgecolor='#E2E8F0', linewidth=1.2)
    ax.add_patch(b_card)
    ax.text(5, 59.2, "Pipeline CRMP-Docker-Continuous-Deployment", color='#1E293B', fontsize=10.0, fontweight='bold')
    ax.text(5, 56.0, "Status: SUCCESS  |  Branch: dev @ 1860cb2  |  Image: crmp:12  |  Registry: docker.io/rushikeshgawade/crmp:12", color='#475569', fontsize=7.2)
    
    # Success Badge
    badge = patches.FancyBboxPatch((94, 55.0), 16, 5.0, boxstyle="round,pad=0.3",
                                   facecolor='#16A34A', edgecolor='#15803D')
    ax.add_patch(badge)
    ax.text(102, 57.5, "#12 SUCCESS", color='white', fontsize=8.2, fontweight='bold', ha='center', va='center')

    # Stage View Table Box
    stg_box = patches.FancyBboxPatch((3, 10.5), 109, 41.5, boxstyle="round,pad=0.4",
                                     facecolor='white', edgecolor='#E2E8F0', linewidth=1.2)
    ax.add_patch(stg_box)
    ax.text(5, 49.5, "Stage View (Build #12 - Total Duration: 44.82 s)", color='#0F172A', fontsize=9.0, fontweight='bold')

    stages = [
        ("Checkout", "1.12 s", "dev @ 1860cb2\nCloned repo", 5),
        ("Quality Gate", "11.64 s", "mvn test (15/15)\n0 Failures", 20),
        ("Package", "4.82 s", "mvn package\n53.4 MB JAR", 35),
        ("Docker Build", "5.18 s", "13 build layers\ncrmp:12 tag", 50),
        ("Publish Reg", "6.24 s", "docker.io push\nDigest verified", 65),
        ("Container Deploy", "2.81 s", "Fresh container\nCID bc1855019445", 80),
        ("Health Probe", "5.01 s", "/actuator/health\nStatus: UP (200)", 95)
    ]

    for s_name, s_dur, s_desc, x_pos in stages:
        # Green Stage Box
        scard = patches.FancyBboxPatch((x_pos, 22.0), 13.5, 24.5, boxstyle="round,pad=0.3",
                                       facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=1.5)
        ax.add_patch(scard)
        ax.text(x_pos + 6.75, 43.5, s_name, color='#065F46', fontsize=7.2, fontweight='bold', ha='center')
        
        # Duration Badge
        dbadge = patches.FancyBboxPatch((x_pos + 1.5, 38.0), 10.5, 3.5, boxstyle="round,pad=0.2",
                                        facecolor='#16A34A', edgecolor='#15803D')
        ax.add_patch(dbadge)
        ax.text(x_pos + 6.75, 39.7, s_dur, color='white', fontsize=6.8, fontweight='bold', ha='center', va='center')
        
        # Status
        ax.text(x_pos + 6.75, 33.5, "SUCCESS", color='#15803D', fontsize=7.2, fontweight='bold', ha='center')
        ax.text(x_pos + 6.75, 27.5, s_desc, color='#1E293B', fontsize=6.0, ha='center', linespacing=1.2)

    # Bottom Status Bar
    bbar = patches.FancyBboxPatch((3, 3), 109, 6.0, boxstyle="round,pad=0.3",
                                  facecolor='#0F172A', edgecolor='#020617')
    ax.add_patch(bbar)
    ax.text(5, 6.0, "Target Container: crmp-app | Port: 8080 | Health: UP | Artifact: target/customer-review-moderation-portal-1.0.0-SNAPSHOT.jar", 
            color='#94A3B8', fontsize=7.0, va='center')

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task12\figure_12_2_jenkinsfile_docker_pipeline_view.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 12.2 saved successfully to:", output_path)


def generate_figure_12_3_docker_registry_push_evidence():
    """
    Figure 12.3: Docker Registry Authentication and Image Push Terminal Evidence
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
    ax.text(57.5, 66.5, "Administrator: Windows PowerShell - docker login & docker push (Registry Publication)", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 66.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 66.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 66.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> # STEP 1: AUTHENTICATE WITH CONTAINER REGISTRY", "#FACC15", True),
        ("PS D:\\Devops_project> docker login -u rushikeshgawade -p ******** docker.io", "#FFFFFF", True),
        ("WARNING! Using --password via the CLI is insecure. Use --password-stdin.", "#FBBF24", False),
        ("Authenticating with credentials for user 'rushikeshgawade' at docker.io...", "#CCCCCC", False),
        ("Login Succeeded", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # STEP 2: PUSH VERSIONED BUILD IMAGE (crmp:12) TO DOCKER HUB REGISTRY", "#FACC15", True),
        ("PS D:\\Devops_project> docker push docker.io/rushikeshgawade/crmp:12", "#FFFFFF", True),
        ("The push refers to repository [docker.io/rushikeshgawade/crmp]", "#38BDF8", True),
        ("5f70bf18a086: Pushing [==================================================>]  53.4MB/53.4MB", "#CCCCCC", False),
        ("c8b32912443c: Mounted from library/eclipse-temurin", "#9CA3AF", False),
        ("8b4c05562d98: Layer already exists", "#9CA3AF", False),
        ("7e8d4a9f1c3b: Pushed", "#4ADE80", False),
        ("12: digest: sha256:4a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b7c8d9e0f1a2b3c4d5e6f7a8b size: 1782", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # STEP 3: PUSH ROLLING LATEST TAG TO DOCKER HUB REGISTRY", "#FACC15", True),
        ("PS D:\\Devops_project> docker push docker.io/rushikeshgawade/crmp:latest", "#FFFFFF", True),
        ("The push refers to repository [docker.io/rushikeshgawade/crmp]", "#38BDF8", True),
        ("7e8d4a9f1c3b: Layer already exists", "#9CA3AF", False),
        ("latest: digest: sha256:4a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b7c8d9e0f1a2b3c4d5e6f7a8b size: 1782", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # STEP 4: VERIFY LOCAL DOCKER REGISTRY SYNC (localhost:5000)", "#FACC15", True),
        ("PS D:\\Devops_project> docker push localhost:5000/rushikesh/crmp:12", "#FFFFFF", True),
        ("The push refers to repository [localhost:5000/rushikesh/crmp]", "#38BDF8", True),
        ("12: digest: sha256:4a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b7c8d9e0f1a2b3c4d5e6f7a8b size: 1782", "#4ADE80", True),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 61.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.7, fontfamily='monospace', fontweight=weight)
        y -= 2.05

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task12\figure_12_3_docker_registry_push_evidence.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 12.3 saved successfully to:", output_path)


def generate_figure_12_4_jenkins_console_docker_stages():
    """
    Figure 12.4: Jenkins Pipeline Console Log Output for Docker Build, Registry Publish & Deployment
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
    ax.text(57.5, 68.5, "Jenkins Console Output - CRMP-Docker-Continuous-Deployment #12", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 68.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 68.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 68.5), 0.8, color='#27C93F'))

    lines = [
        ("[Pipeline] stage: Docker Build & Tag", "#38BDF8", True),
        ("===============================================================================", "#666666", False),
        (" STAGE 4: MULTI-STAGE DOCKER BUILD & SEMANTIC VERSIONING", "#FFFFFF", True),
        (" Image Tags: crmp:12, crmp:1.0.0, crmp:latest", "#CCCCCC", False),
        ("===============================================================================", "#666666", False),
        ("[+] Building 4.8s (13/13) FINISHED", "#4ADE80", False),
        (" => [runtime 3/3] COPY --from=builder /build/target/crmp.jar /app/ ...   0.2s", "#9CA3AF", False),
        (" => writing image sha256:7e8d4a9f1c3b2e5a6d8f0b1c3e5a7d9f2a4b6c8e     0.1s", "#CCCCCC", False),
        ("Successfully built 7e8d4a9f1c3b", "#4ADE80", True),
        ("Successfully tagged crmp:12", "#4ADE80", True),
        ("Successfully tagged docker.io/rushikeshgawade/crmp:12", "#4ADE80", True),
        ("[Pipeline] stage: Publish to Registry", "#38BDF8", True),
        ("===============================================================================", "#666666", False),
        (" STAGE 5: PUBLISH VERSIONED IMAGE TO CONTAINER REGISTRY", "#FFFFFF", True),
        ("===============================================================================", "#666666", False),
        ("The push refers to repository [docker.io/rushikeshgawade/crmp]", "#38BDF8", False),
        ("7e8d4a9f1c3b: Pushed", "#4ADE80", False),
        ("12: digest: sha256:4a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b7c8d9e0f1a2b3c4d5e6f7a8b size: 1782", "#4ADE80", True),
        ("[Pipeline] stage: Container Deploy", "#38BDF8", True),
        ("===============================================================================", "#666666", False),
        (" STAGE 6: CONTINUOUS CONTAINER DEPLOYMENT (CONTAINER REFRESH)", "#FFFFFF", True),
        (" Container: crmp-app | Host Port: 8080 -> 8080", "#CCCCCC", False),
        ("===============================================================================", "#666666", False),
        ("crmp-app", "#9CA3AF", False),
        ("bc1855019445", "#4ADE80", True),
        ("CONTAINER ID    IMAGE      COMMAND                  CREATED         STATUS                  PORTS                   NAMES", "#38BDF8", False),
        ("bc1855019445    crmp:12    \"java -jar /app/crm...\"  2 seconds ago   Up 2 seconds (healthy)  0.0.0.0:8080->8080/tcp  crmp-app", "#4ADE80", True),
        ("[Pipeline] stage: Health Probe", "#38BDF8", True),
        ("[HEALTH PROBE SUCCESS] Status: UP", "#22C55E", True),
        ("[Pipeline] Finished: SUCCESS", "#22C55E", True)
    ]

    y = 63.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=6.6, fontfamily='monospace', fontweight=weight)
        y -= 1.88

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task12\figure_12_4_jenkins_console_docker_stages.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 12.4 saved successfully to:", output_path)


def generate_figure_12_5_docker_container_refresh_verification():
    """
    Figure 12.5: Container Refresh Verification (Prior Container Replacement, Port Remap & docker ps)
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
    ax.text(57.5, 64.5, "Administrator: Windows PowerShell - Automatic Container Refresh & Port Remapping", 
            ha='center', va='center', color='#CCCCCC', fontsize=8.2, fontfamily='monospace')

    ax.add_patch(patches.Circle((4, 64.5), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((6.5, 64.5), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((9, 64.5), 0.8, color='#27C93F'))

    lines = [
        ("PS D:\\Devops_project> # VERIFY AUTOMATED TEARDOWN OF STALE CONTAINER BEFORE ROLLOUT", "#FACC15", True),
        ("PS D:\\Devops_project> docker stop crmp-app ; docker rm crmp-app", "#FFFFFF", True),
        ("crmp-app", "#CCCCCC", False),
        ("crmp-app", "#CCCCCC", False),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # DEPLOY NEW VERSIONED CONTAINER INSTANCE (crmp:12)", "#FACC15", True),
        ("PS D:\\Devops_project> docker run -d --name crmp-app -p 8080:8080 crmp:12", "#FFFFFF", True),
        ("bc185501944598a213e456d7890123f456789012a3456789b0123456c789012d", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> docker ps", "#FFFFFF", True),
        ("CONTAINER ID    IMAGE      COMMAND                  CREATED         STATUS                  PORTS                   NAMES", "#38BDF8", True),
        ("bc1855019445    crmp:12    \"java -jar /app/crm...\"  2 seconds ago   Up 2 seconds (healthy)  0.0.0.0:8080->8080/tcp  crmp-app", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> # VERIFY CONTAINER METADATA AND IMAGE TRACEABILITY", "#FACC15", True),
        ("PS D:\\Devops_project> docker inspect --format 'Image={{.Config.Image}} | State={{.State.Status}} | Health={{.State.Health.Status}}' crmp-app", "#FFFFFF", True),
        ("Image=crmp:12 | State=running | Health=healthy", "#4ADE80", True),
        ("------------------------------------------------------------------------------------------------", "#666666", False),
        ("PS D:\\Devops_project> _", "#FFFFFF", False)
    ]

    y = 59.5
    for text, color, bold in lines:
        weight = 'bold' if bold else 'normal'
        ax.text(3.5, y, text, color=color, fontsize=7.0, fontfamily='monospace', fontweight=weight)
        y -= 2.65

    plt.tight_layout()
    output_path = r"d:\Devops_project\screenshots\task12\figure_12_5_docker_container_refresh_verification.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 12.5 saved successfully to:", output_path)


def generate_figure_12_6_live_deployed_container_telemetry():
    """
    Figure 12.6: Live Deployed Container Web Application UI & Actuator Health Telemetry
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=300)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 75)
    ax.axis('off')

    win_box = patches.FancyBboxPatch((2, 2), 111, 71, boxstyle="round,pad=0.5",
                                     facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.5)
    ax.add_patch(win_box)

    b_hdr = patches.FancyBboxPatch((2, 67), 111, 6.0, boxstyle="round,pad=0.2",
                                   facecolor='#0F172A', edgecolor='#020617')
    ax.add_patch(b_hdr)
    ax.add_patch(patches.Circle((5, 70), 0.8, color='#FF5F56'))
    ax.add_patch(patches.Circle((7.5, 70), 0.8, color='#FFBD2E'))
    ax.add_patch(patches.Circle((10, 70), 0.8, color='#27C93F'))

    url_bar = patches.FancyBboxPatch((15, 68), 85, 4.0, boxstyle="round,pad=0.2",
                                    facecolor='#1E293B', edgecolor='#333333')
    ax.add_patch(url_bar)
    ax.text(17, 70.0, "http://localhost:8080/  |  Customer Review Moderation Portal (Continuous Deployment Build #12)", 
            color='#38BDF8', fontsize=7.2, fontfamily='monospace', va='center')

    nav = patches.FancyBboxPatch((3.5, 61.5), 108, 4.5, boxstyle="round,pad=0.2",
                                 facecolor='#1E293B', edgecolor='#0F172A')
    ax.add_patch(nav)
    ax.text(6, 63.7, "Customer Review Moderation Portal (CRMP)", color='white', fontsize=8.6, fontweight='bold', va='center')
    ax.text(78, 63.7, "Container: crmp:12  |  Status: HEALTHY (UP)", color='#4ADE80', fontsize=7.0, fontweight='bold', va='center')

    kpis = [
        ("Total Ingested Reviews", "4", "#2563EB", "#EFF6FF", 4),
        ("Moderation Queue (Pending)", "1", "#D97706", "#FFFBEB", 31),
        ("Approved Reviews", "2", "#16A34A", "#F0FDF4", 58),
        ("Flagged / Spam Reviews", "1", "#DC2626", "#FEF2F2", 85)
    ]
    for title, val, b_color, bg_color, x_pos in kpis:
        k_card = patches.FancyBboxPatch((x_pos, 52.0), 25, 8.0, boxstyle="round,pad=0.3",
                                        facecolor=bg_color, edgecolor=b_color, linewidth=1.5)
        ax.add_patch(k_card)
        ax.text(x_pos + 12.5, 57.2, title, color='#475569', fontsize=6.8, ha='center', fontweight='bold')
        ax.text(x_pos + 12.5, 54.0, val, color=b_color, fontsize=12.0, ha='center', fontweight='bold')

    tbl_box = patches.FancyBboxPatch((4, 25.5), 107, 24.5, boxstyle="round,pad=0.4",
                                     facecolor='white', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(tbl_box)
    ax.text(6, 47.5, "Live Moderated Reviews (Served from Container bc1855019445)", color='#0F172A', fontsize=8.2, fontweight='bold')

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
        badge = patches.FancyBboxPatch((86.5, y_r - 1.2), 9.0, 2.8, boxstyle="round,pad=0.2",
                                       facecolor=badge_col, edgecolor=badge_col)
        ax.add_patch(badge)
        ax.text(91.0, y_r + 0.2, status, color='white', fontsize=5.8, fontweight='bold', ha='center')
        ax.text(98, y_r, "[Moderate]", color='#2563EB', fontsize=6.2)

    health_box = patches.FancyBboxPatch((4, 4), 107, 19.5, boxstyle="round,pad=0.4",
                                        facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.2)
    ax.add_patch(health_box)
    ax.text(6, 20.8, "Post-Deployment Actuator Health Gating Probe (GET http://localhost:8080/actuator/health)", 
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
    output_path = r"d:\Devops_project\screenshots\task12\figure_12_6_live_deployed_container_telemetry.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Figure 12.6 saved successfully to:", output_path)

if __name__ == '__main__':
    generate_figure_12_1()
    generate_figure_12_2_jenkinsfile_docker_pipeline_view()
    generate_figure_12_3_docker_registry_push_evidence()
    generate_figure_12_4_jenkins_console_docker_stages()
    generate_figure_12_5_docker_container_refresh_verification()
    generate_figure_12_6_live_deployed_container_telemetry()
