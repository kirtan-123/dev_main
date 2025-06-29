pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "schedule-tracker"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "default"
        KUBECONFIG = "C:/Users/Kirtan/.kube/config"
    }

    stages {
        stage('Check Docker Access') {
            steps {
                echo "Verifying Docker access..."
                bat "docker info"
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Start Minikube (if needed)') {
            steps {
                script {
                    def minikubeStatus = bat(script: "minikube status", returnStdout: true).trim()
                    if (!minikubeStatus.contains("Running")) {
                        echo "Minikube not running. Starting Minikube..."
                        // Add --wait=false and --v=5 to reduce hanging
                        timeout(time: 5, unit: 'MINUTES') {
                            bat "minikube start --driver=docker --wait=false --v=5"
                        }
                        sleep 30
                    } else {
                        echo "Minikube is already running"
                    }
                }
            }
        }

        stage('Use Minikube Docker Daemon') {
            steps {
                echo "Pointing Docker to Minikube's Docker daemon..."
                // Inline version of setting docker-env (instead of using bat files)
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
                       

                        // Verify deployment.yaml exists in the kubernetes folder
                        def fileExists = fileExists 'kubernetes/deployment.yaml'
                        if (!fileExists) {
                            error "deployment.yaml not found in kubernetes folder"
                        }
                        
                    
                        
                        // Wait for deployment to be ready
                        timeout(time: 2, unit: 'MINUTES') {
                            bat "kubectl rollout status deployment/schedule-tracker"
                        }
                        
                        // Get service URL
                        def serviceUrl = bat(script: "minikube service schedule-tracker-service --url", returnStdout: true).trim()
                        echo "App available at: ${serviceUrl}"
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                def minikubeIP = bat(script: "minikube ip", returnStdout: true).trim()
                echo "✅ Application deployed successfully to Minikube!"
                echo "Minikube IP: ${minikubeIP}"
            }
        }

        failure {
            script {
                echo "❌ Deployment failed. Gathering debug info..."
                bat "kubectl get pods -o wide"
                bat "kubectl describe deployment schedule-tracker"
                bat "kubectl describe pods"
            }
        }
    }
}