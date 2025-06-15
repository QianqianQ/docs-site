---
title: Jenkins
description: Jenkins.
---
Self-contained, open source automation server which can be used to automate all sorts of tasks related to building, testing, and delivering or deploying software.

## Installation
```bash
# Docker
# https://www.jenkins.io/doc/book/installing/docker/
docker build -t myjenkins-blueocean:2.387.2-1 .

docker run \
  --name jenkins-blueocean \
  --restart=on-failure \
  --detach \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  --volume /path/to/local/data:/container/data \
  myjenkins-blueocean:2.387.2-1

sudo kill `sudo lsof -t -i:50000`

docker container stop jenkins-blueocean | xargs docker rm
```

## Troubleshooting

### HTML rendering issue
**Solution** Configuring Content Security Policy
```groovy
// Sets the CSP property to an empty string, allowing unrestricted HTML content
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")
```

## Jenkinsfile

### Archive artifacts and publish results
```groovy
/*
This Jenkins pipeline defines a CI/CD workflow with three main stages:
1. Test - Cleans workspace, sets up Python environment, and runs test script
2. Generate summary - Generates test summary report using Python script
3. Archive artifacts and publish results - Archives various file types and publishes test results

The pipeline:
- Runs on any available agent
- Keeps build records for 180 days
- Archives multiple file types including logs, reports, and test artifacts
- Publishes test results using ACI plugin
*/

pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        cleanWs()
        sh '''#!/usr/bin/env bash
            set +x
            echo
            echo

            cd "${WORKSPACE}"

            export PYTHONPATH="${PYTHONPATH}:/path/"
            source /home/user/venv/bin/activate

            archive_path="${JENKINS_HOME}/jobs/${JOB_NAME}/builds/archive/"
            python3 /path/to/test.py "${arg}"
        '''
      }
    }

    stage('Generate summary') {
      steps {
        sh '''#!/usr/bin/env bash
            set +x
            echo
            echo

            cd "${WORKSPACE}"

            export PYTHONPATH="${PYTHONPATH}:/path/"
            source /home/user/venv/bin/activate
            python3 /path/to/summary.py
            '''
      }
    }

    stage('Archive artifacts and publish results') {
        steps {
            echo 'Archive artifacts and publish results'
        }
        post {
            always {
                step($class: 'ArtifactArchiver', artifacts: '*.txt, *.json, *.tar, *.yaml, *.gz,*.csv,*.html, *.log, *.xml', followSymlinks: false)
                step([$class: 'ACIPluginPublisher', name: 'testcase*.xml', shownOnProjectPage: false])
            }
    }
    }
  }
  options {
    buildDiscarder(logRotator(daysToKeepStr: '180'))
  }
}
```

### Python project
```groovy
/**
 * Sample Jenkins pipeline for Python project:
 * - Uses Python 3.12.4 Alpine container
 * - Standard build/test/deploy stages
 * - Includes staging approval
 * - Handles artifacts and build states
 */

pipeline {
    agent { docker { image 'python:3.12.4-alpine3.20' } }
    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE = 'sqlite'
    }
    options {
        // Timeout counter starts AFTER agent is allocated
        // timeout(time: 30, unit: 'SECONDS')
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            steps {
                echo 'Build'
            }
        }
        stage('Test') {
            // agent any  // stage agent
            options {
                // Timeout counter starts BEFORE agent is allocated
                timeout(time: 10, unit: 'SECONDS')  // stage
            }
            steps {
                sh 'echo "Database engine is ${DB_ENGINE}"'
                // sh 'printenv'
                retry(3) {
                    sh 'python -V'
                }
                // timeout(time: 3, unit: 'MINUTES') {
                //     sh 'python --version'
                // }
                timeout(time: 3, unit: "MINUTES") {
                    retry(3) {
                        sh 'python -V'
                    }
                }
            }
        }
        // Stages as Deployment Environments
        stage('Deploy - Staging') {
            steps {
                // sh './deploy staging'
                // sh './run-smoke-tests'
                echo 'Deploy - Staging...'
            }
        }
        stage('Sanity check') {
            steps {
                input "Does the staging env ok?"
            }
        }
        stage('Deploy - Production') {
            steps {
                echo 'Deploy...'
                // sh './deploy production'
                unstable(message: 'Deploy unstable')
            }
        }
        stage('Validate') {
            steps {
                echo 'Validate'
            }
        }
    }
    post {
        always {
            // junit 'build/report/**/*.xml'
            // archiveArtifacts 'build/libs/**/*.jar'
            archiveArtifacts artifacts: 'build/lib/**/.jar', fingerprint: true
            echo "Finished"
        }
        success {
            echo 'succeeded!'
        }
        unstable {
            echo 'unstable'
        }
        failure {
            // mail to: 'test@test.com'
            //      subject: "Faillure"
            //      body: "Sth wrong with ${env.BUILD_URL}"
            echo 'failed'
        }
        changed {
            echo 'Things were different before...'
        }
    }
}
```