pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/davaparma/bin_iot.git', branch: 'main'
            }
        }

        stage('Build') {
            steps {
                echo 'Building the Docker image...'
                sh 'docker build -t my-python-app:latest .' 
                sh 'docker save my-python-app:latest -o my-python-app.tar'
                archiveArtifacts artifacts: 'my-python-app.tar', allowEmptyArchive: true 
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests for Smart Bin IoT project!'
                sh 'python3 pipeline_calls.py test'
            }
        }

        stage('Code Quality Analysis') {
            environment {
                SONARQUBE_SCANNER_HOME = tool 'SonarQube Scanner' // Make sure the tool name matches what you configured
            }
            steps {
                withSonarQubeEnv('Local SonarQube') { // Replace 'Local SonarQube' with the name you gave to your SonarQube instance
                    sh "${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=bin_iot \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.login=YOUR_SONARQUBE_TOKEN"
                }
            }
        }

        stage('Deploy to Test Environment') {
            steps {
                echo 'Deploying to test environment for Smart Bin IoT project!'
                sh 'python3 pipeline_calls.py deploy'
            }
        }

        stage('Release to Production') {
            steps {
                echo 'Releasing to production for Smart Bin IoT project!'
                sh 'python3 pipeline_calls.py release'
            }
        }

        stage('Monitoring & Alerts') {
            steps {
                echo 'Setting up monitoring and alerts for Smart Bin IoT project!'
                sh 'python3 pipeline_calls.py monitoring'
            }
        }
    }
}
