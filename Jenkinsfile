node {
    hasFailed = false
    sh 'sudo /var/lib/jenkins/jenkins-chown'
    deleteDir() // wipe out the workspace

    properties([
      parameters([
        [$class: 'StringParameterDefinition',  name: 'DOCS_BRANCH', defaultValue: BRANCH_NAME],
        [$class: 'StringParameterDefinition',  name: 'PUBLISH_VERSION', defaultValue: ''],
        [$class: 'StringParameterDefinition',  name: 'PUBLISH_TITLE', defaultValue: ''],
        [$class: 'BooleanParameterDefinition', name: 'PUBLISH', defaultValue: Boolean.valueOf(false)],
        [$class: 'BooleanParameterDefinition', name: 'SLACK_MESSAGE', defaultValue: Boolean.valueOf(false)]
      ])
    ])

    //String Vars
    hasFailed = false
    String git_creds            = "1335b248-336a-47a9-b0f6-9f7314d6f1f4"
    String doc_gen_git          = "git@github.com:OasisLMF/GenerateDocs.git"
    String doc_gen_branch       = params.DOCS_BRANCH
    String doc_publish_git      = "git@github.com:OasisLMF/OasisLMF.github.io.git"
    String doc_publish_branch   = "master"
    String dir_docs             = "oasis_doc_build"
    String dir_ghpages          = "oasis_doc_publish"

    //Env vars
    env.TAG_RELEASE = params.PUBLISH_VERSION

    try {
        stage('Clone: AutoDoc Generator') {
            sshagent (credentials: [git_creds]) {
                dir(dir_docs) {
                    sh "git clone -b ${doc_gen_branch} ${doc_gen_git} ."
                }
            }
        }
        stage('Run: AutoDoc Generator') {
            sshagent (credentials: [git_creds]) {
                withCredentials([string(credentialsId: 'github-tkn-read', variable: 'gh_token')]) {
                    dir(dir_docs) {
                        sh 'docker build -f docker/Dockerfile.oasis_docbuilder -t oasis_doc_builder .'
                        sh 'docker run -v $(pwd):/tmp/output oasis_doc_builder:latest ' + gh_token
                    }
                }
            }
        }
        if(params.PUBLISH){
            stage('Clone: GitHub Pages') {
                sshagent (credentials: [git_creds]) {
                    dir(dir_ghpages) {
                        sh "git clone -b ${doc_publish_branch} ${doc_publish_git} ."
                    }
                }
            }
            stage('Publish: GitHub Pages') {
                //Extract docs
                dir(dir_docs) {
                    sh "tar -zxvf oasis_docs.tar.gz -C ../${dir_ghpages}"
                }
                //Update gh-pages
                dir(dir_ghpages) {
                    sshagent (credentials: [git_creds]) {
                        sh "git add *"
                        sh "git status"
                        sh "git commit -m 'Update documenation - v${env.TAG_RELEASE}'"
                        sh "git push"
                        //sh "git tag ${env.TAG_RELEASE}"
                        //sh "git push origin ${env.TAG_RELEASE}"
                    }
                }
            }
        }
        if (params.SLACK_MESSAGE) {
            stage('Publish: Send release message') {
                //If publish send slack notification
                dir(dir_docs) {
                    withCredentials([string(credentialsId: 'slack-oasis-core', variable: 'slack_webhook')]) {
                        sh 'python3 post_slack.py ' + "'${params.PUBLISH_TITLE}' " + slack_webhook
                    }
                    withCredentials([string(credentialsId: 'slack-oasis-members', variable: 'slack_webhook')]) {
                        sh 'python3 post_slack.py ' + "'${params.PUBLISH_TITLE}' " + slack_webhook
                    }
                }
            }
        }    
    } catch(hudson.AbortException | org.jenkinsci.plugins.workflow.steps.FlowInterruptedException buildException) {
        hasFailed = true
        error('Build Failed')
    } finally {
        if(params.SLACK_MESSAGE && (params.PUBLISH || hasFailed)){
            def slackColor = hasFailed ? '#FF0000' : '#27AE60'
            SLACK_MSG = "*${env.JOB_NAME}* - (<${env.BUILD_URL}|${env.RELEASE_TAG}>): " + (hasFailed ? 'FAILED' : 'PASSED')
            SLACK_MSG += "\nMode: " + (params.PUBLISH ? 'Publish' : 'Build Test')
            SLACK_CHAN = (params.PUBLISH ? "#builds-release":"#builds-dev")
            slackSend(channel: SLACK_CHAN, message: SLACK_MSG, color: slackColor)
        }
    }
}
