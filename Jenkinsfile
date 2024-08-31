pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID') // Replace with your Jenkins credential ID for AWS Access Key
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY') // Replace with your Jenkins credential ID for AWS Secret Key
        AWS_REGION = 'us-east-2' // Set your AWS region
        ECR_REPOSITORY = '481665086534.dkr.ecr.us-east-2.amazonaws.com/my-python-app' // Your ECR repository URL
        ECS_CLUSTER = 'Jenny' // Your ECS Cluster name
        ECS_SERVICE = 'Jenny' // Your ECS Service name
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
                sh 'docker tag my-python-app:latest ${ECR_REPOSITORY}:latest'
            }
        }

        stage('Authenticate with ECR') {
            steps {
                echo 'Authenticating with Amazon ECR...'
                sh '''
                aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                echo 'Pushing the Docker image to ECR...'
                sh 'docker push ${ECR_REPOSITORY}:latest'
            }
        }

        stage('Deploy to ECS') {
            steps {
                echo 'Deploying the new Docker image to ECS...'
                sh '''
                aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --force-new-deployment --region $AWS_REGION
                '''
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
