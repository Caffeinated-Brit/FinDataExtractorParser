import subprocess
import time


LLM_MODEL = 'Qwen/Qwen2.5-Coder-3B-Instruct'

def start_lmdeploy_server():
    try:
        # Construct the command to start the server

        command = [
            'nohup', 'lmdeploy', 'serve', 'api_server', LLM_MODEL,
            '--server-port', '23333',
            '--tp', '2',
            '--cache-max-entry-count', '0.2'
        ]
        # Run the command to start the server
        print("Started LmDeploy server")
        process = subprocess.run(
            command,  # Command to execute
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,  # Will raise an exception if the command fails
            text=True  # Get the output as a string (not bytes)
        )


        # Print the output from the server
        print("LMDeploy server started successfully.")
        print("Output:", process.stdout)

        return process
    except subprocess.CalledProcessError as e:
        print(f"Error starting LMDeploy server: {e.stderr}")
        return None


start_lmdeploy_server()

