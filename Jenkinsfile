pipeline {
    agent any

    environment {
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
        DOCKER_HUB_USERNAME = credentials('DOCKER_HUB_USERNAME')
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
                sh 'docker tag my-python-app:latest ${DOCKER_HUB_USERNAME}/my-python-app:latest'

                echo 'Pushing the Docker image to Docker Hub...'
                sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin'
                sh 'docker push ${DOCKER_HUB_USERNAME}/my-python-app:latest'
            }
        }

        stage('Test') {
            steps {
                echo 'Running Python unittests for Smart Bin IoT project...'
                sh 'docker-compose run app python3 -m unittest test_bin_iot.py'
            }
        }

        stage('Deploy to Test Environment') {
            steps {
                echo 'Deploying to test environment with Docker Compose...'
                sh 'docker-compose up -d'
            }
        }

        stage('Release to Production') {
            steps {
                echo 'Releasing to production environment...'
                sh 'docker-compose pull'
                sh 'docker-compose up -d --build'
            }
        }

        stage('Monitoring & Alerts') {
            steps {
                echo 'Setting up monitoring and alerts for Smart Bin IoT project...'
                sh 'python3 pipeline_calls.py monitoring'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}
