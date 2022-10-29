pipeline {
    agent any
    stages{  
   stage('Version'){
        steps{
        sh 'python3 --version'
            }
        }
   stage('AI'){
        steps{
        sh 'python3 AI-youtube.py'
            }
        }
    }
}