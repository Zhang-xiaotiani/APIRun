// export LANG="en_US.UTF-8"

pipeline {
    agent any

    environment {
        WORKSPACE_BASE = "/workspace"
        REPO_DIR = "${env.WORKSPACE_BASE}/repo"
        REPORT_DIR = "${env.WORKSPACE_BASE}/report"
        LOG_DIR = "${env.WORKSPACE_BASE}/logs"
        TEMP_DIR = "${env.WORKSPACE_BASE}/temp"
        GIT_URL = 'https://github.com/Zhang-xiaotiani/APIRun.git'
        // 获取当前时间戳（格式：202508012239）
        TIMESTAMP = """${new Date().format('yyyyMMddHHmm')}"""
    }

    stages {

        stage('初始化目录') {
            steps {
                script {
                    sh "mkdir -p ${REPO_DIR} ${REPORT_DIR} ${LOG_DIR} ${TEMP_DIR}"
                    sh "echo 初始化目录结构完成"
                }
            }
        }

        stage('拉取代码') {
            steps {
                dir("${REPO_DIR}") {
                    git branch: 'main', url: "${GIT_URL}"
                }
            }
        }

        stage('安装依赖') {
            steps {
                dir("${REPO_DIR}") {
                    sh "pip install -r requirements.txt"
                    sh "pip install pytest-html"
                }
            }
        }

        stage('运行测试并生成报告') {
            steps {
                script {
                    def reportFile = "test_${TIMESTAMP}.html"
                    sh """
                        cd ${REPO_DIR}
                        pytest --html=${REPORT_DIR}/${reportFile} --self-contained-html \
                               | tee ${LOG_DIR}/test_${TIMESTAMP}.log
                    """
                    // 设置报告路径供后续使用
                    env.REPORT_FILE_NAME = reportFile
                }
            }
        }

        stage('归档与发布报告') {
            steps {
                archiveArtifacts artifacts: "${REPORT_DIR}/${env.REPORT_FILE_NAME}", fingerprint: true
                publishHTML([
                    reportDir: "${REPORT_DIR}",
                    reportFiles: "${env.REPORT_FILE_NAME}",
                    reportName: "测试报告-${env.TIMESTAMP}",
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: false
                ])
            }
        }
    }

    post {
        always {
            echo "流水线完成，报告名称为 test_${env.TIMESTAMP}.html"
            sh "ls -lh ${REPORT_DIR}"
            sh "ls -lh ${LOG_DIR}"
        }
    }
}
