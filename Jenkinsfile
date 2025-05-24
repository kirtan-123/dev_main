pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "schedule-tracker"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "default"
        KUBECONFIG = "kubeconfig"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        // Skipping Setup Minikube stage as Minikube will be started manually
        // stage('Setup Minikube') {
        //     steps {
        //         script {
        //             // Check if Minikube is running
        //             def minikubeStatus = bat(script: "minikube status", returnStdout: true).trim()
                    
        //             if (!minikubeStatus.contains("Running")) {
        //                 echo "Starting Minikube..."
        //                 bat "minikube start --driver=docker"
        //             } else {
        //                 echo "Minikube is already running"
        //             }
                    
        //             // Point shell to minikube's docker-daemon
        //             bat "minikube docker-env --shell cmd > minikube-env.bat"
        //             bat "call minikube-env.bat"
        //         }
        //     }
        // }
        
        stage('Build and Load Docker Image') {
            steps {
                dir('c:/Users/Kirtan/Desktop/dev_main') {
                    script {
                        // Set Docker environment to Minikube's Docker daemon
                        bat "minikube docker-env --shell cmd > minikube-env.bat"
                        bat "call minikube-env.bat"
                        
                        // Build the image inside Minikube's Docker daemon
                        bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                        
                        // Verify the image exists
                        bat "docker images | findstr ${DOCKER_IMAGE}"
                    }
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                dir('c:/Users/Kirtan/Desktop/dev_main') {
                    script {
                        // Skip kubectl commands, assume manual deployment
                        echo "Skipping kubectl deployment commands as Kubernetes is managed manually."
                        
                        // Print final web page URL directly with static NodePort
                        echo "Access the application at: http://127.0.0.1:30000"
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