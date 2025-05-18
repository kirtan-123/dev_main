pipeline {
    agent any
    
    environment {
        PATH = "C:\\Users\\Kirtan\\AppData\\Local\\Programs\\Python\\Python312;C:\\Users\\Kirtan\\AppData\\Local\\Programs\\Python\\Python312\\Scripts;${env.PATH}"
        FLASK_PORT = "5000"
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
                    echo "The application will be available at: http://localhost:5000"
                    start /B cmd /c "python app.py --host=0.0.0.0 --port=%FLASK_PORT% > flask_app.log 2>&1"
                    timeout /t 5 /nobreak
                    echo "Flask application should now be running - check flask_app.log for details"
                    type flask_app.log
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Flask application deployed successfully! Access it at: http://localhost:5000'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
} 