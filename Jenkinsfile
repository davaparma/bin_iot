pipeline {
    agent any

    environment {
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/davaparma/bin_iot.git', branch: 'main'
            }
        }
        stage('Build') {
            steps {
                echo 'Building the Docker image with Docker Compose...'
                sh 'docker-compose build'
                echo 'Tagging the Docker image...'
                sh 'docker tag my-python-app:latest davaparma/my-python-app:latest'

                echo 'Pushing the Docker image to Docker Hub...'
                sh 'docker login -u davaparma -p $DOCKER_HUB_PASSWORD'
                sh 'echo $DOCKER_HUB_PASSWORD | docker login -u davaparma --password-stdin'
                sh 'docker push davaparma/my-python-app:latest'
            }
        }
        stage('Test') {
            steps {
                echo 'Running Python unittest for Smart Bin IoT project!'
                sh 'docker-compose run app python3 -m unittest test_bin_iot.py'
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
                echo 'Deploying to test environment with Docker Compose...'
                sh 'docker-compose pull'
                sh 'docker-compose up -d'
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
