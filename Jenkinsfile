pipeline {
    agent any

    environment {
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
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
                echo 'Preparing Docker context with only the required file...'
                sh '''
                    rm -rf docker-context   
                    mkdir docker-context
                    cp test_bin_iot.py docker-context/
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building the Docker image with Docker Compose...'
                sh '''
                    cd docker-context
                    docker-compose build
                '''
                echo 'Tagging the Docker image...'
                sh 'docker tag my-python-app:latest davaparma/my-test-app:latest'

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
                
                sh 'az login --service-principal --username $AZURE_CLIENT_ID --password $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID'

                sh '''
                    az webapp config container set \
                        --name mydockerapp \
                        --resource-group my-docker-rg \
                        --docker-custom-image-name davaparma/my-python-app:latest \
                        --docker-registry-server-url https://index.docker.io \
                        --docker-registry-server-user davaparma \
                        --docker-registry-server-password $DOCKER_HUB_PASSWORD
                '''
            }
        }
        stage('Monitoring & Alerts') {
            steps {
                echo 'Turning Datadog monitor off and on to trigger alert...'
                sh '''
                    curl -X POST -H "Content-type: application/json" \
                    -H "DD-API-KEY: 1dabb590cbc7199439a6e9ff39a6b865" \
                    -H "DD-APPLICATION-KEY: 8a5d9b85693e7e1299cdeb458b080210bd0a8db4" \
                    -d '{
                          "name": "Website Online Checker",
                          "type": "metric alert",
                          "query": "avg(last_1h):avg:azure.web_serverfarms.current_instance_count{*} == 1",
                          "message": "Website Successfully Online! @streaky_sling.0o@icloud.com",
                          "tags": ["env:production"],
                          "priority": 3,
                          "options": {
                            "notify_audit": true,
                            "locked": false,
                            "timeout_h": 0,
                            "new_host_delay": 300,
                            "require_full_window": true,
                            "notify_no_data": false,
                            "renotify_interval": 0,
                            "escalation_message": "",
                            "include_tags": true,
                            "thresholds": {
                              "critical": 1
                            },
                            "evaluation_delay": 300
                          }
                        }' \
                    "https://api.us5.datadoghq.com/api/v1/monitor"
                '''
            }
        }
    }
}
