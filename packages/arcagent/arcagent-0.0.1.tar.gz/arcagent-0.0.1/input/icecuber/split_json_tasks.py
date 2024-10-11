""" Reformat ARC Prize 2024 files to work with ARC 2020 file format and rules """
import json
import os

# Load the JSON content
json_file_path = '/kaggle/input/arc-prize-2024/arc-agi_test_challenges.json'
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Create the 'test' directory
output_dir = '/kaggle/working/abstraction-and-reasoning-challenge/test'
os.makedirs(output_dir, exist_ok=True)

# Split the JSON content into individual files
for task_id, task_data in data.items():
    output_file_path = os.path.join(output_dir, f'{task_id}.json')
    with open(output_file_path, 'w') as output_file:
        json.dump(task_data, output_file, indent=4)

if open("../input/arc-solution-source-files-by-icecuber/version.txt").read().strip() == "671838222":
    print("Dataset has correct version")
else:
    print("Dataset version not matching!")
    assert(0)
