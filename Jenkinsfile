pipeline {
    agent any

    environment {
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        DATADOG_API_KEY = credentials('DATADOG_API_KEY')
        DATADOG_APP_KEY = credentials('DATADOG_APP_KEY')
        IMAGE_NAME = "davaparma/my-html-app"
    }

    options {
        datadog(collectLogs: true, tags: ["env:production", "team:devops"])
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/davaparma/bin_iot.git', branch: 'main'
            }
        }
        stage('Prepare Docker Context') {
            steps {
                echo 'Preparing Docker context with only the required files...'
                sh '''
                    rm -rf docker-context
                    mkdir docker-context
                    cp hello_sit223.html docker-context/
                    cp test_html.js docker-context/
                    echo "FROM node:alpine" > docker-context/Dockerfile
                    echo "COPY hello_sit223.html /app/hello_sit223.html" >> docker-context/Dockerfile
                    echo "COPY test_html.js /app/test_html.js" >> docker-context/Dockerfile
                    echo "WORKDIR /app" >> docker-context/Dockerfile
                    echo "RUN npm install puppeteer" >> docker-context/Dockerfile
                    echo 'CMD ["node", "test_html.js"]' >> docker-context/Dockerfile
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building the Docker image with Docker...'
                sh '''
                    cd docker-context
                    docker build -t my-html-app:latest .
                '''
                echo 'Tagging the Docker image...'
                sh 'docker tag my-html-app:latest ${IMAGE_NAME}:latest'

                echo 'Pushing the Docker image to Docker Hub...'
                sh 'docker login -u davaparma -p $DOCKER_HUB_PASSWORD'
                sh 'docker push ${IMAGE_NAME}:latest'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests for HTML using the Docker image...'
                sh '''
                    docker pull ${IMAGE_NAME}:latest
                    docker run --rm ${IMAGE_NAME}:latest
                '''
            }
        }
        // Subsequent stages remain unchanged
    }
}
