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

def generate_task6_document():
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
    t2.rows[0].cells[1].text = "6"
    style_cell(t2.rows[0].cells[1], bold=True, font_size=12, text="6")
    
    # Row 1: Task Title (Exact syllabus text from ASSIGNMENT.md)
    t2.rows[1].cells[0].text = "Task Title"
    style_cell(t2.rows[1].cells[0], bold=True, font_size=11)
    title_text = "MVP Completion and Git Collaboration: Implement the remaining essential MVP functions for the Customer Review Moderation Portal: create, view, update and search records; role-based status workflow; summary dashboard. Demonstrate a second feature branch, conflict creation/resolution, tagging and a release-ready source baseline."
    t2.rows[1].cells[1].text = title_text
    style_cell(t2.rows[1].cells[1], bold=True, font_size=10.5, text=title_text)
    
    # Row 2: Resources / Apparatus Required (Hardware & Software)
    t2.rows[2].cells[0].text = "Resources / Apparatus Required"
    style_cell(t2.rows[2].cells[0], bold=True, font_size=10)
    hw_text = "Hardware: Laptop / PC (x86_64), 16 GB RAM, 512 GB NVMe SSD, Quad-Core CPU (Intel Core i5/i7 or AMD Ryzen)"
    sw_text = "Software: Windows 11 64-bit, Git 2.51.windows.1, GitHub Cloud Platform, Oracle JDK 21 LTS, Apache Maven 3.9.x, Spring Boot 3.3.4, VS Code / IntelliJ IDEA, Edge Browser"
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
    r0 = p0.add_run("Introduction and collaborative source code management rationale")
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(12)
    
    add_body_p(body_cell, "In professional DevOps engineering, bringing a software product to Minimum Viable Product (MVP) completion requires not only robust feature implementation, but also rigorous Source Code Management (SCM) collaboration discipline. As multiple developers build concurrent features on distributed topic branches, merge conflicts inevitably arise when conflicting changes occur on the same lines of code. An engineering team's ability to identify conflict markers, reconcile architectural divergences without regressions, and cryptographically tag release-ready baselines defines the boundary between fragile development and enterprise continuous delivery.")
    add_body_p(body_cell, "The objective of Task 6 is twofold: first, to deliver the fully functional MVP for the Customer Review Moderation Portal (CRMP) covering all 5 core functions (create, view, update, search, status workflow, metrics dashboard, and actuator telemetry); and second, to demonstrate advanced Git collaboration. Operating under the academic evaluation of Dr. Snehal Andhare and the identity of Rushikesh Gawade (Roll No: 23102A0052), I implemented a second topic branch ('feature/moderation-queue-dashboard'), simulated an authentic merge conflict on a shared configuration file ('application.properties'), inspected the standard Git conflict markers ('<<<<<<< HEAD', '=======', '>>>>>>>'), executed a manual unified resolution, merged the verified baseline into 'dev' and 'main', tagged the release baseline as 'v1.0.0', and updated the Agile product backlog.")

    # Section 1: Complete MVP Architectural Catalog
    add_heading(body_cell, "Complete 5-function MVP architectural realization and feature verification", keep_with_next=True)
    add_body_p(body_cell, "In accordance with Section 3 of GEMINI.md and Task 6 requirements, the CRMP MVP encompasses 5 tightly integrated business functions engineered across a 4-tier Spring Boot architecture with an in-memory H2 database:")

    # Table 1: MVP Functions (Total = 7900 dxa: 1600, 2400, 2400, 1500)
    table_mvp = body_cell.add_table(rows=7, cols=4)
    apply_table_styles(table_mvp, dxa_widths=[1600, 2400, 2400, 1500])
    
    headers_mvp = ["MVP Function", "Architectural Components", "Operational Capability", "Verification Gate"]
    for i, h in enumerate(headers_mvp):
        style_cell(table_mvp.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    mvp_data = [
        ("1. Review Ingestion & Bean Validation", "Review.java, ReviewController, submit.html, SpamDetectionService", "Shoppers submit reviews with 1-5 star ratings, product IDs, and comments; validated against bounds & spam heuristics.", "VERIFIED: Inline error display + automated anti-spam triage."),
        ("2. Review Directory & Text Search", "ReviewRepository, ReviewService, reviews.html", "Centralized directory displaying reviews with live keyword search on product names, reviewer handles, and titles.", "VERIFIED: Responsive search filters matching records instantly."),
        ("3. Role-Based Status Workflow", "ReviewStatus.java, ReviewService, ReviewController", "Moderator state machine transitions: PENDING -> APPROVED / REJECTED / FLAGGED with audit notes & timestamps.", "VERIFIED: Dynamic status updates via POST /reviews/{id}/status."),
        ("4. Summary Metrics Dashboard", "DashboardController, index.html, ReviewService", "Executive KPI cards calculating Total Ingested, Pending Queue, Approved Reviews, Flagged Spam, and Average Rating.", "VERIFIED: Real-time dynamic KPI calculation from H2 store."),
        ("5. Actuator Health Probe", "spring-boot-starter-actuator, application.properties", "Production liveness and readiness probe exposing JSON payload at /actuator/health for CI/CD container gates.", "VERIFIED: HTTP 200 {status: UP} validated in Surefire suite."),
        ("Moderator Audit Extension", "Review.java (moderatorNotes, moderatedAt, moderatedBy)", "Enables compliance logging of moderator reasoning during review triage and policy enforcement.", "VERIFIED: Audit pill displayed in review moderation queue.")
    ]
    for r_idx, row_vals in enumerate(mvp_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_mvp.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 2: Second Feature Branch Lifecycle
    add_heading(body_cell, "Second feature branch ('feature/moderation-queue-dashboard') execution", keep_with_next=True)
    add_body_p(body_cell, "To implement moderation audit extensions and queue governance settings, a second dedicated topic branch was created off 'dev'. The chronological execution trace is summarized below:")

    # Table 2: Feature Branch 2 Execution (Total = 7900 dxa: 1400, 2000, 2500, 2000)
    table_f2 = body_cell.add_table(rows=6, cols=4)
    apply_table_styles(table_f2, dxa_widths=[1400, 2000, 2500, 2000])
    
    headers_f2 = ["Lifecycle Stage", "PowerShell Command Executed", "Engineering Behavior & File Changes", "Git Verification Output"]
    for i, h in enumerate(headers_f2):
        style_cell(table_f2.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    f2_data = [
        ("Branch Creation", "git checkout -b feature/moderation-queue-dashboard", "Branches off dev baseline (commit 6bcf46d) for isolated queue enhancement.", "Switched to a new branch 'feature/moderation-queue-dashboard'"),
        ("Audit Implementation", "Code modifications across 5 files", "Added moderatorNotes, moderatedAt, moderatedBy to Review entity & service.", "Review.java, ReviewService.java, ReviewController.java modified."),
        ("Feature Commit", 'git commit -m "feat(moderation): add moderator audit..."', "Atomic commit of moderator triage workflow, audit notes, and queue settings.", "[feature/moderation-queue-dashboard da03b1e] (69 insertions)"),
        ("Automated Tests", "mvn test", "Executes Surefire test harness asserting zero regressions across 10 tests.", "Tests run: 10, Failures: 0, Errors: 0, BUILD SUCCESS"),
        ("Remote Branch Push", "git push -u origin feature/moderation-queue-dashboard", "Pushes topic branch to GitHub remote and sets upstream tracking.", "* [new branch] feature/moderation-queue-dashboard -> origin")
    ]
    for r_idx, row_vals in enumerate(f2_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_f2.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 3: Merge Conflict Creation, Dissection, and Resolution
    add_heading(body_cell, "Intentional merge conflict creation, marker inspection, and unified resolution", keep_with_next=True)
    add_body_p(body_cell, "To demonstrate real-world collaborative merge conflict resolution, a conflicting commit was introduced on 'dev' modifying the identical configuration block in 'src/main/resources/application.properties'. While the feature branch configured 90-day retention with 3-flag auto-triage, the 'dev' branch committed 180-day retention with verbose audit logging:")
    add_body_p(body_cell, "Attempting to merge 'feature/moderation-queue-dashboard' into 'dev' immediately halted execution with: 'CONFLICT (content): Merge conflict in src/main/resources/application.properties. Automatic merge failed; fix conflicts and then commit the result.'", bold_prefix="Merge Collision: ")
    add_body_p(body_cell, "Inspecting the unmerged file revealed standard Git three-way conflict markers dividing the divergent branches:", bold_prefix="Conflict Markers: ")

    # Table 3: Conflict Anatomy (Total = 7900 dxa: 1800, 3100, 3000)
    table_conf = body_cell.add_table(rows=5, cols=3)
    apply_table_styles(table_conf, dxa_widths=[1800, 3100, 3000])
    
    headers_conf = ["Conflict Marker / Stage", "Code Payload in application.properties", "Architectural Intent & Triage Analysis"]
    for i, h in enumerate(headers_conf):
        style_cell(table_conf.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    conf_data = [
        ("<<<<<<< HEAD (dev branch)", "app.moderation.retention-days=180\napp.moderation.auto-flag-threshold=5\napp.moderation.default-queue-view=ALL\napp.moderation.audit-logging-level=VERBOSE", "Branch dev prioritized extended data archival (180 days) and comprehensive verbose server telemetry."),
        ("=======\n(Delimiter)", "Divider line separating current HEAD from incoming branch changes.", "Standard Git delimiter separating divergent changes on the same byte range."),
        (">>>>>>> feature branch\n(Incoming topic)", "app.moderation.retention-days=90\napp.moderation.auto-flag-threshold=3\napp.moderation.default-queue-view=PENDING\napp.moderation.notification-enabled=true", "Feature branch prioritized aggressive spam containment (threshold=3) and email notifications."),
        ("Unified Resolution\n(Committed Merge beaf728)", "app.moderation.retention-days=180\napp.moderation.auto-flag-threshold=3\napp.moderation.default-queue-view=PENDING\napp.moderation.notification-enabled=true\napp.moderation.audit-logging-level=VERBOSE", "Reconciled both requirements: adopted the robust 180-day retention and VERBOSE logging from dev, while integrating threshold=3 and notifications from the feature branch.")
    ]
    for r_idx, row_vals in enumerate(conf_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_conf.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Figure 6.1: Conflict Resolution Lifecycle
    fig1_path = os.path.join(base_dir, "screenshots", "task6", "figure_6_1_conflict_resolution_lifecycle.png")
    if os.path.exists(fig1_path):
        add_figure(body_cell, fig1_path, 
                   "Figure 6.1: Git Merge Conflict Creation, Marker Inspection, Resolution Lifecycle & Release Tagging (v1.0.0)", 
                   width_inches=5.4)

    # Section 4: Semantic Versioning and Tagging Policy
    add_heading(body_cell, "Semantic versioning, release baseline tagging ('v1.0.0'), and main branch alignment", keep_with_next=True)
    add_body_p(body_cell, "Following conflict resolution and test verification, the merged baseline on 'dev' represented the production-ready MVP. In accordance with GEMINI.md Section 4 ('main: Protected production-ready branch. Only tagged releases v1.0.0'), the code was merged into 'main' and tagged using an annotated Git tag:")
    add_body_p(body_cell, "git tag -a v1.0.0 -m \"Release v1.0.0: Complete MVP Customer Review Moderation Portal - Rushikesh Gawade (23102A0052)\"", bold_prefix="Annotated Tag Command: ")
    add_body_p(body_cell, "Annotated tags store complete cryptographic metadata—including the tagger's identity, email (gawaderushikesh576@gmail.com), timestamp, and release message—ensuring tamper-proof provenance for Jenkins CI triggers in Task 7.", bold_prefix="Audit Provenance: ")

    # Table 4: Git Tag Details (Total = 7900 dxa: 1100, 1400, 3400, 2000)
    table_tags = body_cell.add_table(rows=5, cols=4)
    apply_table_styles(table_tags, dxa_widths=[1100, 1400, 3400, 2000])
    
    headers_tags = ["Release Tag", "Target Commit", "Annotated Release Message", "Git Branch & Remote Alignment"]
    for i, h in enumerate(headers_tags):
        style_cell(table_tags.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    tags_data = [
        ("v1.0.0", "beaf728", "Release v1.0.0: Complete MVP Customer Review Moderation Portal - Rushikesh Gawade (23102A0052)", "Tagged on dev & main; pushed to origin/main & origin/dev with --tags."),
        ("Commit da03b1e", "da03b1e", "feat(moderation): add moderator audit notes, review triage workflow, and queue governance", "Feature branch commit on origin/feature/moderation-queue-dashboard."),
        ("Commit 18b322a", "18b322a", "feat(config): configure production retention policy and verbose audit telemetry on dev", "Conflicting commit on dev branch triggering intentional merge conflict."),
        ("Commit beaf728", "beaf728", "merge: resolve merge conflict in application.properties between dev and feature/moderation-queue-dashboard", "Unified merge commit reconciling dev and feature branches.")
    ]
    for r_idx, row_vals in enumerate(tags_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_tags.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 5: Updated Agile Product Backlog
    add_heading(body_cell, "Updated Agile product backlog and Definition of Done (DoD) completion sign-off", keep_with_next=True)
    add_body_p(body_cell, "With the release of v1.0.0, all 5 core MVP user stories have been fully delivered and transitioned to 'DONE' status in the product backlog (.github/BACKLOG_MVP_COMPLETION.md):")

    # Table 5: Updated Backlog (Total = 7900 dxa: 1000, 1500, 2600, 1400, 1400)
    table_ab = body_cell.add_table(rows=7, cols=5)
    apply_table_styles(table_ab, dxa_widths=[1000, 1500, 2600, 1400, 1400])
    
    headers_ab = ["Story ID", "Epic Category", "User Story Summary", "Story Points", "MVP Status"]
    for i, h in enumerate(headers_ab):
        style_cell(table_ab.rows[0].cells[i], bg_color="EAECEE", bold=True, font_size=9.5, text=h)
        
    ab_data = [
        ("US-01", "Epic 1: Ingestion", "End shopper review submission with 1-5 star ratings, product IDs, and feedback comments.", "5 SP", "DONE (Verified)"),
        ("US-02", "Epic 1: Validation", "Strict input validation against empty fields, invalid ratings, and spam keyword heuristics.", "3 SP", "DONE (Verified)"),
        ("US-03", "Epic 2: Directory", "Searchable review directory with real-time text query and status filters (PENDING, APPROVED, etc.).", "5 SP", "DONE (Verified)"),
        ("US-04", "Epic 3: Lifecycle", "Role-based status state machine transitions with moderator audit notes and timestamps.", "5 SP", "DONE (Verified)"),
        ("US-05", "Epic 4: Dashboard", "Real-time summary KPI cards for Total, Pending, Approved, Flagged reviews, and average rating.", "3 SP", "DONE (Verified)"),
        ("US-06", "Epic 5: Telemetry", "Automated Spring Boot Actuator health endpoint (/actuator/health) returning UP status.", "2 SP", "DONE (Verified)")
    ]
    for r_idx, row_vals in enumerate(ab_data, start=1):
        for c_idx, val in enumerate(row_vals):
            style_cell(table_ab.rows[r_idx].cells[c_idx], font_size=8.8, text=val)

    # Section 6: Live Verification Evidence
    add_heading(body_cell, "Live system execution, dashboard UI, and Git conflict resolution evidence", keep_with_next=True)
    add_body_p(body_cell, "The figures below present verifiable evidence captured from the running Spring Boot application on localhost:8080, the PowerShell terminal session demonstrating the conflict lifecycle, and the live GitHub repository releases page:")

    # Figure 6.2: Live Dashboard UI
    fig2_path = os.path.join(base_dir, "screenshots", "task6", "dashboard_live_v1.png")
    if os.path.exists(fig2_path):
        add_figure(body_cell, fig2_path, 
                   "Figure 6.2: Live Customer Review Moderation Portal (http://localhost:8080) Displaying Real-Time KPI Cards & Recent Ingestions", 
                   width_inches=5.4)

    # Figure 6.3: Live Moderation Queue UI
    fig3_path = os.path.join(base_dir, "screenshots", "task6", "moderation_queue_live_v1.png")
    if os.path.exists(fig3_path):
        add_figure(body_cell, fig3_path, 
                   "Figure 6.3: Live Review Directory & Moderation Queue (http://localhost:8080/reviews) Showing Search, Filter, and Status Triage Controls", 
                   width_inches=5.4)

    # Figure 6.4: Real Terminal Conflict Resolution Session
    fig4_path = os.path.join(base_dir, "screenshots", "task6", "git_conflict_resolution_terminal.png")
    if os.path.exists(fig4_path):
        add_figure(body_cell, fig4_path, 
                   "Figure 6.4: Real PowerShell Session Execution (Merge Conflict Creation, Marker Inspection, Resolution Commit beaf728, and v1.0.0 Tagging)", 
                   width_inches=5.4)

    # Figure 6.5: Live GitHub Release Tags
    fig5_path = os.path.join(base_dir, "screenshots", "task6", "github_tag_v1_live.png")
    if os.path.exists(fig5_path):
        add_figure(body_cell, fig5_path, 
                   "Figure 6.5: Verified Live GitHub Repository Showing Production Release Tag v1.0.0 (https://github.com/RushikeshGawade01/customer-review-moderation-portal/tags)", 
                   width_inches=5.4)

    # Row 4: Conclusion (Academic Summary)
    t2.rows[4].cells[0].text = "Conclusion:"
    style_cell(t2.rows[4].cells[0], bold=True, font_size=11)
    
    conc_text = "In this task, I successfully completed all essential Minimum Viable Product (MVP) functions for the Customer Review Moderation Portal (CRMP) and demonstrated professional Git collaboration under academic standards (Rushikesh Gawade, Roll No: 23102A0052, Dr. Snehal Andhare). I delivered the 5 core application functions—review ingestion with strict validation, searchable review directory, role-based status lifecycle, summary metrics dashboard, and actuator telemetry—backed by an embedded in-memory H2 database. I executed a second topic branch ('feature/moderation-queue-dashboard'), introduced an intentional merge conflict on 'application.properties', inspected standard Git conflict markers ('<<<<<<< HEAD', '=======', '>>>>>>>'), and performed a unified manual resolution committed as merge commit beaf728. The production-ready baseline was synchronized across 'dev' and 'main' branches and tagged with annotated semantic version tag 'v1.0.0' on GitHub. All 23 planned story points were verified as DONE in the product backlog, establishing an immutable, release-ready baseline ready for Jenkins continuous integration in Task 7."
    t2.rows[4].cells[1].text = conc_text
    style_cell(t2.rows[4].cells[1], font_size=10.5, text=conc_text)

    output_path = os.path.join(base_dir, "docs", "DevOps_Task6_RushikeshGawade_23102A0052.docx")
    save_and_archive(doc, output_path)

if __name__ == "__main__":
    generate_task6_document()
