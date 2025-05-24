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
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image locally for Minikube
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    // Load image into Minikube
                    sh "minikube image load ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                script {
                    // Apply PersistentVolume
                    sh "kubectl apply -f kubernetes/persistent-volume.yaml"
                    
                    // Apply PersistentVolumeClaim
                    sh "kubectl apply -f kubernetes/persistent-volume.yaml"
                    
                    // Apply Deployment
                    sh "kubectl apply -f kubernetes/deployment.yaml"
                    
                    // Apply Service
                    sh "kubectl apply -f kubernetes/service.yaml"
                    
                    // Wait for deployment to be ready
                    sh "kubectl rollout status deployment/schedule-tracker"
                }
            }
        }
    }
    
    post {
        success {
            script {
                def minikubeIP = sh(script: "minikube ip", returnStdout: true).trim()
                echo "Application deployed successfully to Minikube!"
                echo "Access the application at: http://${minikubeIP}:30000"
            }
        }
        failure {
            echo 'Deployment failed!'
        }
    }
} 