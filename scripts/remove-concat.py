import os
import re

def flatten_concat_line(line):
    pattern = r'^(\s*"value"\s*:\s*)"@concat\(\'archive/\',\s*@concat\((.*)\)\)"(,?)'
    match = re.match(pattern, line)
    if match:
        prefix = match.group(1)
        inner = match.group(2)
        suffix = match.group(3)
        new_line = f'{prefix}"@concat(\'archive/\', {inner})"{suffix}\n'
        return new_line
    return None

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated = False
    new_lines = []

    for line in lines:
        if "@concat('archive/', @concat(" in line:
            fixed_line = flatten_concat_line(line)
            if fixed_line:
                new_lines.append(fixed_line)
                updated = True
                continue
        new_lines.append(line)

    if updated:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ Updated: {filepath}")
    else:
        print(f"⏭️ No nested archive concat found in: {filepath}")

def main():
    dataset_dir = "workspace/dataset"  # change if needed
    for filename in os.listdir(dataset_dir):
        if filename.endswith(".json"):
            process_file(os.path.join(dataset_dir, filename))

if __name__ == "__main__":
    main()
