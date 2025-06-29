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

        stage('Verify Deployment') {
            steps {
                dir('c:/Users/Kirtan/Desktop/dev_main') {
                    script {
                        echo " deployment "

                        // Wait for existing deployment to be ready
                        timeout(time: 2, unit: 'MINUTES') {
                            bat 'set KUBECONFIG=C:\\Users\\Kirtan\\.kube\\config && kubectl rollout status deployment/schedule-tracker'
                        }

                        // Get service URL
                        def serviceUrl = bat(script: "minikube service schedule-tracker-service --url", returnStdout: true).trim()
                        echo "✅ App available at: ${serviceUrl}"
                    }
                }
            }
        }
    }

    post {
    always {
        echo "📦 Post block "
    }

    success {
        script {
            echo "✅ Pipeline succeeded. Getting Minikube IP..."
            def minikubeIP = bat(script: "minikube ip", returnStdout: true).trim()
            echo "Minikube IP: ${minikubeIP}"
        }
    }

    failure {
        echo "❌ Pipeline failed. Gathering Kubernetes debug information..."

        bat 'set KUBECONFIG=C:\\Users\\Kirtan\\.kube\\config && kubectl get pods -o wide'
        bat 'set KUBECONFIG=C:\\Users\\Kirtan\\.kube\\config && kubectl describe deployment schedule-tracker || echo "deployment not found"'
        bat 'set KUBECONFIG=C:\\Users\\Kirtan\\.kube\\config && kubectl describe pods || echo "pods not found"'
    }
}

}
