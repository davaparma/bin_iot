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
                echo 'Running Python unittest for Smart Bin IoT project!'
                sh 'python3 -m unittest test_bin_iot.py'
            }
        }

        stage('Code Quality Analysis') {
            environment {
                SONARQUBE_SCANNER_HOME = tool 'SonarQube Scanner'
            }
            steps {
                withSonarQubeEnv('Local SonarQube') { 
                    sh "${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=bin_iot \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN}"
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
