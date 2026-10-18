# ==============================================================================
# Multi-Stage Dockerfile for Customer Review Moderation Portal (CRMP)
# Student: Rushikesh Gawade (Roll No: 23102A0052) | Evaluator: Dr. Snehal Andhare
# Subject: DevOps Lab - Task 11 (Docker Image and Container Lifecycle)
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Maven Build & Dependency Packaging
# ------------------------------------------------------------------------------
FROM maven:3.9.6-eclipse-temurin-21 AS builder

LABEL maintainer="Rushikesh Gawade <gawaderushikesh576@gmail.com>"
LABEL project="customer-review-moderation-portal"
LABEL role="build-stage"

WORKDIR /build

# Copy Maven Project Descriptor and Cache Dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy Source Code and Compile Executable JAR
COPY src ./src
RUN mvn clean package -DskipTests=true -B

# ------------------------------------------------------------------------------
# Stage 2: Minimal Production JRE Runtime
# ------------------------------------------------------------------------------
FROM eclipse-temurin:21-jre-alpine AS runtime

LABEL maintainer="Rushikesh Gawade <gawaderushikesh576@gmail.com>"
LABEL project="customer-review-moderation-portal"
LABEL version="1.0.0"
LABEL role="runtime-stage"

# Create unprivileged application user and service group for security hardening
RUN addgroup -S crmpgroup && adduser -S crmpuser -G crmpgroup

WORKDIR /app

# Copy compiled executable JAR from builder stage
COPY --from=builder /build/target/customer-review-moderation-portal-*.jar /app/crmp.jar
RUN chown -R crmpuser:crmpgroup /app

# Configure non-root user
USER crmpuser

# Container Port Exposure
EXPOSE 8080

# Environment Configuration
ENV SPRING_PROFILES_ACTIVE=production \
    SERVER_PORT=8080 \
    JAVA_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC -XX:+ExitOnOutOfMemoryError"

# Automated Healthcheck for Container Lifecycle Monitoring
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
    CMD wget -q --spider http://localhost:8080/actuator/health || exit 1

# Container Process Entrypoint
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/crmp.jar"]
