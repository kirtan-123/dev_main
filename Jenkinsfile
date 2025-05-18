pipeline {
    agent any
    
    tools {
        python 'Python3'
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
                    python --version
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