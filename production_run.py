import subprocess
import sys
import os

def run_production_server():
    try:
        subprocess.run([
            'gunicorn',
            '-c', 'gunicorn_config.py',
            'run:app'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Gunicorn: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")

if __name__ == '__main__':
    run_production_server()