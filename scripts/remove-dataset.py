import os
import re

def fix_inline_dataset_concats(line):
    # Pattern: @concat('archive/', @dataset().something) -> @concat('archive/', dataset().something)
    pattern = r"(@concat\('archive/',\s*)@dataset\(\)(\.[a-zA-Z0-9_]+)(\))"
    fixed_line = re.sub(pattern, r"\1dataset()\2\3", line)
    return fixed_line if fixed_line != line else None

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated = False
    new_lines = []

    for line in lines:
        if "@concat('archive/', @dataset()." in line:
            fixed = fix_inline_dataset_concats(line)
            if fixed:
                new_lines.append(fixed)
                updated = True
                continue
        new_lines.append(line)

    if updated:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ Updated: {filepath}")
    else:
        print(f"⏭️ No matching archive-dataset lines in: {filepath}")

def main():
    dataset_dir = "workspace/dataset"  # update path if needed
    for filename in os.listdir(dataset_dir):
        if filename.endswith(".json"):
            process_file(os.path.join(dataset_dir, filename))

if __name__ == "__main__":
    main()
