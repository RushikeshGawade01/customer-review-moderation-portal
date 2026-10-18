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

def generate_task2_document():
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
    t2.rows[0].cells[1].text = "2"
    style_cell(t2.rows[0].cells[1], bold=True, font_size=12, text="2")
    
    # Row 1: Task Title
    t2.rows[1].cells[0].text = "Task Title"
    style_cell(t2.rows[1].cells[0], bold=True, font_size=11)
    title_text = "Agile Planning and DevOps Workflow: Create user stories and acceptance criteria for the Customer Review Moderation Portal. Prepare a product backlog, 15-Task Kanban/Scrum plan, Definition of Done and a DevOps lifecycle diagram from development to operations."
    t2.rows[1].cells[1].text = title_text
    style_cell(t2.rows[1].cells[1], bold=True, font_size=10.5, text=title_text)
    
    # Row 2: Resources / Apparatus Required (Hardware & Software)
    t2.rows[2].cells[0].text = "Resources / Apparatus Required"
    style_cell(t2.rows[2].cells[0], bold=True, font_size=10)
    hw_text = "Hardware: Laptop / PC (x86_64), 16 GB RAM, 512 GB NVMe SSD, Quad-Core Processor (Intel Core i5/i7 or AMD Ryzen)"
    sw_text = "Software: Windows 11 64-bit, Oracle JDK 21 LTS, Apache Maven 3.9.x, Git 2.51.x, Spring Boot 3.x, Embedded H2 Database, Jira / Kanban Board, Visual Studio Code / IntelliJ IDEA"
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
    r0 = p0.add_run("Agile methodology adoption and Scrumban governance rationale")
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)
    
    add_body_p(body_cell, "Modern software engineering mandates a tight synergy between Agile planning and DevOps execution. For the engineering lifecycle of the Customer Review Moderation Portal (CRMP), I adopted a hybrid 'Scrumban' methodology—fusing the iterative cadence, sprint boundaries, and ceremony rigor of Scrum with the visual flow management, Work-In-Progress (WIP) constraints, and pull-based execution of Kanban.")
    add_body_p(body_cell, "While traditional Waterfall models introduce rigid handoffs between development, quality assurance, and operations teams, Scrumban treats every feature as an incremental, deployable slice of functionality. In our 15-task laboratory progression, each sprint produces working code accompanied by automated Selenium test cases, multi-stage Docker containers, and Ansible automation. Limiting Work-In-Progress (WIP) prevents multi-tasking bottlenecks, accelerates feedback loops, and guarantees that code does not transition to 'Done' until verified against strict continuous integration quality gates.")

    # Section 1: User Stories and Gherkin Acceptance Criteria
    add_heading(body_cell, "Granular user stories and Gherkin acceptance criteria", keep_with_next=True)
    add_body_p(body_cell, "To govern user-centric feature implementation across the Customer Review Moderation Portal, I decomposed the business requirements into 5 primary Epics encompassing 6 core User Stories. Each user story is estimated in Fibonacci story points and formalizes acceptance criteria using industry-standard Gherkin (Given-When-Then) syntax:")

    # Table 1: User Stories & Acceptance Criteria (Total = 7900 dxa: 900, 1400, 2600, 2100, 900)
    table_us = body_cell.add_table(rows=7, cols=5)
    apply_table_styles(table_us, dxa_widths=[900, 1400, 2600, 2100, 900])
    
    headers_us = ["Story ID", "Epic / Module", "User Story Description (Role - Need - Benefit)", "Acceptance Criteria (Gherkin Syntax)", "Points"]
    for i, h in enumerate(headers_us):
        style_cell(table_us.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    us_data = [
        ("US-01", "Epic 1: Review Ingestion", "As an End Shopper, I want to submit a product rating (1-5), review title, and comments, so that other buyers can make informed purchasing choices.", "Scenario: Valid Submission\nGiven shopper navigates to /submit\nWhen valid details entered and submitted\nThen status is PENDING and alert shows.", "5 SP"),
        ("US-02", "Epic 1: Input Validation", "As a Platform Admin, I want strict input validation on empty fields and invalid star ratings, so that garbage data is rejected at submission.", "Scenario: Out-of-bounds Rating\nGiven review form with rating 6 or 0\nWhen form is submitted\nThen inline error 'Rating must be 1-5' is displayed.", "3 SP"),
        ("US-03", "Epic 2: Review Directory", "As a Content Moderator, I want to view a centralized directory with real-time text search, so that I can triage pending reviews rapidly.", "Scenario: Keyword Filtering\nGiven 20 reviews in directory\nWhen moderator types product name\nThen table updates instantly to matching rows.", "5 SP"),
        ("US-04", "Epic 3: Status Lifecycle", "As a Content Moderator, I want to click 'Approve', 'Reject', or 'Flag' on pending reviews, so that verified reviews publish and spam is blocked.", "Scenario: Approve Transition\nGiven review in PENDING state\nWhen moderator clicks 'Approve'\nThen status tag dynamically updates to APPROVED.", "5 SP"),
        ("US-05", "Epic 4: KPI Dashboard", "As a Brand Merchant, I want real-time KPI cards for Total, Pending, Approved, and Flagged reviews, so that I can monitor customer sentiment.", "Scenario: KPI Counters Sync\nGiven review approval action executed\nWhen merchant visits dashboard\nThen approved counter increments by 1 in real time.", "3 SP"),
        ("US-06", "Epic 5: Health & Probing", "As a DevOps Engineer, I want an automated HTTP /actuator/health endpoint returning UP, so that CI/CD and container probes detect readiness.", "Scenario: Automated Liveness Probe\nGiven application running on port 8080\nWhen GET /actuator/health executed\nThen HTTP 200 with {\"status\":\"UP\"} is returned.", "2 SP")
    ]
    for r_idx, row_vals in enumerate(us_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_us.rows[r_idx].cells[c_idx], font_size=8.6, text=val)

    # Section 2: Prioritized Product Backlog
    add_heading(body_cell, "Prioritized product backlog (MoSCoW & WSJF framework)", keep_with_next=True)
    add_body_p(body_cell, "To optimize value delivery and establish clear sprint planning boundaries, the Product Backlog is prioritized using the MoSCoW framework (Must Have, Should Have, Could Have, Won't Have) alongside Weighted Shortest Job First (WSJF) estimation:")

    # Table 2: Product Backlog (Total = 7900 dxa: 900, 1600, 2600, 900, 1000, 900)
    table_pb = body_cell.add_table(rows=8, cols=6)
    apply_table_styles(table_pb, dxa_widths=[900, 1600, 2600, 900, 1000, 900])
    
    headers_pb = ["Backlog ID", "Epic Category", "Feature / Backlog Item Title", "Story Pts", "MoSCoW", "Target Sprint"]
    for i, h in enumerate(headers_pb):
        style_cell(table_pb.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    pb_data = [
        ("PBI-01", "Core Architecture", "4-Tier Spring Boot Skeleton & In-Memory H2 Persistence", "5 SP", "Must Have", "Sprint 1"),
        ("PBI-02", "Review Ingestion", "Responsive Submission Form with Spring Bean Validation", "5 SP", "Must Have", "Sprint 2"),
        ("PBI-03", "Moderation Queue", "Centralized Directory with Live Search & Status Filters", "5 SP", "Must Have", "Sprint 2"),
        ("PBI-04", "State Machine", "Role-Based Lifecycle Workflow (PENDING -> APPROVED/REJECTED)", "5 SP", "Must Have", "Sprint 2"),
        ("PBI-05", "Metrics Dashboard", "Real-Time Summary KPI Cards & Sentiment Aggregator", "3 SP", "Must Have", "Sprint 2"),
        ("PBI-06", "Continuous Testing", "Headless Selenium WebDriver 4.x Automated Test Suite", "5 SP", "Must Have", "Sprint 3"),
        ("PBI-07", "CI/CD & Container", "Multi-stage Dockerfile & Jenkins Declarative Pipeline", "8 SP", "Must Have", "Sprint 4")
    ]
    for r_idx, row_vals in enumerate(pb_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_pb.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 3: Visual Kanban Board Representation
    add_heading(body_cell, "Visual Kanban task board and sprint execution flow", keep_with_next=True)
    add_body_p(body_cell, "To ensure continuous flow transparency, eliminate blocking dependencies, and enforce Work-In-Progress limits, the team manages all engineering tasks on a standardized 5-column Kanban board:")

    # Insert Figure 2.1: Kanban Board
    fig1_path = os.path.join(base_dir, "screenshots", "task2", "figure_2_1_kanban_board.png")
    if os.path.exists(fig1_path):
        add_figure(body_cell, fig1_path, 
                   "Figure 2.1: Visual Kanban Task Board & Sprint Execution Flow for Customer Review Moderation Portal", 
                   width_inches=5.4)

    add_body_p(body_cell, "Work-In-Progress (WIP) Limits Rationale: As illustrated in Figure 2.1, strict WIP limits are enforced on the 'In Progress' (limit = 2) and 'CI Testing / QA' (limit = 2) columns. In a DevOps delivery pipeline, piling up unverified features creates quality debt. By constraining active development to 2 items simultaneously, engineers are compelled to assist in clearing test failures or deployment gates before pulling fresh user stories from the Sprint To-Do queue. This minimizes lead time and maximizes release stability.")

    # Section 4: 15-Task Scrum Sprint Plan
    add_heading(body_cell, "15-Task Kanban/Scrum sprint plan across the university syllabus", keep_with_next=True)
    add_body_p(body_cell, "To achieve 100% syllabus alignment, the 15 laboratory tasks are organized into 5 structured, two-week sprint cadences. Each sprint represents a cohesive engineering milestone culminating in a verified deliverable:")

    # Table 3: 15-Task Sprint Roadmap (Total = 7900 dxa: 800, 1500, 2400, 1800, 1400)
    table_sp = body_cell.add_table(rows=16, cols=5)
    apply_table_styles(table_sp, dxa_widths=[800, 1500, 2400, 1800, 1400])
    
    headers_sp = ["Sprint", "Task Identifier", "Engineering Activity & Scope", "DevOps Deliverable", "Quality Gate / Verification"]
    for i, h in enumerate(headers_sp):
        style_cell(table_sp.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    sp_data = [
        ("Sprint 1", "Task 1", "Problem definition, real-time need analysis, stakeholder matrix.", "Problem statement & 15-task scope document.", "Academic approval by Dr. Snehal Andhare."),
        ("Sprint 1", "Task 2", "Agile planning, user stories, product backlog, DoD, and lifecycle flow.", "Backlog, task board, sprint plan, DoD matrix.", "Acceptance criteria review & signed backlog."),
        ("Sprint 1", "Task 3", "4-tier architecture, SRS, use case model, H2 DB, local setup.", "Architecture specification & working baseline.", "Local compilation & Actuator health UP."),
        ("Sprint 2", "Task 4", "Git repo init, .gitignore, branch naming policy, skeleton commit.", "GitHub repo URL, README, initial skeleton.", "Git log verification & conventional commits."),
        ("Sprint 2", "Task 5", "Implement review ingestion on feature branch, PR, peer review.", "Feature branch, pull request, merge evidence.", "Code review approval & clean fast-forward merge."),
        ("Sprint 2", "Task 6", "Complete remaining MVP modules, intentional merge conflict fix, v1.0.0.", "Functional MVP, resolved conflict log, release tag.", "Zero conflict markers; tag v1.0.0 verified."),
        ("Sprint 3", "Task 7", "Jenkins installation, GitHub webhook/poll trigger, Maven CI job.", "Configured Jenkins CI job, build logs, jar artifact.", "Automated trigger on commit; BUILD SUCCESS."),
        ("Sprint 3", "Task 8", "Jenkinsfile pipeline-as-code (Checkout, Build, Test, Deploy).", "Declarative Jenkinsfile & multi-stage pipeline run.", "Green pipeline execution with 0 manual steps."),
        ("Sprint 3", "Task 9", "Selenium WebDriver test design covering 4 user journeys, failure png.", "Selenium test suite, test plan, screenshot hook.", "100% headless pass rate via mvn test."),
        ("Sprint 3", "Task 10", "Jenkins quality gate halt on defect, intentional bug fix verification.", "Test report, aborted pipeline log, fix commit run.", "Pipeline halts immediately on test assertion failure."),
        ("Sprint 4", "Task 11", "Multi-stage Dockerfile, build, tag, port 8080 mapping, lifecycle logs.", "Dockerfile, image inspection, lifecycle command logs.", "Container runs cleanly in isolation on port 8080."),
        ("Sprint 4", "Task 12", "Jenkins-Docker CD: automated container build, publish, and rollout.", "Versioned container image, automated CD pipeline.", "Automated commit-to-running-container deployment."),
        ("Sprint 5", "Task 13", "Ansible configuration management: prerequisites, ports, directories.", "Ansible inventory (hosts.ini), playbook.yml.", "Syntax check passed via ansible-playbook."),
        ("Sprint 5", "Task 14", "Automated provisioning, idempotency proof (changed=0), health rollback.", "Provisioned host, idempotency evidence, rollback log.", "Idempotency verified; Actuator UP confirmed."),
        ("Sprint 5", "Task 15", "End-to-end DevOps demonstration, documentation compilation, viva.", "Production release, complete technical report, viva.", "Comprehensive defense & faculty evaluation.")
    ]
    for r_idx, row_vals in enumerate(sp_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_sp.rows[r_idx].cells[c_idx], font_size=8.5, text=val)

    # Section 5: Definition of Ready (DoR) and Definition of Done (DoD)
    add_heading(body_cell, "Definition of Ready (DoR) and Multi-Tiered Definition of Done (DoD)", keep_with_next=True)
    add_body_p(body_cell, "To maintain zero defect leakage throughout sprint execution, the team established unambiguous gates for story intake and completion:")
    add_body_p(body_cell, "Definition of Ready (DoR): A backlog item may only enter active sprint development when: (1) The user story clearly states Persona, Action, and Business Value; (2) Acceptance criteria are fully written in Gherkin syntax; (3) External dependencies (DB schema, API models) are identified; (4) Story points are estimated via team consensus; and (5) UI locator IDs are pre-allocated for Selenium automation.", bold_prefix="• ")
    add_body_p(body_cell, "Definition of Done (DoD): A feature is considered 'Done' only when it satisfies all six verification tiers detailed below:", bold_prefix="• ")

    # Table 4: Multi-Tiered Definition of Done (Total = 7900 dxa: 1200, 2000, 2700, 2000)
    table_dod = body_cell.add_table(rows=7, cols=4)
    apply_table_styles(table_dod, dxa_widths=[1200, 2000, 2700, 2000])
    
    headers_dod = ["DoD Tier", "Quality Verification Area", "Mandatory Acceptance Standards", "Automated DevOps Verification Tool"]
    for i, h in enumerate(headers_dod):
        style_cell(table_dod.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    dod_data = [
        ("Tier 1: Code Quality", "Syntax, Formatting & Lints", "Zero Java compiler warnings, SonarLint zero blocker defects, strict adherence to naming conventions.", "Maven Compiler Plugin & IDE static analysis"),
        ("Tier 2: Unit Testing", "Service & State Machine Logic", "100% method pass rate for state transitions (PENDING -> APPROVED/REJECTED/FLAGGED), zero exceptions.", "JUnit 5 + Spring Boot Starter Test (mvn test)"),
        ("Tier 3: E2E Automation", "Selenium WebDriver UI Journeys", "All 4 critical browser journeys pass headlessly; failure screenshot hooks execute without error.", "Headless Selenium WebDriver 4.x + Chrome"),
        ("Tier 4: CI Build Gate", "Continuous Integration Pipeline", "Jenkins pipeline executes Checkout, Build, and Test stages; build status green; Surefire report archived.", "Jenkins CI Automation Server (Jenkinsfile)"),
        ("Tier 5: Container & Health", "Docker Packaging & Probing", "Multi-stage Docker build succeeds (<220 MB); container runs on port 8080; /actuator/health returns UP.", "Docker CLI + cURL HTTP probe check"),
        ("Tier 6: Documentation", "Archival & Academic Identity", "Script-driven docx generated with exact student name (Rushikesh Gawade), zero XML defects, prior version in docs/prev/.", "Python python-docx pipeline (save_and_archive)")
    ]
    for r_idx, row_vals in enumerate(dod_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_dod.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 6: End-to-End DevOps Lifecycle Diagram
    add_heading(body_cell, "End-to-end DevOps lifecycle architecture from development to operations", keep_with_next=True)
    add_body_p(body_cell, "DevOps bridges the historical divide between software development and production operations. The complete lifecycle for the Customer Review Moderation Portal operates as a continuous, closed-loop system encompassing eight interconnected phases:")

    # Insert Figure 2.2: DevOps Lifecycle
    fig2_path = os.path.join(base_dir, "screenshots", "task2", "figure_2_2_devops_lifecycle.png")
    if os.path.exists(fig2_path):
        add_figure(body_cell, fig2_path, 
                   "Figure 2.2: End-to-End DevOps Lifecycle Workflow (Development to Operations) for Customer Review Moderation Portal", 
                   width_inches=5.4)

    add_body_p(body_cell, "DevOps Phases and Continuous Feedback Loops: As shown in Figure 2.2, the lifecycle progresses across continuous planning (Jira/Markdown), code versioning (Git/GitHub), deterministic builds (Maven Wrapper), automated testing gates (Selenium WebDriver), declarative release orchestration (Jenkins), lightweight container packaging (Docker), automated configuration (Ansible), and real-time operational monitoring (Spring Boot Actuator). Critical telemetry from the /actuator/health endpoint and automated test failure logs feed directly back into Sprint Planning, completing the feedback loop and driving continuous improvement.")

    # Section 7: Agile Velocity and Flow Metrics
    add_heading(body_cell, "Sprint velocity forecast, capacity allocation, and DORA metrics", keep_with_next=True)
    add_body_p(body_cell, "To ensure team throughput predictability and assess engineering maturity, I tracked sprint capacity and aligned project targets with industry-standard DORA (DevOps Research and Assessment) metrics:")

    # Table 5: Sprint Velocity & DORA Metrics (Total = 7900 dxa: 1000, 1800, 1700, 1700, 1700)
    table_vm = body_cell.add_table(rows=6, cols=5)
    apply_table_styles(table_vm, dxa_widths=[1000, 1800, 1700, 1700, 1700])
    
    headers_vm = ["Sprint Ref", "Total Story Points", "Committed Tasks", "Velocity Achievement", "Target DORA Metric / SLA"]
    for i, h in enumerate(headers_vm):
        style_cell(table_vm.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    vm_data = [
        ("Sprint 1", "13 Story Points", "Tasks 1, 2, 3", "100% (13 SP Completed)", "Lead Time for Planning < 48 hours"),
        ("Sprint 2", "16 Story Points", "Tasks 4, 5, 6", "100% (16 SP Completed)", "Change Failure Rate = 0% on dev merge"),
        ("Sprint 3", "18 Story Points", "Tasks 7, 8, 9, 10", "100% (18 SP Completed)", "Automated Test Gate Halt < 5 seconds"),
        ("Sprint 4", "13 Story Points", "Tasks 11, 12", "100% (13 SP Completed)", "Docker Build Turnaround < 90 seconds"),
        ("Sprint 5", "15 Story Points", "Tasks 13, 14, 15", "100% (15 SP Completed)", "Ansible Idempotency: changed=0, failed=0")
    ]
    for r_idx, row_vals in enumerate(vm_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_vm.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Row 4: Conclusion (Academic Summary)
    t2.rows[4].cells[0].text = "Conclusion:"
    style_cell(t2.rows[4].cells[0], bold=True, font_size=11)
    
    conc_text = "In this task, I have successfully formulated the complete Agile planning framework and DevOps operational workflow for the Git-Based Customer Review Moderation Portal (CRMP). By synthesizing Scrum and Kanban into a unified Scrumban methodology, I established a clear, user-centric backlog comprising 6 detailed User Stories across 5 core Epics, each backed by formal Gherkin-syntax acceptance criteria and Fibonacci story point estimations. I established a visual 5-column Kanban task board with strict Work-In-Progress (WIP) limits that prevent multi-tasking bottlenecks and prioritize automated testing throughput. Furthermore, I structured the 15-task university syllabus into 5 cohesive sprint cycles, defined a comprehensive 6-tier Definition of Done (DoD) that enforces zero compiler warnings, 100% headless Selenium test passes, and Jenkins build gates, and architected the complete 8-stage DevOps lifecycle diagram spanning from Git version control to Docker deployment, Ansible idempotency, and Spring Boot Actuator monitoring. This establishes a highly disciplined, predictable, and automated delivery foundation ready for architectural design and local development baseline setup in Task 3."
    t2.rows[4].cells[1].text = conc_text
    style_cell(t2.rows[4].cells[1], font_size=10.5, text=conc_text)

    output_path = os.path.join(base_dir, "docs", "DevOps_Task2_RushikeshGawade_23102A0052.docx")
    save_and_archive(doc, output_path)

if __name__ == "__main__":
    generate_task2_document()
