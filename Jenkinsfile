pipeline {
  agent any
  stages {
    stage('Test Redis') {
      steps {
        sh '''molecule test
'''
      }
    }
  }
}