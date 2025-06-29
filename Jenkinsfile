pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "schedule-tracker"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "default"
        KUBECONFIG = "C:/Users/Kirtan/.kube/config"
        CHANGE_MINIKUBE_NONE_USER = 'true'
    }

    stages {
        stage('Check Docker Access') {
            steps {
                echo "Verifying Docker access..."
                bat "docker info"
            }
        }

        stage('Debug Minikube Access') {
            steps {
                bat "whoami"
                bat "minikube status"
                bat "kubectl config current-context"
            }
        }

        stage('Start Minikube') {
            steps {
                echo "Starting Minikube if not already running..."
                bat '''
                @echo off
                minikube status | findstr /C:"Running"
                if %ERRORLEVEL% NEQ 0 (
                    minikube start
                )
                '''
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Use Minikube Docker Daemon') {
            steps {
                echo "Pointing Docker to Minikube's Docker daemon..."
                bat '''
                @echo off
                for /f "tokens=*" %%i in ('minikube docker-env --shell cmd') do call %%i
                '''
            }
        }

        stage('Build Docker Image in Minikube') {
            steps {
                dir('c:/Users/Kirtan/Desktop/dev_main') {
                    bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
                    bat "docker images | findstr %DOCKER_IMAGE%"
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                dir('c:/Users/Kirtan/Desktop/dev_main') {
                    script {
                        echo "Deploying to Minikube cluster..."
                        def fileExists = fileExists 'kubernetes/deployment.yaml'
                        if (!fileExists) {
                            error "deployment.yaml not found in kubernetes folder"
                        }

                        bat "kubectl apply -f kubernetes/deployment.yaml"

                        timeout(time: 2, unit: 'MINUTES') {
                            bat "kubectl rollout status deployment/schedule-tracker"
                        }

                        // ✅ NEW: Get service URL from Minikube
                        
                }
            }
        }
    }

    post {
        success {
            script {
                def minikubeIP = bat(script: "minikube ip", returnStdout: true).trim()
                echo "✅ Deployment completed successfully!"
                echo "📡 Minikube IP: ${minikubeIP}"
            }
        }

        failure {
            script {
                echo "❌ Deployment failed. Collecting logs..."
                bat "kubectl get pods -o wide"
                bat "kubectl describe deployment schedule-tracker"
                bat "kubectl describe pods"
            }
        }
    }
}
