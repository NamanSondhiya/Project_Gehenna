@Library("jenkins-shared") _
pipeline {
    agent any
    environment {
        SONAR_EV = tool 'Sonar'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Clean the Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('CodeClone From GitHub') {
            steps {
                script {
                    git_clone("https://github.com/NamanSondhiya/Project_Gehenna.git", "devOps")
                }
            }
        }
        stage('GitLeaks Scan') {
            steps {
                sh 'gitleaks detect --source . -r gitleaks-report.json || true'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    sonarqube_analysis(SONAR_EV, "gehenna", "gehenna", "SonarToken")
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    sonarqube_QualityGates(2, true)           
                }
            }
        }
        stage('Owasp Dependency Check') {
            steps {
                script {
                    owasp_scan()
                }
            }
        }
        stage('Trivy FileSystem Scan') {
            steps {
                script {
                    trivy_fs_scan()
                }
            }
        }
    }
}