@Library('jenkins-pipeline-scripts')

String supportTeleservicesEmail = 'support-ts+jenkins@imio.be'
String skipCiRegex = '.*\\[(ci)?\\-?\\s?skip\\-?\\s?(ci)?\\].*'
String mainBranch = 'main'
String bullseye = 'bullseye'
String bullseyeTest = 'bullseye-test'
String teleservicesBullseye = 'teleservices/bullseye'

pipeline {
    agent none
    parameters {
        booleanParam(
            name: 'USE_CACHE_TO_BUILD_IMAGE',
            defaultValue: true,
            description: "Docker build will not be using cache if you choose 'false' value."
        )
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '50'))
    }
    stages {
      stage('Build prod image') {
        //agent any
        when {
          allOf {
            branch mainBranch
            not(changelog skipCiRegex)
          }
        }
        parallel {
          stage(bullseye) {
            agent any
            steps {
              script {
                if (params.USE_CACHE_TO_BUILD_IMAGE) {
                  sh 'make build-bullseye-test'
                } else {
                  sh 'make build-no-cache-bullseye-test'
                }
              }
            }
            script {
              if (params.USE_CACHE_TO_BUILD_IMAGE) {
                sh 'make build-bullseye'
              }
                      else {
                sh 'make build-no-cache-bullseye'
                      }
            }
          }
        }
      }
    }
    stage('Build test image') {
      parallel {
        stage(bullseyeTest) {
      agent any
      steps {
        script {
          if (params.USE_CACHE_TO_BUILD_IMAGE) {
            sh 'make build-bullseye-test'
                } else {
            sh 'make build-no-cache-bullseye-test'
          }
        }
      }
        }
      }
    }
        stage('Push base prod image to staging registry') {
          //agent any
          when {
            allOf {
              branch mainBranch
              not {
                changelog skipCiRegex
              }
            }
          }
          parallel {
            stage(bullseye) {
              agent any
              steps {
                pushImageToRegistry(
                "${env.BUILD_ID}",
                teleservicesBullseye
              )
              }
            }
          }
        }
        stage('Push other images to staging registry') {
          //agent any
          when {
            allOf {
              branch mainBranch
              not {
                changelog skipCiRegex
              }
            }
          }
          parallel {
            stage(bullseyeTest) {
              agent any
              steps {
                pushImageToRegistry(
                "${env.BUILD_ID}",
                'teleservices/bullseye-test'
                )
              }
            }
          }
        }
        stage('Deploy to staging') {
          agent any
          when {
            allOf {
              branch mainBranch
              expression {
                currentBuild.result == null || currentBuild.result == 'SUCCESS'
              }
              not {
                changelog skipCiRegex
              }
            }
          }
          steps {
            sh "curl -k --fail --show-error --header \"X-Rundeck-Auth-Token:$RUNDECK_TS_TOKEN\" " +
              '-d \"argString=-name staging\" -d \"filter=name ts001.staging.imio.be\" ' +
              'https://run.imio.be/api/12/job/94b605f2-ad32-4f9f-977e-37342f6b7d32/run/ '
          }
        }
        // stage('Test staging') {
        //   agent any
        //   when {
        //     allOf {
        //       branch "main"
        //       expression {
        //         currentBuild.result == null || currentBuild.result == 'SUCCESS'
        //       }
        //       not {
        //         changelog skipCiRegex
        //       }
        //     }
        //   }
        //   steps {
        //     script {
        //       try {
        //         timeout(time: 15, unit: 'MINUTES', activity: true) {
        //           sh {
        //             """
        //             sleep 3
        //             until curl -m 1 --output /dev/null --silent --fail 'https://staging.guichet-citoyen.be/';
        //             do
        //                 sleep 3
        //                 echo 'Waiting until guichet-citoyen staging instance started'
        //             done
        //             echo 'The instance is now started.'
        //             """
        //           }
        //         }
        //       }
        //       catch (exc) {
        //         unstable('Staging instance is down.')
        //       }
        //     }
        //     script {
        //       try {
        //         sh 'make validation-tests'
        //       }
        //       catch (exc) {
        //         unstable('Validation tests failed!')
        //       }
        //     }
        //   }
        // }
        stage('Deploy') {
          agent any
          options {
            timeout(time: 48, unit: 'HOURS')
          }
          input {
            message 'Deploy to production?'
            ok 'Yes'
          }
          steps {
            echo 'Confirmed production deploy'
            moveImageToProdRegistry(env.TAG_NAME, teleservicesBullseye)
            echo 'Schedule Rundeck job'
            sh 'curl -k --fail -XPOST --header \"Content-Type: application/json\" ' +
              "--header \"X-Rundeck-Auth-Token: $RUNDECK_TS_TOKEN\" " +
              'https://run.imio.be/api/12/job/311af116-fedc-4e33-b2a7-99c8651f8e9b/run'
            emailext to: supportTeleservicesEmail,
            recipientProviders: [developers(), requestor()],
            subject: "New release will be deploy: ${currentBuild.displayName}",
            body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} released ${env.fullDisplayName} <br />"
            echo 'Upgrade finished.'
          }
        }
    }
    post {
      fixed {
        emailext to: supportTeleservicesEmail,
          recipientProviders: [developers(), requestor()],
          subject: "Fixed Pipeline: ${currentBuild.fullDisplayName}",
          body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} is back to normal (${env.BUILD_URL})"
      }
      failure {
        emailext to: supportTeleservicesEmail,
        recipientProviders: [developers(), requestor()],
        subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
        body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} failed (${env.BUILD_URL})"
      }
      success {
        node(null) {
          cleanWs()
        }
      }
    }
}
