pipeline {
  agent any
  stages {
    stage('Test Redis') {
      steps {
        sh '''pyenv activate python2
molecule test
'''
      }
    }
  }
}