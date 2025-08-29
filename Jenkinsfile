pipeline {
  agent any

  options { ansiColor('xterm'); timestamps() }

  environment {
    PYTHON = 'python3'
    VENV_DIR = '.venv'
  }

  // Webhook triggers the job (keep the checkbox in the job too)
  triggers { githubPush() }

  stages {
    stage('Checkout') {
      steps {
        // If your job is "Pipeline script from SCM", prefer checkout scm:
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
          # Optional: if you later add requirements.txt, they’ll be installed:
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
          # If pytest is present, use it (nicer JUnit); otherwise unittest
          if python -c "import pkgutil; import sys; sys.exit(0 if pkgutil.find_loader('pytest') else 1)"; then
            pytest -q --junitxml=reports/junit.xml || true
          else
            python -m unittest discover -v || true
            # Produce a minimal JUnit if you want; for now we rely on console logs
          fi
        '''
      }
    }
  }

  post {
    always {
      // If pytest ran, publish JUnit; if not present, this step quietly skips
      junit allowEmptyResults: true, testResults: 'reports/**/*.xml'
      archiveArtifacts artifacts: 'reports/**/*.xml', allowEmptyArchive: true
    }
  }
}
