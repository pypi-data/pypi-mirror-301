import os
import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode('utf-8'))
        sys.exit(1)
    return output.decode('utf-8')

def confirm_version_change():
    response = input("Have you updated the version in setup.py? (yes/no): ").lower()
    if response != 'yes':
        print("Please update the version in setup.py before uploading.")
        sys.exit(1)

def main():
    # Confirm version change
    confirm_version_change()

    # Remove old distribution files
    run_command("rm -rf dist build *.egg-info")

    # Build the package
    run_command("python setup.py sdist bdist_wheel")

    # Upload to PyPI
    run_command("twine upload dist/*")

    print("Package successfully uploaded to PyPI!")

if __name__ == "__main__":
    main()
