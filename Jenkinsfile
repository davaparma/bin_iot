pipeline {
    agent any

    environment {
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Building the Docker image with Docker Compose...'
                sh 'docker-compose build'
            }
        }
        stage('Tag Docker Image') {
            steps {
                echo 'Tagging the Docker image...'
                sh 'docker tag my-python-app:latest 481665086534.dkr.ecr.us-east-2.amazonaws.com/my-python-app:latest'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing the Docker image to Docker Hub...'
                sh 'echo $DOCKER_HUB_PASSWORD | docker login -u davaparma --password-stdin'
                sh 'docker push davaparma/my-python-app:latest'
            }
        }
        stage('Push to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    echo 'Pushing the Docker image to Amazon ECR...'
                    sh 'aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 481665086534.dkr.ecr.us-east-2.amazonaws.com/my-python-app'
                    sh 'docker push 481665086534.dkr.ecr.us-east-2.amazonaws.com/my-python-app:latest'
                }
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
                    sh "${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=bin_iot -Dsonar.sources=. -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_AUTH_TOKEN}"
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
                sh 'docker-compose -f docker-compose.production.yml pull'
                sh 'docker-compose -f docker-compose.production.yml up -d'
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
