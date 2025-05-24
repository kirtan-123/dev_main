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
                    
                    // Point shell to minikube's docker-daemon
                    bat "minikube docker-env --shell cmd > minikube-env.bat"
                    bat "call minikube-env.bat"
                }
            }
        }
        
        stage('Build and Load Docker Image') {
            steps {
                script {
                    // Clean up any existing deployment
                    bat "kubectl delete deployment schedule-tracker --ignore-not-found=true"
                    bat "kubectl delete pods --all --ignore-not-found=true"
                    
                    // Build the image
                    bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    // Verify the image exists
                    bat "docker images | findstr ${DOCKER_IMAGE}"
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                script {
                    // Apply PersistentVolume and PersistentVolumeClaim
                    bat "kubectl apply -f kubernetes/persistent-volume.yaml"
                    
                    // Apply the static deployment.yaml
                    bat "kubectl apply -f kubernetes/deployment.yaml"
                    
                    // Apply Service
                    bat "kubectl apply -f kubernetes/service.yaml"
                    
                    // Wait for deployment with timeout and improved error handling
                    timeout(time: 5, unit: 'MINUTES') {
                        script {
                            def rolloutStatus = bat(script: "kubectl rollout status deployment/schedule-tracker", returnStatus: true)
                            if (rolloutStatus != 0) {
                                echo "Deployment failed. Checking pod status..."
                                bat "kubectl get pods"
                                bat "kubectl describe deployment schedule-tracker"
                                bat "kubectl describe pods"
                                // Optionally fetch pod logs for more diagnostics
                                def podList = bat(script: "kubectl get pods -l app=schedule-tracker -o jsonpath='{.items[*].metadata.name}'", returnStdout: true).trim()
                                if (podList) {
                                    podList.split(' ').each { pod ->
                                        echo "Logs for pod: ${pod}"
                                        bat "kubectl logs ${pod}"
                                    }
                                }
                                error("Deployment rollout failed")
                            }
                        }
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
                bat "kubectl describe pods"
            }
        }
    }
} 