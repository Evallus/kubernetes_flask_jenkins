pipeline {
    options { buildDiscarder(logRotator(numToKeepStr:'5'))}
    environment {
        DOCKER_IMAGE_NAME = "evalus/tasksapp-python"
        DOCKER_IMAGE = ""
    }
    agent any
    parameters {
        booleanParam(name: 'executeTests', defaultValue: true, description: '')
    }
    stages {
        stage('Checkout Source') {
            steps {
                script {
                   echo 'Initiating application...'
                }
                checkout scm
            }
        }
        stage("Build") {
            steps {
                script {
                   echo 'Building image...'
                   DOCKER_IMAGE = docker.build(DOCKER_IMAGE_NAME)
                }
            }
        }
        stage("Push") { //IF app.py changed
            environment {
                registryCredential = 'dockerhublogin'
            }
            steps {
                script {
                    echo 'Pushing image...'
                    docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
                        dockerImage.push("latest")
                    }
                }
            }
        }
        stage("Test") {
            when {
                expression {
                    params.executeTests
                }
            }
            steps {
                script {
                   echo 'Testing application...'
                }
            }
        }
        stage("Deploy") { //IF MANIFESTS CHANGED OR IS NOT CURRENTLY RUNNING
//             when {
//                 expression {
//                     BRANCH_NAME == 'main' //AND TESTED AND PASSED_TEST
//                 }
//             }
            steps {
                script {
                   echo 'Deploying application...'
                   kubernetesDeploy(configs: "tasksapp.yaml", kubeconfigId: "kubernetes")
                }
            }
        }
    }
}