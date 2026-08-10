// Jenkinsfile — declarative pipeline for ai-devops-bot
// This mirrors the GitHub Actions CI pipeline but runs on
// a self-hosted Jenkins server inside Docker.
//
// Interview talking point:
// "I implemented the same pipeline in both GitHub Actions (cloud-native)
//  and Jenkins (self-hosted) to demonstrate understanding of both approaches"

pipeline {

    // ── AGENT ──
    // 'any' means run on any available Jenkins agent.
    // In production this would be a specific agent label like 'docker' or 'linux'
    agent any

    // ── ENVIRONMENT ──
    // Variables available to all stages.
    // Credentials are stored in Jenkins Credentials Store — never hardcoded.
    environment {
        REPO_NAME    = 'ai-devops-bot'
        DOCKER_IMAGE = "ghcr.io/ganeshputran/ai-devops-bot"
        PYTHON_VERSION = '3.11'
    }

    // ── OPTIONS ──
    // Pipeline-level settings
    options {
        timeout(time: 30, unit: 'MINUTES')  // fail if pipeline runs over 30 mins
        buildDiscarder(logRotator(numToKeepStr: '10'))  // keep last 10 builds
        disableConcurrentBuilds()  // don't run two builds at same time
    }

    stages {

        // ── STAGE 1: CHECKOUT ──
        // Jenkins clones the repo into its workspace.
        // Interview: "Jenkins checks out from SCM — Source Control Management"
        stage('Checkout') {
            steps {
                echo "Checking out code from GitHub..."
                checkout scm
                echo "Branch: ${env.BRANCH_NAME}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }

        // ── STAGE 2: SETUP ──
        // Install Python dependencies needed for testing.
        stage('Setup') {
            steps {
                echo "Setting up Python environment..."
                sh '''
                    python3 --version
                    pip3 install pytest pytest-cov --quiet
                    echo "Dependencies installed"
                '''
            }
        }

        // ── STAGE 3: TEST ──
        // Run pytest and save results.
        // Interview: "Always test before build — fail fast principle"
        stage('Test') {
            steps {
                echo "Running test suite..."
                sh '''
                    python3 -m pytest test_app.py -v \
                        --tb=short \
                        --cov=app \
                        --cov-report=term-missing \
                        2>&1 | tee test_output.txt
                '''
            }
            post {
                always {
                    // Archive test results so they appear in Jenkins UI
                    archiveArtifacts artifacts: 'test_output.txt', allowEmptyArchive: true
                }
                failure {
                    echo "Tests FAILED — check test_output.txt for details"
                }
                success {
                    echo "All tests PASSED"
                }
            }
        }

        // ── STAGE 4: HEALTH CHECK ──
        // Run app.py to verify all live portfolio pages are up.
        // Interview: "We verify live infrastructure as part of the pipeline"
        stage('Health Check') {
            steps {
                echo "Checking portfolio page health..."
                sh '''
                    python3 app.py | tee health_report.txt
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'health_report.txt', allowEmptyArchive: true
                }
                failure {
                    echo "Health check FAILED — one or more pages are down!"
                }
            }
        }

        // ── STAGE 5: BUILD DOCKER IMAGE ──
        // Build the Docker image locally.
        // Interview: "Jenkins can build and tag Docker images as part of CI"
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh """
                    docker build -t ${DOCKER_IMAGE}:jenkins-${env.BUILD_NUMBER} .
                    docker tag ${DOCKER_IMAGE}:jenkins-${env.BUILD_NUMBER} ${DOCKER_IMAGE}:jenkins-latest
                    echo "Image built: ${DOCKER_IMAGE}:jenkins-${env.BUILD_NUMBER}"
                """
            }
        }

    }

    // ── POST ──
    // Runs after all stages regardless of outcome.
    // Interview: "Post section handles notifications and cleanup"
    post {
        success {
            echo """
            ✅ Pipeline PASSED
            Job:    ${env.JOB_NAME}
            Build:  #${env.BUILD_NUMBER}
            Branch: ${env.BRANCH_NAME}
            """
        }
        failure {
            echo """
            ❌ Pipeline FAILED
            Job:    ${env.JOB_NAME}
            Build:  #${env.BUILD_NUMBER}
            Check the logs above for details.
            """
        }
        always {
            // Clean workspace after build to save disk space
            cleanWs()
        }
    }
}
