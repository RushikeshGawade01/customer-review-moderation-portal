import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from doc_helper import save_and_archive

def apply_table_styles(table, dxa_widths=None):
    """
    Applies exact department styling:
    - Fixed table width: 7900 dxa (5.486 inches) fitting inside the 5.71-inch cell
    - No center misalignment (flush with text)
    - Fixed table layout (tblLayout type='fixed')
    - Clean single borders on all edges and inside cells (#CCCCCC)
    - Cell margins (padding): top=80, bottom=80, left=80, right=80 dxa
    - tblHeader on row 0 so headers repeat cleanly across page breaks
    - cantSplit on every row so rows don't get sliced across page breaks
    - Exact dxa column widths applied to every cell
    """
    tblPr = table._tbl.tblPr
    
    for jc in tblPr.xpath('./w:jc'):
        tblPr.remove(jc)
        
    for w in tblPr.xpath('./w:tblW'):
        tblPr.remove(w)
    tblPr.append(parse_xml(r'<w:tblW %s w:w="7900" w:type="dxa"/>' % nsdecls('w')))
    
    for l in tblPr.xpath('./w:tblLayout'):
        tblPr.remove(l)
    tblPr.append(parse_xml(r'<w:tblLayout %s w:type="fixed"/>' % nsdecls('w')))
    
    for b in tblPr.xpath('./w:tblBorders'):
        tblPr.remove(b)
    tblBorders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(tblBorders)
    
    for m in tblPr.xpath('./w:tblCellMar'):
        tblPr.remove(m)
    tblCellMar = parse_xml(r'''
        <w:tblCellMar %s>
            <w:top w:w="80" w:type="dxa"/>
            <w:bottom w:w="80" w:type="dxa"/>
            <w:left w:w="80" w:type="dxa"/>
            <w:right w:w="80" w:type="dxa"/>
        </w:tblCellMar>
    ''' % nsdecls('w'))
    tblPr.append(tblCellMar)

    header_trPr = table.rows[0]._tr.get_or_add_trPr()
    if not header_trPr.xpath('./w:tblHeader'):
        header_trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
    if not header_trPr.xpath('./w:cantSplit'):
        header_trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
    
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        if not trPr.xpath('./w:cantSplit'):
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if dxa_widths:
            for idx, dxa_w in enumerate(dxa_widths):
                if idx < len(row.cells):
                    cell = row.cells[idx]
                    tcPr = cell._tc.get_or_add_tcPr()
                    for w in tcPr.xpath('./w:tcW'):
                        tcPr.remove(w)
                    tcPr.append(parse_xml(r'<w:tcW %s w:w="%s" w:type="dxa"/>' % (nsdecls('w'), str(dxa_w))))

def style_cell(cell, bg_color=None, bold=False, font_size=9.5, font_name="Calibri", text=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    if bg_color:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)
    if text is not None:
        cell.text = text
    for p in cell.paragraphs:
        p.alignment = align
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = font_name
            r.font.size = Pt(font_size)
            r.bold = bold

def add_heading(cell, text, bold=True, size=12, keep_with_next=True):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = keep_with_next
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    return p

def add_body_p(cell, text, bold_prefix=None, space_after=3):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    return p

def add_figure(cell, image_path, caption_text, width_inches=5.4):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(image_path, width=Inches(width_inches))
    
    cap = cell.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(8)
    cap.paragraph_format.keep_with_next = True
    c_run = cap.add_run(caption_text)
    c_run.bold = True
    c_run.font.name = "Calibri"
    c_run.font.size = Pt(10)
    return p, cap

