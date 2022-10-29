node {
 stage('build') {
      cmd_exec('echo "Buils starting..."')
      cmd_exec('echo "dir /a /b"')
        }
   stage('Version'){
        steps{
        sh 'python --version'
            }
        }

}
def cmd_exec(command) {
    return bat(returnStdout: true, script: "${command}").trim()
}