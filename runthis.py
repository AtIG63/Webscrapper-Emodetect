import subprocess

def run_python_script(file_path):
    try:
        # Run the Python script and ignore its output
        subprocess.run(['python', file_path], check=True)
        print(f"Successfully ran {file_path}")
    except subprocess.CalledProcessError:
        print(f"Error running {file_path}")

# Paths to your Python scripts
file1 = 'D:/PROJECTS/BlackCoffer_Assignment/extract.py'
file2 = 'D:/PROJECTS/BlackCoffer_Assignment/sentiment.py'

# Run the scripts one after another
run_python_script(file1)
run_python_script(file2)
