pipeline {

    agent any

    environment {
        IMAGE_NAME = "jenkins-docker-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} \
                    -t ${IMAGE_NAME}:latest \
                    .
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image \
                    --format table \
                    --output trivy-report.txt \
                    ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    IMAGE_TAG=${IMAGE_TAG} \
                    docker compose up -d --no-build
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 15
                    curl --fail http://localhost:5000/health
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                    docker image prune -f
                '''
            }
        }
    }

    post {

        always {
            archiveArtifacts artifacts: 'trivy-report.txt',
            allowEmptyArchive: true
        }

        success {
            echo 'CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'CI/CD pipeline failed.'
        }
    }
}
