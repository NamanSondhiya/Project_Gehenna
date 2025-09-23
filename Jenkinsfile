pipeline{
    agent any
    environment {
        SCANNER_EV = tool 'Sonar'
    }
    stages{
        stage("Clean WorkSpace") {
            steps {
                cleanWs()
            }
        }
        stage("Clone Code From Github"){
            steps{
                git url:"https://github.com/NamanSondhiya/Project_Gehenna.git" , branch: "devOps"
            }
        }
        stage("Security Scans") {
            parallel{
                stage("GitLeaks Scan") {
                    steps {
                        sh 'gitleaks detect --source . -r gitleaks-report.json -f json || true'
                    }
                }
                stage("trivy file system scan") {
                    steps {
                        sh 'trivy fs . > trivy.txt'
                    }
                }
            }
        }
        stage("SonarQube Analysis") {
            steps {
                withSonarQubeEnv('Sonar') {
                    sh ''' $SCANNER_EV/bin/sonar-scanner -Dsonar.projectName=Gehenna2 -Dsonar.projectKey=Gehnna2 '''
                }
            }
        }
        stage("Quality Gates") {
            steps {
                script {
                    timeout(time: 3, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                    }
                }
            }
        }
        stage("Owasp Dependency Check") {
            steps {
                dependencyCheck additionalArguments: '''--scan ./''', odcInstallation: 'owasp'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage("Build with Docker compose") {
            steps {
                sh 'docker compose down -v --remove-orphans || true'
                sh 'docker compose up -d --build > logs.txt'
            }
        }
    }
    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}