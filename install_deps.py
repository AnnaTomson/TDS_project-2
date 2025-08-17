import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    packages = [
        "flask==2.3.3",
        "openai>=1.0.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        "python-dotenv>=1.0.0",
        "python-multipart>=0.0.6",
        "python-dateutil>=2.8.2",
        "requests>=2.31.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            install(package)
            print(f"Successfully installed {package}")
        except Exception as e:
            print(f"Error installing {package}: {str(e)}")
