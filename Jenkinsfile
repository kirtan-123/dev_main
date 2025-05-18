pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'  // Adjust this to match your Python version
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Create and activate virtual environment
                    sh '''
                        python -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        pip install pytest
                        python -m pytest tests/ || true
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Start the Flask application in the background
                    sh '''
                        . venv/bin/activate
                        nohup python app.py > app.log 2>&1 &
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            // Clean up
            sh 'pkill -f "python app.py" || true'
        }
    }
} 