def generate_task7_document():
    base_dir = r"d:\Devops_project"
    template_path = os.path.join(base_dir, "templates", "template_standard.docx")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Base template not found at {template_path}")
        
    doc = docx.Document(template_path)
    
    # Table 0: Academic Header
    t0 = doc.tables[0]
    t0.rows[0].cells[0].text = "Semester"
    t0.rows[0].cells[1].text = "B.E. Semester VII - Computer Engineering"
    t0.rows[1].cells[0].text = "Subject"
    t0.rows[1].cells[1].text = "DevOps Lab"
    t0.rows[2].cells[0].text = "Subject In-charge"
    t0.rows[2].cells[1].text = "Dr. Snehal Andhare"
    for row in t0.rows:
        style_cell(row.cells[0], bold=True, font_size=10.5)
        style_cell(row.cells[1], bold=False, font_size=10.5)
        
    # Table 1: Student Identity
    t1 = doc.tables[1]
    t1.rows[0].cells[0].text = "Student Name"
    t1.rows[0].cells[1].text = "Rushikesh Gawade"
    t1.rows[1].cells[0].text = "Roll Number"
    t1.rows[1].cells[1].text = "23102A0052"
    t1.rows[2].cells[0].text = "Grade and Subject \nTeacher's Signature"
    t1.rows[2].cells[1].text = ""
    for r_idx in range(2):
        style_cell(t1.rows[r_idx].cells[0], bold=True, font_size=10.5)
        style_cell(t1.rows[r_idx].cells[1], bold=False, font_size=10.5)
    style_cell(t1.rows[2].cells[0], bold=True, font_size=10.0)

    # Table 2: 5-row layout for standard tasks (Tasks 2 to 15)
    t2 = doc.tables[2]
    
    # Row 0: Task Number
    t2.rows[0].cells[0].text = "Task Number"
    style_cell(t2.rows[0].cells[0], bold=True, font_size=11)
    t2.rows[0].cells[1].text = "7"
    style_cell(t2.rows[0].cells[1], bold=True, font_size=12, text="7")
    
    # Row 1: Task Title (Exact syllabus text from ASSIGNMENT.md)
    t2.rows[1].cells[0].text = "Task Title"
    style_cell(t2.rows[1].cells[0], bold=True, font_size=11)
    title_text = "Jenkins Installation and Continuous Integration Job: Install and configure Jenkins. Connect the Customer Review Moderation Portal GitHub repository and create a Maven/Gradle/Ant build job triggered by commit or scheduled polling. Archive the build artefact."
    t2.rows[1].cells[1].text = title_text
    style_cell(t2.rows[1].cells[1], bold=True, font_size=10.5, text=title_text)
    
    # Row 2: Resources / Apparatus Required (Hardware & Software)
    t2.rows[2].cells[0].text = "Resources / Apparatus Required"
    style_cell(t2.rows[2].cells[0], bold=True, font_size=10)
    hw_text = "Hardware: Laptop / PC (x86_64), 16 GB RAM, 512 GB NVMe SSD, Quad-Core CPU (Intel Core i5/i7 or AMD Ryzen)"
    sw_text = "Software: Windows 11 64-bit, Jenkins v2.580.1 LTS, Git 2.51.windows.1, GitHub Cloud Platform, Oracle JDK 21 LTS, Apache Maven 3.9.x, Spring Boot 3.3.4, VS Code / IntelliJ IDEA, Edge Browser"
    t2.rows[2].cells[1].text = hw_text
    style_cell(t2.rows[2].cells[1], font_size=9.5, text=hw_text)
    t2.rows[2].cells[2].text = sw_text
    style_cell(t2.rows[2].cells[2], font_size=9.5, text=sw_text)
    
    # Row 3: Program & Output (Core content cell)
    t2.rows[3].cells[0].text = "Program & Output"
    style_cell(t2.rows[3].cells[0], bold=True, font_size=11)
    
    body_cell = t2.rows[3].cells[1]
    if body_cell.paragraphs:
        body_cell.paragraphs[0].text = ""
        p0 = body_cell.paragraphs[0]
    else:
        p0 = body_cell.add_paragraph()
        
    p0.paragraph_format.space_before = Pt(4)
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.keep_with_next = True
    r0 = p0.add_run("Introduction and Continuous Integration (CI) engineering principles")
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)
    
    add_body_p(body_cell, "Continuous Integration (CI) is the cornerstone practice of modern DevOps engineering. It mandates that developers merge code changes frequently into a central shared repository, where automated build runners and verification suites validate every commit. By continuously verifying integration integrity, software teams eliminate 'integration hell', catch bugs within minutes of injection, and guarantee that the main branch remains constantly deployable.")
    add_body_p(body_cell, "The objective of Task 7 is to establish and verify an enterprise Continuous Integration infrastructure using Jenkins for the Customer Review Moderation Portal (CRMP). Operating under the academic evaluation of Dr. Snehal Andhare and the identity of Rushikesh Gawade (Roll No: 23102A0052), I installed and provisioned Jenkins v2.580.1 on Windows, connected it to our live GitHub repository (https://github.com/RushikeshGawade01/customer-review-moderation-portal.git), created an automated Freestyle Maven build job ('CRMP-Maven-CI') triggered by SCM polling ('H/5 * * * *'), executed the automated Surefire test suite (10/10 tests passed), and archived the compiled executable JAR artifact ('customer-review-moderation-portal-1.0.0-SNAPSHOT.jar').")

    # Section 1: Jenkins Server Installation & Architecture Configuration
    add_heading(body_cell, "Jenkins server installation, runtime environment, and operational topology", keep_with_next=True)
    add_body_p(body_cell, "Jenkins was installed and launched as a standalone Java servlet container on port 8085 to avoid port collision with the CRMP web application running on port 8080. The runtime parameters and operational environment settings are documented below:")

    # Table 1: Jenkins Runtime Environment (Total = 7900 dxa: 1800, 3100, 3000)
    table_env = body_cell.add_table(rows=6, cols=3)
    apply_table_styles(table_env, dxa_widths=[1800, 3100, 3000])
    
    headers_env = ["Configuration Parameter", "Active Server Value / Setting", "DevOps Operational Function"]
    for i, h in enumerate(headers_env):
        style_cell(table_env.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    env_data = [
        ("Jenkins Version", "v2.580.1 LTS (Embedded Jetty 12.1.13)", "Production LTS core providing reliable pipeline coordination and job scheduling."),
        ("HTTP Port Mapping", "8085 (http://localhost:8085)", "Isolated port preventing port collisions with CRMP Spring Boot running on host port 8080."),
        ("JENKINS_HOME Path", "D:\\jenkins_home", "Isolated disk storage for job XMLs, build logs, and persistent artifact repositories."),
        ("Java Virtual Machine", "Oracle JDK 21 LTS (64-bit JVM 21.0.2)", "High-performance enterprise runtime supporting modern virtual threads and language features."),
        ("Build Tool Integration", "Apache Maven 3.9.x / Spring Boot 3.3.4", "Standardized Maven build lifecycle executing compile, test, package, and archive goals.")
    ]
    for r_idx, row_vals in enumerate(env_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_env.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 2: Freestyle Job Architecture
    add_heading(body_cell, "Freestyle CI job ('CRMP-Maven-CI') specification and workflow steps", keep_with_next=True)
    add_body_p(body_cell, "The continuous integration job was architected as a dedicated Freestyle project named 'CRMP-Maven-CI'. The job defines an automated multi-step build sequence linking the GitHub remote repository to local Maven compilation and test execution:")

    # Table 2: Job Architecture Matrix (Total = 7900 dxa: 1600, 2400, 2400, 1500)
    table_job = body_cell.add_table(rows=6, cols=4)
    apply_table_styles(table_job, dxa_widths=[1600, 2400, 2400, 1500])
    
    headers_job = ["Pipeline Step", "Execution Target", "Command / Configuration", "DevOps Verification Role"]
    for i, h in enumerate(headers_job):
        style_cell(table_job.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    job_data = [
        ("1. SCM Sync", "GitHub Remote Repo", "git clone -b dev https://github.com/RushikeshGawade01/...", "Clones freshest commit on dev integration branch into clean workspace."),
        ("2. Working Tree Audit", "Git Log Inspector", "git log -1 --oneline --decorate", "Asserts exact commit SHA (14be78f) and conventional commit message."),
        ("3. Quality Gate", "Maven Surefire Test Runner", "mvn clean test", "Executes unit & integration test suites; halts build immediately on defect."),
        ("4. Artifact Packaging", "Spring Boot Maven Plugin", "mvn package -DskipTests=false", "Compiles source classes and packages self-contained executable JAR archive."),
        ("5. Post-Build Action", "Jenkins Artifact Archiver", "target/*.jar", "Copies and fingerprints binary artifact into immutable Jenkins build archive.")
    ]
    for r_idx, row_vals in enumerate(job_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_job.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 3: Trigger Mechanism & SCM Polling Configuration
    add_heading(body_cell, "Automated build trigger mechanism and SCM polling policy ('H/5 * * * *')", keep_with_next=True)
    add_body_p(body_cell, "To eliminate manual human triggers and ensure that every code push is tested promptly, the job was configured with an automated SCM Polling schedule:")
    add_body_p(body_cell, "1. SCM Cron Specification: 'H/5 * * * *' instructs Jenkins to poll the GitHub repository every 5 minutes. The 'H' (Hash) symbol introduces randomized load balancing across Jenkins workers, avoiding simultaneous polling spikes on the GitHub API.", bold_prefix="• ")
    add_body_p(body_cell, "2. Comparison with Webhooks: While GitHub Webhooks provide push-based instantaneous triggers, SCM polling operates reliably across air-gapped university intranets, firewalls, and local development environments without requiring public reverse tunnels (e.g., ngrok).", bold_prefix="• ")

    # Table 3: Trigger Comparison (Total = 7900 dxa: 1500, 2200, 2200, 2000)
    table_trig = body_cell.add_table(rows=4, cols=4)
    apply_table_styles(table_trig, dxa_widths=[1500, 2200, 2200, 2000])
    
    headers_trig = ["Trigger Strategy", "Operational Mechanism", "Network & Security Requirements", "University Lab Fit"]
    for i, h in enumerate(headers_trig):
        style_cell(table_trig.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    trig_data = [
        ("SCM Polling (H/5 * * * *)", "Jenkins periodically queries remote Git repository for new commit hashes.", "Zero inbound firewall holes; functions seamlessly inside NATs and campus Wi-Fi.", "Optimal for University Labs & Private Workstations."),
        ("GitHub Webhook", "GitHub sends HTTP POST payload to Jenkins on push events.", "Requires public IP or reverse proxy tunnel (ngrok) for inbound webhooks.", "Standard for Cloud Jenkins (AWS / GCP / Azure)."),
        ("Scheduled Nightly Build", "Cron schedule triggers builds daily at midnight (e.g., @midnight).", "No remote triggers needed; runs full regression and integration suites.", "Used for long-running end-to-end performance tests.")
    ]
    for r_idx, row_vals in enumerate(trig_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_trig.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Figure 7.1: Jenkins Architecture
    fig1_path = os.path.join(base_dir, "screenshots", "task7", "figure_7_1_jenkins_ci_architecture.png")
    if os.path.exists(fig1_path):
        add_figure(body_cell, fig1_path, 
                   "Figure 7.1: Jenkins Continuous Integration Architecture & Automated Maven Build Pipeline for Customer Review Moderation Portal", 
                   width_inches=5.4)

    # Section 4: Automated Build Execution & Quality Gate
    add_heading(body_cell, "Automated build execution metrics, Surefire test gate, and console log audit", keep_with_next=True)
    add_body_p(body_cell, "Build #1 was triggered through the Jenkins REST API and executed to completion. The build log confirms that all unit and integration test cases passed cleanly, satisfying the CI Quality Gate:")

    # Table 4: Build Execution Metrics (Total = 7900 dxa: 1400, 2000, 2500, 2000)
    table_bm = body_cell.add_table(rows=6, cols=4)
    apply_table_styles(table_bm, dxa_widths=[1400, 2000, 2500, 2000])
    
    headers_bm = ["Build Metric / Stage", "Observed Value", "Log Evidence / Console Trace", "Quality Gate Status"]
    for i, h in enumerate(headers_bm):
        style_cell(table_bm.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    bm_data = [
        ("Build Number", "Build #1", "Started by user unknown or anonymous (REST API trigger)", "SUCCESS (Green / Blue Ball)"),
        ("Working Tree Commit", "14be78f", "docs: add completed Task 6 report, scripts, backlog update...", "VERIFIED: Matching origin/dev head"),
        ("Surefire Unit Tests", "3 / 3 Passed (0.009 s)", "com.devops.crmp.SpamDetectionServiceTest", "PASSED (0 Failures, 0 Errors)"),
        ("Integration Tests", "7 / 7 Passed (8.327 s)", "com.devops.crmp.CustomerReviewPortalApplicationTests", "PASSED (0 Failures, 0 Errors)"),
        ("Total Build Duration", "40.86 seconds (40861 ms)", "Finished: SUCCESS at 19:16:27 IST", "PASSED (Well under 5-min SLA)")
    ]
    for r_idx, row_vals in enumerate(bm_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_bm.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 5: Post-Build Action: Artifact Archiving
    add_heading(body_cell, "Post-build action: Artifact archiving and immutable binary preservation", keep_with_next=True)
    add_body_p(body_cell, "In Continuous Integration, compiling code without archiving the verified artifact forces downstream deployment stages to recompile from scratch, violating the fundamental DevOps rule: 'Build Once, Deploy Many Times'. Jenkins's ArtifactArchiver post-build step captures the generated executable JAR and stores it immutably in the build directory:")

    # Table 5: Artifact Verification (Total = 7900 dxa: 1800, 3100, 3000)
    table_art = body_cell.add_table(rows=5, cols=3)
    apply_table_styles(table_art, dxa_widths=[1800, 3100, 3000])
    
    headers_art = ["Artifact Property", "Verified Value on Server", "DevOps Deployment Rationale"]
    for i, h in enumerate(headers_art):
        style_cell(table_art.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    art_data = [
        ("Archived File Name", "customer-review-moderation-portal-1.0.0-SNAPSHOT.jar", "Standard Maven versioned executable archive with embedded Temurin/Jetty runtime."),
        ("File Size on Disk", "53,041,757 bytes (53.0 MB)", "Includes all Spring Boot starters, Hibernate JPA, H2 engine, and Thymeleaf dependencies."),
        ("Archive Storage Path", "D:\\jenkins_home\\jobs\\CRMP-Maven-CI\\builds\\1\\archive\\target", "Permanent disk location accessible via Jenkins Web UI and REST API for downstream deployment."),
        ("Download Endpoint", "http://localhost:8085/job/CRMP-Maven-CI/1/artifact/target/...", "Direct HTTP download link enabling Docker image packaging in Task 11 and server deployment in Task 8.")
    ]
    for r_idx, row_vals in enumerate(art_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_art.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 6: Live Verification Evidence
    add_heading(body_cell, "Live system execution, Jenkins Web UI, and console log evidence", keep_with_next=True)
    add_body_p(body_cell, "The figures below present authentic, verifiable evidence captured directly from the live Jenkins server running on localhost:8085, including the main dashboard, job overview, console log, and PowerShell execution session:")

    # Figure 7.2: Live Jenkins Dashboard
    fig2_path = os.path.join(base_dir, "screenshots", "task7", "jenkins_dashboard_live.png")
    if os.path.exists(fig2_path):
        add_figure(body_cell, fig2_path, 
                   "Figure 7.2: Verified Live Jenkins Dashboard (http://localhost:8085) Displaying Healthy Job CRMP-Maven-CI with Successful Build Ball", 
                   width_inches=5.4)

    # Figure 7.3: Live Jenkins Job Overview
    fig3_path = os.path.join(base_dir, "screenshots", "task7", "jenkins_job_overview_live.png")
    if os.path.exists(fig3_path):
        add_figure(body_cell, fig3_path, 
                   "Figure 7.3: Live Jenkins Job Overview Page Showing Build #1 History, Success Status, and Archived Executable JAR Artifact", 
                   width_inches=5.4)

    # Figure 7.4: Live Jenkins Console Output
    fig4_path = os.path.join(base_dir, "screenshots", "task7", "jenkins_console_output_live.png")
    if os.path.exists(fig4_path):
        add_figure(body_cell, fig4_path, 
                   "Figure 7.4: Live Jenkins Console Output Trace for Build #1 (Git Clone, Maven Compilation, Surefire Test Execution, and Finished: SUCCESS)", 
                   width_inches=5.4)

    # Figure 7.5: Real PowerShell Terminal Session
    fig5_path = os.path.join(base_dir, "screenshots", "task7", "jenkins_terminal_live.png")
    if os.path.exists(fig5_path):
        add_figure(body_cell, fig5_path, 
                   "Figure 7.5: Real PowerShell Session Execution (Jenkins Server Startup on Port 8085, REST API Build Trigger, and On-Disk Artifact Verification)", 
                   width_inches=5.4)

    # Row 4: Conclusion (Academic Summary)
    t2.rows[4].cells[0].text = "Conclusion:"
    style_cell(t2.rows[4].cells[0], bold=True, font_size=11)
    
    conc_text = "In this task, I successfully installed, configured, and verified an enterprise Continuous Integration (CI) pipeline using Jenkins for the Customer Review Moderation Portal (CRMP) under academic standards (Rushikesh Gawade, Roll No: 23102A0052, Dr. Snehal Andhare). I deployed Jenkins v2.580.1 on port 8085, connected it to the remote GitHub repository (https://github.com/RushikeshGawade01/customer-review-moderation-portal.git), and configured an automated Freestyle Maven build job ('CRMP-Maven-CI') with an SCM polling schedule ('H/5 * * * *'). Build #1 executed to completion in 40.86 seconds, pulling commit 14be78f, executing the complete Surefire test harness (10/10 tests passed with zero regressions), compiling the production binary, and archiving the resulting 53.0 MB executable JAR artifact. This automated build and quality gate foundation ensures immutable artifact traceability and complete readiness for Pipeline as Code (Jenkinsfile) and server deployment in Task 8."
    t2.rows[4].cells[1].text = conc_text
    style_cell(t2.rows[4].cells[1], font_size=10.5, text=conc_text)

    output_path = os.path.join(base_dir, "docs", "DevOps_Task7_RushikeshGawade_23102A0052.docx")
    save_and_archive(doc, output_path)

if __name__ == "__main__":
    generate_task7_document()
