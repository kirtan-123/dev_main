pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "schedule-tracker"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "default"
        KUBECONFIG = "C:/Users/Kirtan/.kube/config"
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
                        try {
                            // First ensure Minikube is running
                            def minikubeStatus = bat(script: "minikube status", returnStdout: true).trim()
                            if (!minikubeStatus.contains("Running")) {
                                echo "Starting Minikube..."
                                timeout(time: 2, unit: 'MINUTES') {
                                    bat "minikube start --force"
                                }
                                sleep(30)
                            }
                            
                            // Set Docker environment to Minikube's Docker daemon with timeout
                            timeout(time: 1, unit: 'MINUTES') {
                                bat "minikube docker-env --shell cmd > minikube-env.bat"
                                bat "type minikube-env.bat"
                                bat "call minikube-env.bat"
                            }
                            
                            // Build the image inside Minikube's Docker daemon
                            bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                            
                            // Verify the image exists
                            bat "docker images | findstr ${DOCKER_IMAGE}"
                        } catch (Exception e) {
                            echo "Error during Docker setup: ${e.message}"
                            // Cleanup
                            bat "minikube delete --force"
                            error "Failed to setup Docker environment"
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Minikube') {
            steps {
                dir('c:/Users/Kirtan/Desktop/dev_main') {
                    script {
                        // Check if Minikube is running and start it if not
                        def minikubeStatus = bat(script: "minikube status", returnStdout: true).trim()
                        if (!minikubeStatus.contains("Running")) {
                            echo "Starting Minikube..."
                            try {
                                // Set a timeout for minikube start
                                timeout(time: 2, unit: 'MINUTES') {
                                    bat "minikube start --force"
                                }
                                
                                // Verify Minikube is actually running
                                def verifyStatus = bat(script: "minikube status", returnStdout: true).trim()
                                if (!verifyStatus.contains("Running")) {
                                    error "Minikube failed to start properly"
                                }
                                
                                // Wait for Minikube to be fully ready
                                sleep(30)
                            } catch (Exception e) {
                                echo "Error starting Minikube: ${e.message}"
                                // Try to clean up
                                bat "minikube delete --force"
                                error "Failed to start Minikube after cleanup"
                            }
                        }
                        
                        // Run minikube service command and print the URL
                        def serviceUrl = bat(script: "minikube service schedule-tracker-service --url", returnStdout: true).trim()
                        echo "Minikube service URL: ${serviceUrl}"
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