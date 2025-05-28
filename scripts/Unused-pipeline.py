import os
import json

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

def main():
    pipeline_dir = "workspace/pipeline"
    master_pipeline_file = os.path.join(pipeline_dir, "pln_master.json")

    if not os.path.exists(master_pipeline_file):
        print("❌ Master pipeline not found.")
        return

    used_pipelines = set(extract_used_pipelines(master_pipeline_file, pipeline_dir))
    all_pipelines = get_all_pipelines(pipeline_dir)
    unused_pipelines = all_pipelines - used_pipelines

    print(f"\n🔍 Total pipelines found: {len(all_pipelines)}")
    print(f"✅ Used pipelines: {len(used_pipelines)}")
    print(f"❌ Unused pipelines: {len(unused_pipelines)}")

    if unused_pipelines:
        print("\n🗃️ List of unused pipelines:")
        for pipeline in sorted(unused_pipelines):
            print(f"  - {pipeline}")
    else:
        print("\n🎉 All pipelines are in use!")

if __name__ == "__main__":
    main()
