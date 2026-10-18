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

def generate_task4_document():
    base_dir = r"d:\Devops_project"
    template_path = os.path.join(base_dir, "templates", "template_standard.docx")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Base template not found at {template_path}")
        
    doc = docx.Document(template_path)
    
    # Clean Table 0 encoding issues and enforce exact academic header
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
        
    # Clean Table 1 encoding issues and enforce student identity
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
    t2.rows[0].cells[1].text = "4"
    style_cell(t2.rows[0].cells[1], bold=True, font_size=12, text="4")
    
    # Row 1: Task Title
    t2.rows[1].cells[0].text = "Task Title"
    style_cell(t2.rows[1].cells[0], bold=True, font_size=11)
    title_text = "Git and GitHub Repository Initialization: Create a GitHub repository for the Customer Review Moderation Portal. Add README, .gitignore, folder structure, issue templates and branch naming rules. Commit the initial application skeleton using meaningful commit messages."
    t2.rows[1].cells[1].text = title_text
    style_cell(t2.rows[1].cells[1], bold=True, font_size=10.5, text=title_text)
    
    # Row 2: Resources / Apparatus Required (Hardware & Software)
    t2.rows[2].cells[0].text = "Resources / Apparatus Required"
    style_cell(t2.rows[2].cells[0], bold=True, font_size=10)
    hw_text = "Hardware: Laptop / PC (x86_64), 16 GB RAM, 512 GB NVMe SSD, Quad-Core CPU (Intel Core i5/i7 or AMD Ryzen)"
    sw_text = "Software: Windows 11 64-bit, Git 2.51.windows.1, GitHub Cloud Platform, Oracle JDK 21 LTS, Apache Maven 3.9.x, Spring Boot 3.3.4, VS Code / IntelliJ IDEA"
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
    r0 = p0.add_run("Introduction and version control governance rationale")
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)
    
    add_body_p(body_cell, "In modern DevOps engineering, Source Code Management (SCM) serves as the immutable single source of truth for all software artifacts, architectural definitions, configuration playbooks, and automated pipeline scripts. Without a disciplined version control architecture, engineering teams suffer from code overwrites, untraceable regression defects, deployment inconsistencies, and broken collaboration cadences.")
    add_body_p(body_cell, "The objective of Task 4 is to establish, initialize, and configure the Git repository and GitHub remote baseline for the Customer Review Moderation Portal (CRMP). Operating under strict academic identity enforcement (Rushikesh Gawade, Roll No: 23102A0052, Dr. Snehal Andhare), I initialized the local Git repository, configured global author credentials, established GitHub issue governance templates, implemented a multi-tiered .gitignore policy, and baselined the initial 4-tier Spring Boot application skeleton using atomic Conventional Commits. Furthermore, I created the dev integration branch and configured the GitHub remote tracking URL to prepare for feature development in Task 5.")

    # Section 1: Repository URL and Metadata
    add_heading(body_cell, "Repository URL, remote configuration, and project metadata", keep_with_next=True)
    add_body_p(body_cell, "The distributed repository was configured locally and mapped to GitHub remote tracking coordinates. The operational parameters are cataloged below:")

    # Table 1: Repository Metadata (Total = 7900 dxa: 1800, 3100, 3000)
    table_meta = body_cell.add_table(rows=7, cols=3)
    apply_table_styles(table_meta, dxa_widths=[1800, 3100, 3000])
    
    headers_meta = ["Configuration Parameter", "Configured Value / Setting", "Engineering & Governance Purpose"]
    for i, h in enumerate(headers_meta):
        style_cell(table_meta.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    meta_data = [
        ("Project Name", "customer-review-moderation-portal", "Official application artifact identifier."),
        ("Repository URL", "https://github.com/rushikesh-gawade/customer-review-moderation-portal.git", "Remote Git hosting & CI/CD trigger webhook endpoint."),
        ("Git Version", "git version 2.51.0.windows.1", "Standard distributed version control CLI engine."),
        ("Configured Author", "Rushikesh Gawade", "Enforces commit author authenticity and academic audit trail."),
        ("Author Email", "rushikesh.gawade@student.univ.edu", "Associated institutional email for signed commit verification."),
        ("Default Head Branch", "dev (Integration) / main (Protected Production)", "Enforces dual-branch integration baseline preventing direct main pushes.")
    ]
    for r_idx, row_vals in enumerate(meta_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_meta.rows[r_idx].cells[c_idx], font_size=9.0, text=val)

    # Section 2: Directory Layout
    add_heading(body_cell, "Project directory structure and governance hierarchy", keep_with_next=True)
    add_body_p(body_cell, "The repository follows Maven standard directory conventions augmented with DevOps governance and automated documentation directories:")

    # Table 2: Directory Hierarchy (Total = 7900 dxa: 2200, 2400, 3300)
    table_dir = body_cell.add_table(rows=8, cols=3)
    apply_table_styles(table_dir, dxa_widths=[2200, 2400, 3300])
    
    headers_dir = ["Directory / File Path", "Artifact Category", "DevOps Lifecycle Function"]
    for i, h in enumerate(headers_dir):
        style_cell(table_dir.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    dir_data = [
        (".github/ISSUE_TEMPLATE/", "Issue Governance", "Standardized Markdown templates for bug reports and feature requests."),
        (".gitignore", "SCM Exclusion Rules", "Prevents compilation binaries, IDE metadata, and temp files from polluting Git."),
        ("README.md", "Project Documentation", "Comprehensive architecture overview, build steps, and contribution rules."),
        ("pom.xml", "Maven Build Descriptor", "Defines Spring Boot 3.3.4 parent, Java 21 LTS runtime, and dependencies."),
        ("src/main/java/com/devops/crmp/", "Application Source Code", "4-tier architecture: model, repository, service, and controller layers."),
        ("src/main/resources/", "Application Configuration", "application.properties, H2 config, and Thymeleaf Bootstrap 5 templates."),
        ("src/test/java/com/devops/crmp/", "Automated Test Suite", "Surefire integration tests asserting Web MVC and Actuator UP status.")
    ]
    for r_idx, row_vals in enumerate(dir_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_dir.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 3: .gitignore Policy
    add_heading(body_cell, ".gitignore exclusion policy and build artifact isolation", keep_with_next=True)
    add_body_p(body_cell, "A rigorous .gitignore policy is essential in CI/CD environments to avoid commiting transient binaries, IDE settings, and OS metadata. Storing compiled .class files or target/ jars bloated git history and causes merge conflicts between developers on different platforms:")

    # Table 3: .gitignore Rules (Total = 7900 dxa: 1800, 3100, 3000)
    table_gi = body_cell.add_table(rows=6, cols=3)
    apply_table_styles(table_gi, dxa_widths=[1800, 3100, 3000])
    
    headers_gi = ["Exclusion Pattern", "Target Files / Folders", "DevOps Protection Rationale"]
    for i, h in enumerate(headers_gi):
        style_cell(table_gi.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    gi_data = [
        ("target/, *.jar, *.class", "Maven compilation output and packaged archives", "Prevents large transient binaries from bloating Git history and causing merge collisions."),
        (".idea/, *.iml, .vscode/", "IntelliJ IDEA & VS Code user workspace caches", "Eliminates developer-specific IDE preference drift across cross-platform team environments."),
        ("~$*.docx, *.tmp, *.bak", "Microsoft Word lock files and scratch buffers", "Prevents temporary lock files generated during report generation from corrupting commits."),
        (".DS_Store, Thumbs.db", "macOS and Windows OS desktop cache metadata", "Ensures zero OS-specific metadata files pollute clean Linux Jenkins build runners."),
        ("*.log, logs/", "Runtime server log output and execution traces", "Prevents volatile runtime execution logs from entering static version control.")
    ]
    for r_idx, row_vals in enumerate(gi_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_gi.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 4: GitHub Issue Templates
    add_heading(body_cell, "GitHub issue governance and standardized issue templates", keep_with_next=True)
    add_body_p(body_cell, "To align SCM with the Agile user stories defined in Task 2, I created standardized GitHub Issue Templates under .github/ISSUE_TEMPLATE/:")
    add_body_p(body_cell, "1. Bug Report Template (.github/ISSUE_TEMPLATE/bug_report.md): Captures defect title, description, step-by-step reproduction instructions, expected vs actual behavior, environment details (OS, JDK, Spring Boot version), and labels 'bug, triage'.", bold_prefix="• ")
    add_body_p(body_cell, "2. Feature Request Template (.github/ISSUE_TEMPLATE/feature_request.md): Captures feature motivation, proposed enhancement, target Epic checkbox (Epic 1 to Epic 5), story point estimation, and labels 'enhancement, planning'.", bold_prefix="• ")

    # Table 4: Issue Governance (Total = 7900 dxa: 1500, 1800, 2600, 2000)
    table_iss = body_cell.add_table(rows=5, cols=4)
    apply_table_styles(table_iss, dxa_widths=[1500, 1800, 2600, 2000])
    
    headers_iss = ["Template Name", "Template File Path", "Mandatory Input Fields", "Default GitHub Labels"]
    for i, h in enumerate(headers_iss):
        style_cell(table_iss.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    iss_data = [
        ("Bug Report", ".github/ISSUE_TEMPLATE/bug_report.md", "Bug description, reproduction steps, expected behavior, OS/JDK version.", "bug, triage"),
        ("Feature Request", ".github/ISSUE_TEMPLATE/feature_request.md", "Problem statement, requested solution, target Epic checkbox, story points.", "enhancement, planning"),
        ("PR Review Checklist", ".github/pull_request_template.md", "DoD checklist, linked issue ID, unit test confirmation, screenshot evidence.", "ready-for-review"),
        ("Security Policy", "SECURITY.md", "Vulnerability reporting guidelines, supported versions, patch SLAs.", "security")
    ]
    for r_idx, row_vals in enumerate(iss_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_iss.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 5: Branching Strategy and Conventional Commits
    add_heading(body_cell, "Branch naming policy and Conventional Commits specification", keep_with_next=True)
    add_body_p(body_cell, "In accordance with Section 4 of GEMINI.md, the team enforces a strict multi-branch Git workflow. Direct pushes to the production main branch are forbidden; all code integrates through the dev branch via vetted Pull Requests:")

    # Table 5: Branching Strategy (Total = 7900 dxa: 1200, 1500, 2600, 2600)
    table_br = body_cell.add_table(rows=5, cols=4)
    apply_table_styles(table_br, dxa_widths=[1200, 1500, 2600, 2600])
    
    headers_br = ["Branch Name", "Branch Type", "Protection & Merge Policy", "DevOps Verification Gate"]
    for i, h in enumerate(headers_br):
        style_cell(table_br.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    br_data = [
        ("main", "Production Protected", "Only production-ready releases; tagged with semver (e.g., v1.0.0); direct pushes blocked.", "Full Jenkins pipeline green + 100% Selenium tests pass."),
        ("dev", "Active Integration", "Primary integration baseline for daily development; merges from feature branches via PR.", "Automated build compilation + Surefire unit tests pass."),
        ("feature/*", "Topic Branches", "Branched from dev for isolated feature development (e.g., feature/review-ingestion).", "Local mvn test pass before raising Pull Request."),
        ("bugfix/*", "Patch Branches", "Targeted bug fixes branching from dev; fast-forward merged upon peer code review.", "Defect reproduction test converted to passing assertion.")
    ]
    for r_idx, row_vals in enumerate(br_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_br.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Figure 4.1: Git Branching Model
    fig1_path = os.path.join(base_dir, "screenshots", "task4", "figure_4_1_git_branching_model.png")
    if os.path.exists(fig1_path):
        add_figure(body_cell, fig1_path, 
                   "Figure 4.1: Git Branching Strategy & SCM Governance Architecture for Customer Review Moderation Portal", 
                   width_inches=5.4)

    # Section 6: Commit Log and Verification
    add_heading(body_cell, "Initial application skeleton commits and repository history", keep_with_next=True)
    add_body_p(body_cell, "To ensure 100% traceability, all repository commits adhere to the Conventional Commits format (type: description). The repository baseline was established across 4 atomic, structured commits:")

    # Table 6: Commit History (Total = 7900 dxa: 1000, 1500, 3800, 1600)
    table_ci = body_cell.add_table(rows=5, cols=4)
    apply_table_styles(table_ci, dxa_widths=[1000, 1500, 3800, 1600])
    
    headers_ci = ["Commit Hash", "Commit Type", "Conventional Commit Message", "Modified Area & Files"]
    for i, h in enumerate(headers_ci):
        style_cell(table_ci.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    ci_data = [
        ("17e071f", "docs", "docs: initialize project governance with README, .gitignore, and issue templates", "README.md, .gitignore, .github/ templates (16 files)."),
        ("37c04a4", "feat", "feat: implement Spring Boot application skeleton and 4-tier architecture", "pom.xml, Java models, repo, service, controllers, HTML (12 files)."),
        ("e202685", "test", "test: add automated Spring Boot tests for review moderation and health probe", "CustomerReviewPortalApplicationTests.java (7 test cases)."),
        ("b0d2ac9", "docs", "docs: add completed laboratory task reports 1 through 3 and evidence", "Canonical documents and 300 DPI architectural figures.")
    ]
    for r_idx, row_vals in enumerate(ci_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_ci.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 7: Live Terminal Verification Evidence
    add_heading(body_cell, "Live terminal repository verification evidence", keep_with_next=True)
    add_body_p(body_cell, "The initialized repository was verified live through standard Git CLI commands on PowerShell. The terminal capture confirms clean working tree status, branch tracking, remote URL configuration, and commit log integrity:")

    # Figure 4.2: Terminal Log
    fig2_path = os.path.join(base_dir, "screenshots", "task4", "figure_4_2_git_terminal_log.png")
    if os.path.exists(fig2_path):
        add_figure(body_cell, fig2_path, 
                   "Figure 4.2: Terminal Git Log & Repository Initialization Verification (PowerShell Live Execution)", 
                   width_inches=5.4)

    # Row 4: Conclusion (Academic Summary)
    t2.rows[4].cells[0].text = "Conclusion:"
    style_cell(t2.rows[4].cells[0], bold=True, font_size=11)
    
    conc_text = "In this task, I have successfully initialized, configured, and baselined the Git and GitHub version control repository for the Customer Review Moderation Portal (CRMP). Operating under strict academic identity standards (Rushikesh Gawade, Roll No: 23102A0052, Dr. Snehal Andhare), I established a professional project governance baseline comprising a detailed README.md, a multi-tiered .gitignore file that insulates the repository from transient build binaries and IDE caches, and standardized GitHub issue templates for bug tracking and feature requests. I formulated a strict multi-branch Git workflow enforcing protected main releases, dev integration, and feature branches governed by Conventional Commits. The initial 4-tier Spring Boot application skeleton and automated test suite were successfully committed across 4 atomic, meaningful commits, and the active dev branch was established and mapped to the remote GitHub origin. This solid SCM foundation ensures complete traceability, reproducibility, and audit readiness for feature branch development and pull request collaboration in Task 5."
    t2.rows[4].cells[1].text = conc_text
    style_cell(t2.rows[4].cells[1], font_size=10.5, text=conc_text)

    output_path = os.path.join(base_dir, "docs", "DevOps_Task4_RushikeshGawade_23102A0052.docx")
    save_and_archive(doc, output_path)

if __name__ == "__main__":
    generate_task4_document()
