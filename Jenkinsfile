pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "schedule-tracker"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "default"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Minikube') {
            steps {
                script {
                    // Check if Minikube is running
                    def minikubeStatus = bat(script: "minikube status", returnStdout: true).trim()
                    
                    if (!minikubeStatus.contains("Running")) {
                        echo "Starting Minikube..."
                        bat "minikube start --driver=docker"
                    } else {
                        echo "Minikube is already running"
                    }
                    
                    // Configure docker to use minikube's docker daemon
                    bat "minikube docker-env --shell cmd"
                    bat "minikube docker-env --shell cmd | findstr SET > minikube-env.bat"
                    bat "call minikube-env.bat"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image directly in minikube's docker daemon
                    bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                script {
                    // Apply PersistentVolume
                    bat "kubectl apply -f kubernetes/persistent-volume.yaml"
                    
                    // Apply PersistentVolumeClaim
                    bat "kubectl apply -f kubernetes/persistent-volume.yaml"
                    
                    // Apply Deployment
                    bat "kubectl apply -f kubernetes/deployment.yaml"
                    
                    // Apply Service
                    bat "kubectl apply -f kubernetes/service.yaml"
                    
                    // Wait for deployment with timeout and better error handling
                    timeout(time: 5, unit: 'MINUTES') {
                        bat """
                            kubectl rollout status deployment/schedule-tracker || (
                                echo "Deployment failed. Checking pod status..."
                                kubectl get pods
                                kubectl describe deployment schedule-tracker
                                exit 1
                            )
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                def minikubeIP = bat(script: "minikube ip", returnStdout: true).trim()
                echo "Application deployed successfully to Minikube!"
                echo "Access the application at: http://${minikubeIP}:30000"
            }
        }
        failure {
            script {
                echo 'Deployment failed! Checking pod status...'
                bat "kubectl get pods"
                bat "kubectl describe deployment schedule-tracker"
            }
        }
    }
} 