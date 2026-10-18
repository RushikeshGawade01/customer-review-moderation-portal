# DevOps Project Master Rules & Operational Blueprint

This document defines the absolute, uncompromised standards, constraints, academic identity, document layouts, and DevOps technical requirements for all 15 tasks of this laboratory project. Every operation, code modification, document generation, and test execution must strictly adhere to these rules.

---

## 1. Academic & Student Identity
All generated documents, git commits, configuration files, reports, and code comments must consistently reflect the following exact identity:

* **Student Name:** Rushikesh Gawade
* **Roll Number:** 23102A0052
* **Program & Branch:** B.E. Semester VII – Computer Engineering
* **Subject:** DevOps Lab
* **Subject In-charge / Evaluator:** Dr. Snehal Andhare
* **Assigned Project Title:** Git-Based Customer Review Moderation Portal
* **Document Filename Pattern:** `DevOps_Task{N}_RushikeshGawade_23102A0052.docx` (where `{N}` is 1 to 15)

---

## 2. Document Template & Formatting Enforcement
Every task document must be generated programmatically from the approved department template to ensure 100% structural fidelity and visual consistency:

1. **Base Templates:**
   * **Task 1:** `templates/template_task1.docx` (4-row Table 2 format).
   * **Tasks 2 to 15:** `templates/template_standard.docx` (5-row Table 2 format with Apparatus row).
2. **Table Envelope Integrity:**
   * **Table 0:** Semester, Subject, Subject In-charge (`Dr. Snehal Andhare`).
   * **Table 1:** Student Name (`Rushikesh Gawade`), Roll Number (`23102A0052`), Teacher's Signature.
   * **Table 2:**
     * `Row 0`: Task Number.
     * `Row 1`: Task Title (Exact title from the official 15-task allocation sheet).
     * `Row 2` (Tasks 2-15): Resources / Apparatus Required (Hardware & Software).
     * `Row 3` (Task 1: Row 2): Program & Output (Core content, bold section titles, tables, code snippets, centered figures).
     * `Row 4` (Task 1: Row 3): Conclusion (Formal academic summary of objectives achieved and verified).
3. **Typography & Styling:**
   * Default Font Family: **Calibri**.
   * Body Paragraphs: 11pt–12pt regular, 1.15 line spacing, 3pt space-after.
   * Section Headings: 12pt Bold Calibri.
   * Tables in Content: Headers shaded `#EAECEE`, cell borders `#CCCCCC`, font size 9.5pt–10pt.
   * Margins: Top: `0.53"`, Bottom: `0.50"`, Left: `0.75"`, Right: `0.75"`.
4. **Reproducibility & Document Archival Policy:**
   * Every document must be generated via a Python script in `scripts/generate_task{N}.py` so it can be re-run and updated deterministically.
   * **Archival of Previous Versions:** The root `docs/` folder must ONLY ever contain the single, latest, canonical task file (`DevOps_Task{N}_RushikeshGawade_23102A0052.docx`). Whenever an updated version of a task document is generated, any previous version must automatically be archived into `docs/prev/` (e.g., `docs/prev/DevOps_Task{N}_RushikeshGawade_23102A0052_prev_<timestamp>.docx`) so there is zero confusion. Never leave temporary `_v2`, `_v3` files loose in `docs/`.

---

## 3. Application Domain: Customer Review Moderation Portal (CRMP)
The application is an enterprise-grade, responsive web platform engineered for real-time customer feedback ingestion, review moderation, sentiment tracking, and content governance:

* **Tech Stack:**
  * **Backend:** Java 17/21+ with Spring Boot 3.x.
  * **Build & Dependency Tool:** Apache Maven (`pom.xml`) with Maven Wrapper (`mvnw`).
  * **Database:** Embedded H2 Database (zero external database setup required, fast in-memory execution, reliable CI test runs).
  * **Frontend / UI:** Spring Boot Thymeleaf + Bootstrap 5 (clean responsive web layout with distinct IDs/classes for reliable Selenium locator targeting).
  * **Health Check & Monitoring:** Spring Boot Actuator (`/actuator/health`) for automated CI/CD and Ansible reliability checks.
* **Core MVP Scope (Strictly 5 Functions):**
  1. *Review Ingestion & Input Validation:* Product ID/Name, Reviewer Name, Rating (1–5 Stars), Review Title, Feedback Comment, with strict input format validation.
  2. *Review Directory & Moderation Queue:* Responsive table with search by product/reviewer, keyword lookup, and status filtering (`PENDING`, `APPROVED`, `REJECTED`, `FLAGGED`).
  3. *Role-Based Status Lifecycle:* State machine transitions enforcing: `PENDING` $\rightarrow$ `APPROVED` $\rightarrow$ `REJECTED` / `FLAGGED`.
  4. *Summary Metrics Dashboard:* Real-time summary KPI cards (Total Reviews, Pending Review Queue, Approved Reviews, Flagged/Rejected Spam, Average Rating).
  5. *Actuator Health Endpoint:* Real-time JSON health status (`UP`) for automated probes and deployment gates.

