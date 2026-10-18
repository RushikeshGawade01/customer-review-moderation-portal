# Customer Review Moderation Portal (CRMP)

[![Java 21](https://img.shields.io/badge/Java-21%20LTS-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3.4-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Build Status](https://img.shields.io/badge/Build-Passing-success.svg)]()
[![License](https://img.shields.io/badge/License-Academic%20Evaluation-blue.svg)]()

> **University DevOps Laboratory Project**  
> **Student Name:** Rushikesh Gawade  
> **Roll Number:** 23102A0052  
> **Program & Branch:** B.E. Semester VII – Computer Engineering  
> **Subject In-charge / Evaluator:** Dr. Snehal Andhare  
> **Repository:** `https://github.com/rushikesh-gawade/customer-review-moderation-portal.git`

---

## 1. Project Overview
The **Customer Review Moderation Portal (CRMP)** is an enterprise-grade, responsive web platform engineered for real-time customer feedback ingestion, review moderation, sentiment tracking, and content governance. The platform resolves the critical business risks of unmoderated user reviews—such as spam injection, defamatory statements, profanity, and competitor review-bombing—while providing a deterministic, zero-dependency environment for automated CI/CD pipelines.

---

## 2. Core MVP Scope (Strictly 5 Functions)
1. **Review Ingestion & Input Validation (`/reviews/submit`):** End shoppers submit star ratings (1–5), product ID, name, reviewer details, and comments, with strict Jakarta Bean Validation.
2. **Review Directory & Moderation Queue (`/reviews`):** Centralized moderation table with real-time text search across products/comments and status filtering.
3. **Role-Based Moderation State Machine:** Dynamic status transitions governing reviews through `PENDING` $\rightarrow$ `APPROVED` | `REJECTED` | `FLAGGED`.
4. **Summary Metrics KPI Dashboard (`/`):** Real-time metric cards calculating Total Reviews, Pending Queue, Approved Reviews, and Average Star Rating.
5. **Spring Boot Actuator Health Probe (`/actuator/health`):** Real-time JSON health check returning HTTP 200 `{"status":"UP"}` for automated CI/CD and container probes.

---

## 3. Technology Stack & Prerequisites
- **Language / Runtime:** Java 21 LTS (Oracle JDK 21 / Eclipse Adoptium)
- **Framework:** Spring Boot 3.3.4 (Spring MVC, Spring Data JPA, Spring Boot Actuator)
- **Template Engine:** Thymeleaf with Bootstrap 5.3 & Bootstrap Icons
- **Database:** Embedded In-Memory H2 Database (`jdbc:h2:mem:crmpdb`)
- **Build Tool:** Apache Maven 3.9.x
- **Containerization:** Multi-stage Dockerfile (Eclipse Temurin JRE)
- **Configuration Management:** Ansible Playbook & Inventory

---

## 4. Local Build & Execution Guide

### Prerequisites Check
```powershell
java -version
mvn -version
git --version
```

### Clean & Compile
```powershell
mvn clean compile
```

### Execute Automated Test Suite
```powershell
mvn test
```

### Package & Run Application
```powershell
mvn package -DskipTests
java -jar target/customer-review-moderation-portal-1.0.0-SNAPSHOT.jar
```
Application will be accessible at: `http://localhost:8080/`

### Health Check Endpoint
```powershell
curl.exe -s http://localhost:8080/actuator/health
```

---

## 5. Git Branching Strategy & Contribution Guidelines
We strictly enforce a multi-branch Git workflow following the **Conventional Commits** specification:

- `main`: Protected production branch. Only tagged releases (`v1.0.0`) are merged here.
- `dev`: Active integration branch where feature branches merge via Pull Requests.
- `feature/*`: Granular feature branches (e.g., `feature/review-ingestion`, `feature/moderation-queue`).
- `bugfix/*`: Targeted defect fixes.

### Commit Convention
```text
feat: add review status transition logic
fix: resolve null pointer on empty review comment
test: add headless selenium test suite
docs: update architecture diagram and README
ci: configure jenkinsfile pipeline stages
```
