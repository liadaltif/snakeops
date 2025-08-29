pipeline {
  agent any

  environment {
    PYTHON = 'python3'
    VENV_DIR = '.venv'
  }

  // your webhook will trigger; keep this for GitHub integration
  triggers { githubPush() }

  stages {
    stage('Checkout') {
      steps {
        // uses the repo this job is tied to
        checkout scm
        sh 'git rev-parse --short HEAD'
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
          if [ -n "$files" ]; then
            echo "[compile] byte-compiling python files..."
            python -m py_compile $files
          else
            echo "no python files found."
          fi
        '''
      }
    }

    stage('Unit tests') {
      steps {
        sh '''
          set -e
          . ${VENV_DIR}/bin/activate
          mkdir -p reports
          pytest -q --junitxml=reports/junit.xml
        '''
      }
    }
  }

  post {
    always {
      // publish test report to Jenkins UI
      junit allowEmptyResults: true, testResults: 'reports/**/*.xml'
      archiveArtifacts artifacts: 'reports/**/*.xml', allowEmptyArchive: true
    }
  }
}
