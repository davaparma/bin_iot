pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-2'
        ECR_REPO = '481665086534.dkr.ecr.us-east-2.amazonaws.com/my-python-app'
        DOCKER_IMAGE_TAG = 'latest'
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
            }
        }

        stage('Tag Docker Image') {
            steps {
                echo 'Tagging the Docker image...'
                sh "docker tag my-python-app:latest ${ECR_REPO}:${DOCKER_IMAGE_TAG}"
            }
        }

        stage('Push to ECR') {
            steps {
                echo 'Pushing the Docker image to Amazon ECR...'
                sh '''
                export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                export AWS_DEFAULT_REGION=${AWS_REGION}
                
                $(aws ecr get-login-password --region ${AWS_REGION}) | docker login --username AWS --password-stdin ${ECR_REPO}
                docker push ${ECR_REPO}:${DOCKER_IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Production') {
            steps {
                echo 'Deploying to production environment using AWS CodeDeploy...'
                sh '''
                aws deploy create-deployment \
                    --application-name MyPythonApp \
                    --deployment-group-name MyAppDeploymentGroup \
                    --s3-location bucket=your-s3-bucket,key=appspec.yml,bundleType=YAML \
                    --region ${AWS_REGION}
                '''
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
