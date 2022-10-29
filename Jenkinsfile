pipeline {
    agent any
    stages{  
   stage('Version'){
        steps{
        sh 'python --version'
            }
        }
   stage('AI'){
        steps{
        sh 'python AI-youtube.py'
            }
        }
    }
}