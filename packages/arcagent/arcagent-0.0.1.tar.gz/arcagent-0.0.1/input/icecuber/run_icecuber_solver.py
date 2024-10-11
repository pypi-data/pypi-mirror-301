# run_icecuber_solver.py
""" Icecuber's original solution to the ARC 2020 challenge """
from subprocess import Popen, PIPE, STDOUT
from pathlib import Path
import json
import sys

# don't delete previous attempted solutions unless you're attempt a new solution for real
arc_2020_path = Path("/kaggle/working/abstraction-and-reasoning-challenge/test/")
if __name__ == '__main__':
    if len(sys.argv) > 1 and Path(sys.argv[1]).is_dir():
        arc_2020_path = Path(sys.argv[1])
    else:
        print("USAGE: python3 run_icecuber_solver.py /kaggle/path/to/arc-2020-format-files/")
assert arc_2020_path.is_dir()


def mySystem(cmd):
    """ Helper to run subprocess.Popen on a POSIX command line string """
    print(cmd)
    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    for line in iter(process.stdout.readline, b''):
        print(line.decode("utf-8"), end='')
    assert(process.wait() == 0)


dummy_run = False
# Check for dummy submission task ID among tasks and create old_submission.csv header
for fn in Path(arc_2020_path).glob('*.json'):
    if "136b0064" in str(fn):
        print("Making dummy submission")
        f = open("old_submission.csv", "w")
        f.write("output_id,output\n")
        f.close()
        dummy_run = True
for i, p in enumerate(Path(arc_2020_path).glob('*')):
    if i < 5 or i > 95:
        print(i, p)
    elif i == 50:
        print('...')


# This will take at least 2 minutes for each task!
if not dummy_run:
    mySystem("cp -r ../input/arc-solution-source-files-by-icecuber ./absres-c-files")
    mySystem("cd absres-c-files; make -j")
    # usage safe_run.py <start_task_num> <num_tasks>
    mySystem("cd absres-c-files; python3 safe_run.py 0 20")
    mySystem("cp absres-c-files/submission_part.csv old_submission.csv")
    mySystem("tar -czf store.tar.gz absres-c-files/store")
    mySystem("rm -r absres-c-files")


def translate_submission(file_path):
    """ Translate from old submission format (csv) to new one (json) """
    # Read the original submission file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    submission_dict = {}

    for line in lines[1:]:  # Skip the header line
        output_id, output = line.strip().split(',')
        task_id, output_idx = output_id.split('_')
        predictions = output.split(' ')  # Split predictions based on ' '

        # Take only the first two predictions
        if len(predictions) > 2:
            predictions = predictions[:2]

        processed_predictions = []
        for pred in predictions:
            if pred:  # Check if pred is not an empty string
                pred_lines = pred.split('|')[1:-1]  # Remove empty strings from split
                pred_matrix = [list(map(int, line)) for line in pred_lines]
                processed_predictions.append(pred_matrix)

        attempt_1 = processed_predictions[0] if len(processed_predictions) > 0 else []
        attempt_2 = processed_predictions[1] if len(processed_predictions) > 1 else []

        if task_id not in submission_dict:
            submission_dict[task_id] = []

        attempt_dict = {
            "attempt_1": attempt_1,
            "attempt_2": attempt_2
        }

        if output_idx == '0':
            submission_dict[task_id].insert(0, attempt_dict)
        else:
            submission_dict[task_id].append(attempt_dict)

    # Write to the new json file
    with open('sub_icecube.json', 'w') as file:
        json.dump(submission_dict, file, indent=4)


translate_submission('/kaggle/working/old_submission.csv')
