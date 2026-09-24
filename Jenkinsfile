pipeline {
    agent any

    environment {
        // Ensure the local virtual environment path is recognized
        VENV_PATH = "${WORKSPACE}/.venv"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls the latest code from your GitHub repository
                checkout scm
            }
        }

        stage('Setup Environment & Dependencies') {
            steps {
                sh '''
                    # 1. Create virtual environment if it doesn't exist
                    if [ ! -d "$VENV_PATH" ]; then
                        python3 -m venv .venv
                    fi
                    
                    # 2. Activate venv and install dependencies
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                sh '''
                    . .venv/bin/activate
                    
                    # Install browser system dependencies (requires sudo/root on the Jenkins server)
                    playwright install-deps
                    
                    # Install the actual browsers (Chromium, Firefox, WebKit)
                    playwright install
                '''
            }
        }

        stage('Execute Playwright Tests') {
            steps {
                // The 'catchError' block ensures the pipeline continues to execution reports even if tests fail
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh '''
                        . .venv/bin/activate
                        
                        # Run tests across all browsers sequentially or using your matrix logic
                        pytest --browser chromium --browser firefox --browser webkit -p no:asyncio --html=reports/report.html --self-contained-html
                    '''
                }
            }
        }
    }

    post {
        always {
            // Publish the pytest HTML report to the Jenkins build UI
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Playwright Test Report',
                reportTitles: 'Opencart Playwright Automation Results'
            ])
            
            // Clean up the workspace to keep the Jenkins server clean
            cleanWs()
        }
    }
}
