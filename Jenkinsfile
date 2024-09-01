pipeline {
    agent any

    environment {
        DOCKER_HUB_PASSWORD = credentials('DOCKER_HUB_PASSWORD')
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        DATADOG_API_KEY = credentials('DATADOG_API_KEY')
        DATADOG_APP_KEY = credentials('DATADOG_APP_KEY')
        IMAGE_NAME = "davaparma/my-python-app"  // Define the image name without the tag
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
                    cp app.py test_smart_bin.py Dockerfile requirements.txt docker-context/
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building the Docker image with Docker Compose...'
                sh '''
                    cd docker-context
                    docker build --platform linux/amd64 -t my-python-app:latest .
                '''
                echo 'Tagging the Docker image...'
                sh 'docker tag my-python-app:latest ${IMAGE_NAME}:latest'

                echo 'Pushing the Docker image to Docker Hub...'
                sh 'docker login -u davaparma -p $DOCKER_HUB_PASSWORD'
                sh 'docker push ${IMAGE_NAME}:latest'
            }
        }

stage('Test') {
    steps {
        echo 'Running Python unittest for Smart Bin IoT project using the Docker image...'
        sh '''
            docker run --rm ${IMAGE_NAME}:latest python app.py test
        '''
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
                --docker-custom-image-name ${IMAGE_NAME}:latest \
                --docker-registry-server-url https://index.docker.io \
                --docker-registry-server-user davaparma \
                --docker-registry-server-password $DOCKER_HUB_PASSWORD
        '''
        sh 'az webapp restart --name mydockerapp --resource-group my-docker-rg'
    }
}


        stage('Monitoring & Alerts') {
            steps {
                echo 'Turning Datadog monitor off and on to trigger alert...'
                sh '''
                    curl -X POST -H "Content-type: application/json" \
                    -H "DD-API-KEY: ${DATADOG_API_KEY}" \
                    -H "DD-APPLICATION-KEY: ${DATADOG_APP_KEY}" \
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
