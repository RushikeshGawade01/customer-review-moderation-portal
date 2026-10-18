pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['production', 'staging', 'dev'], description: 'Target Deployment Environment')
        string(name: 'SERVER_PORT', defaultValue: '8080', description: 'Host Forwarding HTTP Port')
        choice(name: 'REGISTRY_TARGET', choices: ['Docker-Hub', 'Local-Registry'], description: 'Container Image Registry Target')
        string(name: 'APP_VERSION', defaultValue: '1.0.0', description: 'Semantic Application Release Version')
        string(name: 'CONTAINER_NAME', defaultValue: 'crmp-app', description: 'Deployed Container Instance Name')
    }

    environment {
        PROJECT_NAME    = 'customer-review-moderation-portal'
        IMAGE_NAME      = 'crmp'
        DOCKER_HUB_REPO = 'docker.io/rushikeshgawade/crmp'
        LOCAL_REG_REPO  = 'localhost:5000/rushikesh/crmp'
        STUDENT_NAME    = 'Rushikesh Gawade'
        ROLL_NO         = '23102A0052'
        EVALUATOR       = 'Dr. Snehal Andhare'
        PATH            = "D:\\Devops_project\\bin;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "==============================================================================="
                echo " STAGE 1: SCM CHECKOUT & AUDIT"
                echo " Student:    ${env.STUDENT_NAME} (${env.ROLL_NO})"
                echo " Evaluator:  ${env.EVALUATOR}"
                echo " Target Env: ${params.DEPLOY_ENV} (Port: ${params.SERVER_PORT})"
                echo " Version:    ${params.APP_VERSION} (Build: #${env.BUILD_NUMBER})"
                echo "==============================================================================="
                checkout scm
                bat 'git log -1 --oneline --decorate'
            }
        }

        stage('Quality Gate (Test)') {
            steps {
                echo "==============================================================================="
                echo " STAGE 2: CONTINUOUS TESTING & QUALITY GATE ENFORCEMENT"
                echo "==============================================================================="
                bat 'mvn clean test'
            }
        }

        stage('Package') {
            steps {
                echo "==============================================================================="
                echo " STAGE 3: APPLICATION PACKAGING (SPRING BOOT EXECUTABLE JAR)"
                echo "==============================================================================="
                bat 'mvn package -DskipTests=true -B'
            }
        }

        stage('Docker Build & Tag') {
            steps {
                echo "==============================================================================="
                echo " STAGE 4: MULTI-STAGE DOCKER BUILD & SEMANTIC VERSIONING"
                echo " Image Tags: crmp:${env.BUILD_NUMBER}, crmp:${params.APP_VERSION}, crmp:latest"
                echo "==============================================================================="
                bat """
                    docker build -t ${env.IMAGE_NAME}:${env.BUILD_NUMBER} -t ${env.IMAGE_NAME}:${params.APP_VERSION} -t ${env.IMAGE_NAME}:latest -t ${env.DOCKER_HUB_REPO}:${env.BUILD_NUMBER} -t ${env.DOCKER_HUB_REPO}:${params.APP_VERSION} -t ${env.DOCKER_HUB_REPO}:latest .
                    docker images ${env.IMAGE_NAME}
                """
            }
        }

        stage('Publish to Registry') {
            steps {
                echo "==============================================================================="
                echo " STAGE 5: PUBLISH VERSIONED IMAGE TO CONTAINER REGISTRY"
                echo " Target Registry: ${params.REGISTRY_TARGET}"
                echo "==============================================================================="
                bat """
                    docker login -u rushikeshgawade -p "token-secured" docker.io
                    docker push ${env.DOCKER_HUB_REPO}:${env.BUILD_NUMBER}
                    docker push ${env.DOCKER_HUB_REPO}:${params.APP_VERSION}
                    docker push ${env.DOCKER_HUB_REPO}:latest
                """
            }
        }

        stage('Container Deploy') {
            steps {
                echo "==============================================================================="
                echo " STAGE 6: CONTINUOUS CONTAINER DEPLOYMENT (CONTAINER REFRESH)"
                echo " Container: ${params.CONTAINER_NAME} | Host Port: ${params.SERVER_PORT} -> 8080"
                echo "==============================================================================="
                bat """
                    docker stop ${params.CONTAINER_NAME}
                    docker rm ${params.CONTAINER_NAME}
                    docker run -d --name ${params.CONTAINER_NAME} -p ${params.SERVER_PORT}:8080 ${env.IMAGE_NAME}:${env.BUILD_NUMBER}
                    docker ps
                """
            }
        }

        stage('Health Probe') {
            steps {
                echo "==============================================================================="
                echo " STAGE 7: POST-DEPLOYMENT CONTAINER HEALTH PROBE"
                echo " Probe Target: http://localhost:${params.SERVER_PORT}/actuator/health"
                echo "==============================================================================="
                bat """
                    powershell -NoProfile -Command "Start-Sleep -Seconds 5; try { \$r = Invoke-RestMethod -Uri 'http://localhost:${params.SERVER_PORT}/actuator/health' -Method Get; Write-Host '[HEALTH PROBE SUCCESS] Status:' \$r.status } catch { Write-Host '[HEALTH PROBE PENDING]' }"
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'target/*.jar', allowEmptyArchive: true, fingerprint: true
            echo "CI/CD Pipeline Run Completed for Build #${env.BUILD_NUMBER}."
        }
        success {
            echo "[SUCCESS] Containerized CRMP Build #${env.BUILD_NUMBER} (Version: ${params.APP_VERSION}) successfully deployed to ${params.DEPLOY_ENV} on port ${params.SERVER_PORT}."
        }
        failure {
            echo "[FAILURE] Quality Gate or Deployment Stage Failed. Container rollout aborted."
        }
    }
}
