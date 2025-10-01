@Library("jenkins-shared") _
pipeline {
    agent any
    parameters {
        booleanParam(name: 'Deploy_with_DockerCompose', defaultValue: false, description: 'Deploys Docker Image Locally with docker compose')
        booleanParam(name: 'Push_to_DockerHub', defaultValue: false, description: 'Uploads the Image to the Docker Hub') 
        string(name: 'IMAGE_TAG_F', defaultValue: latest, description: 'Enter the Frontend Docker image tag')
        string(name: 'IMAGE_TAG_B', defaultValue: latest, description: 'Enter the Backend Docker image tag')
    }
    environment {
        SONAR_EV = tool 'Sonar'
        FRONTEND = "gehenna-frontend-ii"
        BACKEND = "gehenna-backend-ii"
        DOCKERHUB_USER = "namanss"
    }
    tools {
        nodejs 'nodejs20'
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
        stage('SonarQube Analysis') {
            steps {
                script {
                    sonarqube_analysis(SONAR_EV, "gehenna", "gehenna")
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    sonarqube_QualityGate(5, true) 
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
        stage('Build Frontend & Backend') {
            parallel {
                stage ('Build Frontend') {
                    steps {
                        script {
                            docker_build("${FRONTEND}", "${params.IMAGE_TAG_F}", "${DOCKERHUB_USER}", "./frontend")
                        }
                    }
                }
                stage ('Build Backend') {
                    steps {
                        script {
                            docker_build("${BACKEND}", "${params.IMAGE_TAG_B}", "${DOCKERHUB_USER}", "./backend")
                        }
                    }
                }
            }
        }
        stage('Trivy Image Scan') {
            parallel {
                stage('Scan Frontend Image') {
                    steps {
                        script {
                            trivy_image_scan("${FRONTEND}", "${params.IMAGE_TAG_F}")
                        }
                    }
                }
                stage('Scan Backend Image') {
                    steps {
                        script {
                            trivy_image_scan("${BACKEND}", "${params.IMAGE_TAG_B}")  
                        }
                    }
                }
            }
        }
        stage('Push To Dockerhub') {
            when {
                expression { params.Push_to_DockerHub }
            }
            parallel {
                stage('Pushing Frontend to Dockerhub') {
                    steps {
                        script {
                            docker_push("${FRONTEND}", "${params.IMAGE_TAG_F}", "${DOCKERHUB_USER}")
                        }
                    }
                }
                stage('Pushing Backend to Dockerhub') {
                    steps {
                        script {
                            docker_push("${BACKEND}", "${params.IMAGE_TAG_B}", "${DOCKERHUB_USER}")
                        }
                    }
                }
            }
        }
        stage('Deploy with Docker-Compose') {
            when {
                expression { params.Deploy_with_DockerCompose }
            }
            steps {
                script {
                    docker_compose()
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'trivyfs.txt,trivy-image.json,trivy-image.txt,dependency-check-report.xml,gitleaks-report.json', allowEmptyArchive: true
            emailext (
                subject: "${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build ${currentBuild.currentResult}\nProject: ${env.JOB_NAME}\nBuild: #${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}",
                to: 'ssnaman4@gmail.com',
                attachmentsPattern: 'trivyfs.txt,trivy-image.json,trivy-image.txt,dependency-check-report.xml'
            )
        }
        cleanup {
            sh 'docker system prune -f || true'
        }
    }
}