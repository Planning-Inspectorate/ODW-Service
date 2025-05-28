import os
import json
import shutil

def extract_used_pipelines(file_path, pipeline_dir, visited=None):
    if visited is None:
        visited = set()
    pipelines = []
    with open(file_path, 'r') as f:
        data = json.load(f)
    activities = data.get("properties", {}).get("activities", [])
    for activity in activities:
        pipelines.extend(process_pipeline_references(activity, pipeline_dir, visited))
    return pipelines

def process_pipeline_references(activity, pipeline_dir, visited):
    pipelines = []
    type_props = activity.get("typeProperties", {})
    ref = type_props.get("pipeline", {}).get("referenceName")
    if ref and ref not in visited:
        pipelines.append(ref)
        visited.add(ref)
        nested_file = os.path.join(pipeline_dir, f"{ref}.json")
        if os.path.exists(nested_file):
            pipelines.extend(extract_used_pipelines(nested_file, pipeline_dir, visited))
    for key in ["ifFalseActivities", "ifTrueActivities", "activities"]:
        for nested in type_props.get(key, []):
            pipelines.extend(process_pipeline_references(nested, pipeline_dir, visited))
    return pipelines

def get_all_pipelines(pipeline_dir):
    return set(
        os.path.splitext(file)[0]
        for file in os.listdir(pipeline_dir)
        if file.endswith('.json')
    )

def extract_datasets_from_activity(activity):
    datasets = set()

    for key in ["inputs", "outputs"]:
        for ds in activity.get(key, []):
            ref = ds.get("referenceName")
            if ref:
                datasets.add(ref)

    type_props = activity.get("typeProperties", {})
    for key in ["dataset", "inputDataset", "outputDataset"]:
        ref = type_props.get(key, {}).get("referenceName")
        if ref:
            datasets.add(ref)

    if "activities" in type_props:
        for sub in type_props["activities"]:
            datasets.update(extract_datasets_from_activity(sub))

    return datasets

def extract_datasets_from_pipeline_file(pipeline_file):
    with open(pipeline_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f" Skipping invalid JSON: {pipeline_file}")
            return set()

    datasets = set()
    activities = data.get("properties", {}).get("activities", [])
    for activity in activities:
        datasets.update(extract_datasets_from_activity(activity))
    return datasets

def get_datasets_from_unused_pipelines(pipeline_dir, unused_pipelines):
    all_datasets = set()
    for pipeline_name in unused_pipelines:
        file_path = os.path.join(pipeline_dir, f"{pipeline_name}.json")
        if os.path.exists(file_path):
            datasets = extract_datasets_from_pipeline_file(file_path)
            all_datasets.update(datasets)
    return all_datasets

def move_datasets_to_archive(unused_datasets, dataset_dir):
    archive_dir = os.path.join(dataset_dir, "..", "dataset", "Archive", "Unused-Pipeline")
    os.makedirs(archive_dir, exist_ok=True)

    print(f"\n📁 Moving dataset files used only by unused pipelines to: {archive_dir}\n")

    for dataset in unused_datasets:
        filename = f"{dataset}.json"
        src_path = os.path.join(dataset_dir, filename)
        dest_path = os.path.join(archive_dir, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f" Moved dataset: {filename}")
        else:
            print(f" Dataset file not found: {filename}")

def main():
    pipeline_dir = "workspace/pipeline"
    dataset_dir = "workspace/dataset"
    master_pipeline_file = os.path.join(pipeline_dir, "pln_master.json")

    if not os.path.exists(master_pipeline_file):
        print(" Master pipeline not found.")
        return

    used_pipelines = set(extract_used_pipelines(master_pipeline_file, pipeline_dir))
    all_pipelines = get_all_pipelines(pipeline_dir)
    unused_pipelines = all_pipelines - used_pipelines

    print(f"🔍 Found {len(unused_pipelines)} unused pipelines.")

    unused_datasets = get_datasets_from_unused_pipelines(pipeline_dir, unused_pipelines)

    print(f"\n Datasets used only in unused pipelines ({len(unused_datasets)}):")
    for ds in sorted(unused_datasets):
        print(f"- {ds}")

    # Move dataset files used only in unused pipelines
    move_datasets_to_archive(unused_datasets, dataset_dir)

if __name__ == "__main__":
    main()
