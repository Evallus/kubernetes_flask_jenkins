pipeline {
    agent any
    environment {
        NEW_VERSION = '1.3.0'
    }
    parameters {
        choice(name: 'VERSION', choices: ['1.1.0', '1.2.0', '1.3.0'], description: '')
        booleanParam(name: 'executeTests', defaultValue: true, description: '')
    }
    stages {
        stage("init") {
            steps {
                script {
                   echo 'initiating application...'
                   echo "initiating version ${NEW_VERSION}"
                }
            }
        }
        stage("build") {
            steps {
                script {
                   echo 'building application...'
                }
            }
        }
        stage("test") {
            when {
                expression {
                    params.executeTests
                }
            }
            steps {
                script {
                   echo 'testing application...'
                }
            }
        }
        stage("deploy") {
            when {
                expression {
                    BRANCH_NAME == 'main'
                }
            }
            steps {
                script {
                   echo 'deploying application...'
                }
            }
        }
    }
}