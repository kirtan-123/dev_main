pipeline {
    agent any
    
    environment {
        PATH = "C:\\Users\\Kirtan\\AppData\\Local\\Programs\\Python\\Python312;C:\\Users\\Kirtan\\AppData\\Local\\Programs\\Python\\Python312\\Scripts;${env.PATH}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat '''
                    echo "Verifying Python installation..."
                    python --version
                    echo "Installing dependencies..."
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Deploy Flask App') {
            steps {
                bat '''
                    echo "Starting Flask Application..."
                    start /B python app.py
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Flask application deployed successfully!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
} 