---

## 4. Git & GitHub Branching Policy
* **Branch Structure:**
  * `main`: Protected production-ready branch. Only tagged releases (`v1.0.0`).
  * `dev`: Integration branch for day-to-day development.
  * `feature/*`: Specific feature branches (e.g., `feature/review-ingestion`, `feature/moderation-queue-dashboard`).
* **Commit Conventions:** Follow Conventional Commits format (`feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `ci: ...`).
* **Collaboration Demo (Tasks 5 & 6):**
  * Raise clean Pull Requests from feature branches into `dev`.
  * Create an intentional Git merge conflict on a shared file, inspect conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), resolve manually, commit resolution, and tag `v1.0.0`.

---

## 5. Automated Testing & Quality Gate (Selenium WebDriver)
* **Framework:** Java + Selenium WebDriver 4.x + JUnit 5 / TestNG + WebDriverManager.
* **Execution Mode:** Headless Chrome / Edge execution for automated CI runs, with local headful support for demonstration.
* **4 Critical User Journeys to Cover:**
  1. Reviewer navigates to `/submit`, fills form (rating, title, comment), asserts review is submitted with `PENDING` status.
  2. Validation gate: Submitting empty comment, invalid rating (<1 or >5), or profanity triggers inline validation error message.
  3. Search & filter: Moderator searches by product keyword and filters table by status (`PENDING`, `APPROVED`, `FLAGGED`, `REJECTED`).
  4. Status action: Moderator clicks "Approve", "Flag", or "Reject" and verifies review status tag updates dynamically.
* **Screenshot Failure Mechanism:** Implement an `@AfterEach` or `TestWatcher` hook that automatically saves a timestamped PNG into `screenshots/failures/` on any assertion failure.
* **Jenkins Quality Gate (Task 10):**
  * The pipeline must execute `mvn test`.
  * If tests fail, Jenkins **must immediately stop execution** and abort all subsequent Docker and deployment stages.
  * An intentional defect experiment must be recorded: introduce a bug $\rightarrow$ show pipeline failure $\rightarrow$ fix bug $\rightarrow$ show pipeline success.

---

## 6. Docker Containerization & Deployment
* **Dockerfile Standard:** Multi-stage build (Stage 1: Maven build, Stage 2: Minimal Eclipse Temurin JRE runtime) to ensure lightweight, secure images.
* **Container Lifecycle Commands:** Must document `build`, `tag`, `run`, `ps`, `logs`, `stop`, `restart`, and `rm`.
* **Port Mapping:** Host port `8080` $\rightarrow$ Container port `8080`.
* **CD Pipeline:** Jenkinsfile automatically tags Docker image with build number (`review-app:${BUILD_NUMBER}`) and updates the running container.

---

## 7. Configuration Management with Ansible
* **Files:** Clean inventory file (`hosts.ini`) and structured playbook (`playbook.yml`).
* **Prerequisites Managed:** System updates, Java runtime, Docker engine, required directories (`/opt/review-app`), firewall ports (8080).
* **Idempotency Rule:** Running `ansible-playbook -i hosts.ini playbook.yml` a second time **must yield 0 changes** (`changed=0, failed=0`).
* **Rollback & Verification:** Must demonstrate automated curl health-check against `/actuator/health` and a rollback task restoring the prior stable container tag.

---

## 8. Evidence & Screenshot Quality Standards
* **No Clutter:** Screenshots must be strictly cropped to exclude Windows taskbars, unrelated desktop windows, or browser chrome unless illustrating full-screen flow.
* **Standard Resolution:** Centered in Word documents, scaled to a maximum width of `6.0` to `6.2` inches so it never causes page overflow.
* **Captions:** Every inserted figure must have a centered, bold caption: `Figure {TaskNo}.{FigNo}: {Description}`.
* **Raw & Processed Separation:**
  * Raw screenshots: `screenshots/task{N}/raw/`
  * Cleaned/cropped: `screenshots/task{N}/`

---

## 9. Quality & Zero-Regression Checklist (Before Finalizing Any Task)
- [ ] Student name and roll number verified (`Rushikesh Gawade` / `23102A0052`).
- [ ] Task title matches the official syllabus allocation exactly.
- [ ] Document generated and opens without XML corruption.
- [ ] Code snippets and configuration syntax validated.
- [ ] All tables contain complete, realistic domain data (no dummy placeholders like `TODO` or `Lorem Ipsum`).
- [ ] Conclusion reflects genuine academic analysis.
