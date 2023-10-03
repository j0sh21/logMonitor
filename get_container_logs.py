import os
import subprocess

# Directory to store log files
log_directory = "/home/Umbrel/logs/docker"

# Create the directory if it doesn't exist
os.makedirs(log_directory, exist_ok=True)

# List container IDs
container_ids = subprocess.check_output(["sudo", "docker", "ps", "-q"], universal_newlines=True).splitlines()

# Iterate through container IDs and save logs in separate files
for container_id in container_ids:
    log_file = os.path.join(log_directory, f"docker_log_{container_id}.log")
    with open(log_file, "w") as f:
        subprocess.call(["sudo", "docker", "logs", "--until=05m", "--tail", "300", container_id], stdout=f)

print(f"Logs have been saved in {log_directory}.")
