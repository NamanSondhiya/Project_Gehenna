@Library("jenkins-shared") _
pipeline {
    agent any
    parameters {
        booleanParam(name: 'Deploy_with_DockerCompose', defaultValue: false, description: 'Deploys Docker Image Locally with docker compose') 
    }
    environment {
        SONAR_EV = tool 'Sonar'
        FRONTEND = "gehenna-frontend-ii"
        BACKEND = "gehenna-backend-ii"
        IMAGE_TAG = "${BUILD_NUMBER}"
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
                            docker_build("${FRONTEND}", "${IMAGE_TAG}", "${DOCKERHUB_USER}", "./frontend")
                        }
                    }
                }
                stage ('Build Backend') {
                    steps {
                        script {
                            docker_build("${BACKEND}", "${IMAGE_TAG}", "${DOCKERHUB_USER}", "./backend")
                        }
                    }
                }
            }
        }
        stage('Trivy Image Scan') {
            steps {
                script {
                    trivy_image_scan("${FRONTEND}", "${IMAGE_TAG}")
                    trivy_image_scan("${BACKEND}", "${IMAGE_TAG}")  
                }
            }
        }
        stage('Push To Dockerhub') {
            parallel {
                stage('Pushing Frontend to Dockerhub') {
                    steps {
                        script {
                            docker_push("${FRONTEND}", "${IMAGE_TAG}", "${DOCKERHUB_USER}")
                        }
                    }
                }
                stage('Pushing Backend to Dockerhub') {
                    steps {
                        script {
                            docker_push("${BACKEND}", "${IMAGE_TAG}", "${DOCKERHUB_USER}")
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
}