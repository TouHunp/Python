pipeline {
    agent  { docker { image 'python:3.10.7-alpine' } }
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