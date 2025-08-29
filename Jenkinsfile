pipeline {
  agent any

  options { ansiColor('xterm'); timestamps() }

  environment {
    PYTHON = 'python3'
    VENV_DIR = '.venv'
  }

  triggers { githubPush() }   // also tick the checkbox in the job

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/liadaltif/snakeops.git'
            // credentialsId not needed for public repos
      }
    }

    stage('Set up venv') {
      steps {
        sh '''
          set -e
          if [ ! -d "${VENV_DIR}" ]; then ${PYTHON} -m venv ${VENV_DIR}; fi
          . ${VENV_DIR}/bin/activate
          python -m pip install --upgrade pip
          pip install pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        '''
      }
    }

    stage('Compile (syntax check)') {
      steps {
        sh '''
          set -e
          . ${VENV_DIR}/bin/activate
          files=$(git ls-files "*.py" || true)
          if [ -n "$files" ]; then python -m py_compile $files; else echo "no python files"; fi
        '''
      }
    }

    stage('Unit tests') {
      steps {
        sh '''
          set -e
          . ${VENV_DIR}/bin/activate
          mkdir -p reports
          if [ -d tests ] || ls test_*.py >/dev/null 2>&1; then
            pytest -q --junitxml=reports/junit.xml
          else
            echo "no tests found."
          fi
        '''
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/**/*.xml'
      archiveArtifacts artifacts: 'reports/**/*.xml', allowEmptyArchive: true
    }
  }
}
