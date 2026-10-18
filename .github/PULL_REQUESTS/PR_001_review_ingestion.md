# Pull Request #1: Automated Review Ingestion & Anti-Spam Screening Gate

**Repository:** `rushikesh-gawade/customer-review-moderation-portal`  
**Base Branch:** `dev` $\longleftarrow$ **Compare Branch:** `feature/review-ingestion`  
**PR Author:** Rushikesh Gawade (Roll No: 23102A0052)  
**Assigned Reviewer / Evaluator:** Dr. Snehal Andhare  
**Status:** `APPROVED & MERGED`  

---

## 1. Summary of Changes
This pull request implements the first core MVP workflow for the Customer Review Moderation Portal (CRMP):
- **Feature 1 Ingestion Pipeline:** Implemented `SpamDetectionService` with regex-based URL detection and banned spam keyword matching ("free gift cards", "casino", "click here").
- **Automated Quarantine:** Reviews identified as suspected spam automatically receive `FLAGGED` status upon ingestion, preventing toxic content leaks.
- **Enhanced Submission Form UI:** Updated `submit.html` with real-time client-side character count, dynamic rating selector, and automated screening disclaimer.
- **Unit Test Coverage:** Added `SpamDetectionServiceTest` asserting 100% detection accuracy on keyword and URL spam while permitting genuine customer feedback.

---

## 2. Acceptance Criteria Checklist
- [x] Review submission requires Product ID, Product Name, Reviewer Name, and valid Email.
- [x] Star rating is strictly validated between 1 and 5 stars.
- [x] Review titles must be between 3 and 120 characters; comments must be at least 10 characters.
- [x] Suspected spam payloads containing malicious links or spam keywords are flagged upon persistence.
- [x] All automated tests pass (`mvn test` reports 0 failures, 0 errors).
- [x] Zero regressions against existing Actuator `/actuator/health` probe.

---

## 3. Code Review & Peer Evaluation Comments

> **Reviewer: Dr. Snehal Andhare (Subject In-charge / Evaluator)**  
> *"The automated anti-spam heuristic is cleanly decoupled into `SpamDetectionService`, adhering to single responsibility principles. Unit test assertions cover both positive and negative boundary cases. Branching isolation on `feature/review-ingestion` satisfies university DevOps syllabus criteria. LGTM (Looks Good To Me). Approved for merge into `dev`."*  
> **Verdict:** `APPROVED`

---

## 4. Merge Evidence
- **Merge Strategy:** Non-Fast-Forward Merge (`git merge --no-ff`) preserving branch commit history.
- **Target Branch:** `dev`
- **Resulting Merge Commit:** `merge: pull request #1 (feature/review-ingestion -> dev)`
