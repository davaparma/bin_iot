pipeline {
    agent any

    environment {
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
        DOCKER_HUB_USERNAME = credentials('DOCKER_HUB_USERNAME')
        OCTOPUS_API_KEY = credentials('OCTOPUS_API_KEY') // Add your Octopus API key as a Jenkins credential
        OCTOPUS_SERVER = 'https://davaparma.octopus.app/' // Replace with your Octopus Deploy instance URL
        OCTOPUS_PROJECT = 'Demo Deployment' // Replace with your Octopus project name
        OCTOPUS_ENVIRONMENT = 'Production' // Replace with your Octopus environment name
        OCTOPUS_PACKAGE = 'davaparma/my-python-app:latest' // The Docker image you're deploying
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
                sh 'echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin'
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
                    sh """
                    ${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=bin_iot \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.login=${SONAR_AUTH_TOKEN} \
                        -Dsonar.python.version=3.x
                    """
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
                echo 'Deploying to production environment using Octopus Deploy...'
                sh """
                octo create-release \
                    --project="${OCTOPUS_PROJECT}" \
                    --version="1.0.${env.BUILD_NUMBER}" \
                    --deploy-to="${OCTOPUS_ENVIRONMENT}" \
                    --package="${DOCKER_IMAGE}" \
                    --server="${OCTOPUS_SERVER}" \
                    --apiKey="${OCTOPUS_API_KEY}"
                """
                echo 'Running Docker Compose for production environment...'
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

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}
