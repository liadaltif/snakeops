pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Pulls your code from GitHub using the webhook trigger
                git branch: 'main',
                    url: 'https://github.com/liadaltif/snakeops'
                    credentialsId: '3900872b-e16f-4113-a3e5-079c02317289'
            }
        }
        stage('Build') {
            steps {
                echo "🚀 Hello from Jenkins + GitHub!"
                sh 'ls -la'  // lists files from your repo
            }
        }
    }
}

