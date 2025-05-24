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
                    // Apply PersistentVolume
                    bat "kubectl apply -f kubernetes/persistent-volume.yaml"
                    
                    // Apply PersistentVolumeClaim
                    bat "kubectl apply -f kubernetes/persistent-volume.yaml"
                    
                    // Create deployment with correct image pull policy
                    bat """
                        echo apiVersion: apps/v1 > deployment.yaml
                        echo kind: Deployment >> deployment.yaml
                        echo metadata: >> deployment.yaml
                        echo   name: schedule-tracker >> deployment.yaml
                        echo spec: >> deployment.yaml
                        echo   replicas: 2 >> deployment.yaml
                        echo   selector: >> deployment.yaml
                        echo     matchLabels: >> deployment.yaml
                        echo       app: schedule-tracker >> deployment.yaml
                        echo   template: >> deployment.yaml
                        echo     metadata: >> deployment.yaml
                        echo       labels: >> deployment.yaml
                        echo         app: schedule-tracker >> deployment.yaml
                        echo     spec: >> deployment.yaml
                        echo       containers: >> deployment.yaml
                        echo       - name: schedule-tracker >> deployment.yaml
                        echo         image: ${DOCKER_IMAGE}:${DOCKER_TAG} >> deployment.yaml
                        echo         imagePullPolicy: Never >> deployment.yaml
                        echo         ports: >> deployment.yaml
                        echo         - containerPort: 5000 >> deployment.yaml
                        echo         volumeMounts: >> deployment.yaml
                        echo         - name: sqlite-data >> deployment.yaml
                        echo           mountPath: /app/instance >> deployment.yaml
                        echo       volumes: >> deployment.yaml
                        echo       - name: sqlite-data >> deployment.yaml
                        echo         persistentVolumeClaim: >> deployment.yaml
                        echo           claimName: sqlite-pvc >> deployment.yaml
                    """
                    
                    // Apply the deployment
                    bat "kubectl apply -f deployment.yaml"
                    
                    // Apply Service
                    bat "kubectl apply -f kubernetes/service.yaml"
                    
                    // Wait for deployment with timeout and better error handling
                    timeout(time: 5, unit: 'MINUTES') {
                        bat """
                            kubectl rollout status deployment/schedule-tracker
                            if errorlevel 1 (
                                echo Deployment failed. Checking pod status...
                                kubectl get pods
                                kubectl describe deployment schedule-tracker
                                kubectl describe pods
                                exit /b 1
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
                bat "kubectl describe pods"
            }
        }
    }
} 