@Library('jenkins-pipeline-scripts') _

pipeline {
    agent none
    options {
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
      stage('Build') {
        agent any
        when {
          allOf{
            branch "main"
            not {
              changelog '.*\\[(ci)?\\-?\\s?skip\\-?\\s?(ci)?\\].*'
            }
          }
        }
        steps {
          parallel(
            buster: {
              sh 'make build-buster'
            }
            buster-odoo9: {
              echo 'make build-buster-odoo9'
            }
            bullseye: {
              echo 'make build-bullseye'
            }
            bullseye-odoo9: {
              echo 'make build-bullseye-odoo9'
            }
          )
        }
      }
      stage('Push image to staging registry') {
        agent any
        when {
          allOf{
            branch "main"
            not {
              changelog '.*\\[(ci)?\\-?\\s?skip\\-?\\s?(ci)?\\].*'
            }
          }
        }
        steps {
          parallel(
            buster: {
              pushImageToRegistry (
                "${env.BUILD_ID}",
                "teleservices/buster"
              )
            }
            buster-odoo9: {
              echo 'push teleservices/buster-odoo9'
            }
            bullseye: {
              echo 'push teleservices/bullseye'
            }
            bullseye-odoo9: {
              echo 'push teleservices/bullseye-odoo9'
            }
          )
        }
      }
      stage('Deploy to staging') {
        agent any
        when {
          allOf {
            branch "main"
            expression {
              currentBuild.result == null || currentBuild.result == 'SUCCESS'
            }
            not {
              changelog '.*\\[(ci)?\\-?\\s?skip\\-?\\s?(ci)?\\].*'
            }
          }
        }
        steps {
          echo "curl -k --fail --show-error --header \"X-Rundeck-Auth-Token:$RUNDECK_TOKEN\" -d \"argString=-name staging2\" -d \"filter=name ts-staging1\" https://run.imio.be/api/12/job/94b605f2-ad32-4f9f-977e-37342f6b7d32/run/ "
        }
      }
      stage('Deploy') {
        options {
           timeout(time: 60, unit: 'SECONDS')
        }
        input {
          message "Deploy to production?"
          ok "Yes"
        }
        steps {
          echo 'Confirmed production deploy'
          moveImageToProdRegistry(env.TAG_NAME, "teleservices/buster")
          //moveImageToProdRegistry(env.TAG_NAME, "teleservices/buster-odoo9")
          //moveImageToProdRegistry(env.TAG_NAME, "teleservices/bullseye")
          //moveImageToProdRegistry(env.TAG_NAME, "teleservices/bullseye-odoo9")
          echo "Schedule Rundeck job"
          sh "curl -k --fail -XPOST --header \"Content-Type: application/json\" --header \"X-Rundeck-Auth-Token: $RUNDECK_TOKEN\" https://run.imio.be/api/12/job/311af116-fedc-4e33-b2a7-99c8651f8e9b/run"
          emailext to: "support-ts+jenkins@imio.be",
            recipientProviders: [developers(), requestor()],
            subject: "New release will be deploy: ${currentBuild.displayName}",
            body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} released ${env.fullDisplayName} <br />"
          echo 'Upgrade finished.'
        }
      }
    }
    post {
      fixed{
        emailext to: "support-ts+jenkins@imio.be",
          recipientProviders: [developers(), requestor()],
          subject: "Fixed Pipeline: ${currentBuild.fullDisplayName}",
          body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} is back to normal (${env.BUILD_URL})"
      }
      failure{
        emailext to: "support-ts+jenkins@imio.be",
          recipientProviders: [developers(), requestor()],
          subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
          body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} failed (${env.BUILD_URL})"
      }
      always {
        node(null)  {
          sh "make clean"
        }
      }
    }
}