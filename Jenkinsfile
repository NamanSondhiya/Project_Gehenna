@Library("jenkins-shared") _
pipeline {
    agent any
    environment {
        SONAR_EV = tool 'Sonar'
        IMAGE_TAG = "$(BUILD_NUMBER)"
    }
    stages {
        stage('Clean the Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('CodeClone From GitHub') {
            steps {
                scripts{
                    code_checkout("https://github.com/NamanSondhiya/Project_Gehenna.git", "devOps")
                }
            }
        }
    }
}