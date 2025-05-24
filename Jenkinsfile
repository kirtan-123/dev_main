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
                        bat "minikube start"
                        
                        // Wait for Minikube to be ready
                        bat "minikube status"
                    } else {
                        echo "Minikube is already running"
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image locally for Minikube
                    bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    // Load image into Minikube
                    bat "minikube image load ${DOCKER_IMAGE}:${DOCKER_TAG}"
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
                    
                    // Wait for deployment to be ready
                    bat "kubectl rollout status deployment/schedule-tracker"
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
            echo 'Deployment failed!'
        }
    }
} 