import os
import json
import shutil

def extract_datasets_from_activity(activity):
    datasets = set()

    # Standard input/output dataset references
    for io_key in ["inputs", "outputs"]:
        for ds in activity.get(io_key, []):
            ref = ds.get("referenceName")
            if ref:
                datasets.add(ref)

    # typeProperties -> dataset, inputDataset, outputDataset
    nested = activity.get("typeProperties", {})
    for key in ["dataset", "inputDataset", "outputDataset"]:
        ref = nested.get(key, {}).get("referenceName")
        if ref:
            datasets.add(ref)

    # RECURSIVE: dive into nested activities
    if "activities" in nested:
        for sub_activity in nested["activities"]:
            datasets.update(extract_datasets_from_activity(sub_activity))

    return datasets

def extract_datasets_from_pipeline_file(pipeline_file):
    datasets = set()
    with open(pipeline_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f" Skipping invalid JSON: {pipeline_file}")
            return datasets

    activities = data.get("properties", {}).get("activities", [])
    for activity in activities:
        datasets.update(extract_datasets_from_activity(activity))

    return datasets

def get_pipeline_datasets(pipeline_dir):
    all_datasets = set()
    for file in os.listdir(pipeline_dir):
        if file.endswith(".json"):
            full_path = os.path.join(pipeline_dir, file)
            all_datasets.update(extract_datasets_from_pipeline_file(full_path))
    return all_datasets

def get_all_workspace_datasets(dataset_dir):
    all_datasets = set()
    for file in os.listdir(dataset_dir):
        if file.endswith(".json"):
            dataset_name = os.path.splitext(file)[0]
            all_datasets.add(dataset_name)
    return all_datasets

def move_unused_datasets(unused_datasets, dataset_dir):
    archive_dir = os.path.join(dataset_dir, "Archive", "Unused-Dataset")
    os.makedirs(archive_dir, exist_ok=True)

    print(f"\n Moving unused dataset files to: {archive_dir}\n")

    for ds in sorted(unused_datasets):
        filename = f"{ds}.json"
        src_path = os.path.join(dataset_dir, filename)
        dest_path = os.path.join(archive_dir, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f" Moved: {filename}")
        else:
            print(f" Not found: {filename}")

def main():
    pipeline_dir = "workspace/pipeline"
    dataset_dir = "workspace/dataset"

    if not os.path.exists(pipeline_dir) or not os.path.exists(dataset_dir):
        print(" One or more required folders not found.")
        return

    print(" Collecting datasets used in pipelines...")
    pipeline_datasets = get_pipeline_datasets(pipeline_dir)

    print(" Collecting all datasets in workspace/dataset...")
    all_datasets = get_all_workspace_datasets(dataset_dir)

    used = all_datasets & pipeline_datasets
    unused = all_datasets - pipeline_datasets

    print("\n USED DATASETS:")
    for ds in sorted(used):
        print(f"   {ds}")

    print("\n UNUSED DATASETS:")
    for ds in sorted(unused):
        print(f"   {ds}")

    # Move unused dataset files to archive
    move_unused_datasets(unused, dataset_dir)

if __name__ == "__main__":
    main()
