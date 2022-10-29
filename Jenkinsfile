pipeline {
    agent any
    stages{  
   stage('Version'){
        steps{
        bat 'python --version'
            }
        }
   stage('AI'){
        steps{
        bat 'python AI-youtube.py'
            }
        }
    }
}