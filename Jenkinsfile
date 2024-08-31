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
                echo 'Building Smart Bin IoT project!'
                sh 'python3 pipeline_calls.py build'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests for Smart Bin IoT project!'
                sh 'python3 pipeline_calls.py test'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Analyzing code quality for Smart Bin IoT project!'
                sh 'python3 pipeline_calls.py code_quality'
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
                echo 'Setting up monitoring and alerts for Smart Bin IoT project!
                sh 'python3 pipeline_calls.py monitoring'
            }
        }
    }
}
