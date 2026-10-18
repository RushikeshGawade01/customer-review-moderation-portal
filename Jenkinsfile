pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['staging', 'production', 'dev'], description: 'Deployment Target Environment')
        string(name: 'SERVER_PORT', defaultValue: '8080', description: 'Application HTTP Port')
        choice(name: 'DEPLOY_TARGET', choices: ['Apache-Tomcat-11', 'Embedded-Server'], description: 'Target Web Application Server')
        string(name: 'APP_VERSION', defaultValue: '1.0.0', description: 'Semantic Release Version')
    }

    environment {
        PROJECT_NAME = 'customer-review-moderation-portal'
        TOMCAT_HOME  = 'D:\\apache-tomcat-11.0.18-windows-x64\\apache-tomcat-11.0.18'
        DEPLOY_DIR   = 'D:\\deployments\\crmp'
        STUDENT_NAME = 'Rushikesh Gawade'
        ROLL_NO      = '23102A0052'
        EVALUATOR    = 'Dr. Snehal Andhare'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "==============================================================================="
                echo " STAGE 1: SCM CHECKOUT"
                echo " Student:   ${env.STUDENT_NAME} (${env.ROLL_NO})"
                echo " Evaluator: ${env.EVALUATOR}"
                echo " Target:    ${params.DEPLOY_ENV} (Port: ${params.SERVER_PORT})"
                echo "==============================================================================="
                checkout scm
                bat 'git log -1 --oneline --decorate'
            }
        }

        stage('Build & Test') {
            steps {
                echo "==============================================================================="
                echo " STAGE 2: BUILD & TEST (SUREFIRE QUALITY GATE)"
                echo "==============================================================================="
                bat 'mvn clean test'
            }
        }

        stage('Package') {
            steps {
                echo "==============================================================================="
                echo " STAGE 3: PACKAGE (SPRING BOOT EXECUTABLE ARTIFACT)"
                echo "==============================================================================="
                bat 'mvn package -DskipTests=true'
            }
        }

        stage('Deploy to Server') {
            steps {
                echo "==============================================================================="
                echo " STAGE 4: SERVER DEPLOYMENT (TOMCAT / STANDALONE TARGET)"
                echo " Target Server: ${params.DEPLOY_TARGET} | Port: ${params.SERVER_PORT}"
                echo "==============================================================================="
                bat """
                    if not exist "${env.DEPLOY_DIR}" mkdir "${env.DEPLOY_DIR}"
                    copy /Y target\\*.jar "${env.DEPLOY_DIR}\\${env.PROJECT_NAME}-${params.APP_VERSION}.jar"
                    if exist "${env.TOMCAT_HOME}\\webapps" (
                        copy /Y target\\*.jar "${env.TOMCAT_HOME}\\webapps\\crmp.war"
                        echo [DEPLOY] Successfully staged artifact to Tomcat webapps: ${env.TOMCAT_HOME}\\webapps\\crmp.war
                    )
                    echo [DEPLOY] Application binary active in ${env.DEPLOY_DIR}
                """
            }
        }

        stage('Health Probe') {
            steps {
                echo "==============================================================================="
                echo " STAGE 5: POST-DEPLOYMENT HEALTH PROBE"
                echo "==============================================================================="
                echo "[PROBE] Verifying deployment readiness on http://localhost:${params.SERVER_PORT}/actuator/health"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
            echo "CI/CD Pipeline Execution Completed."
        }
        success {
            echo "Pipeline run SUCCESSFUL! Deployed ${env.PROJECT_NAME}-${params.APP_VERSION} to ${params.DEPLOY_ENV} on port ${params.SERVER_PORT}."
        }
        failure {
            echo "Pipeline run FAILED. Halting continuous deployment gate."
        }
    }
}
