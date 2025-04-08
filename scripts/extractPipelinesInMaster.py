import os
import json

def extract_pipelines(file_path, pipeline_dir, visited=None):
    if visited is None:
        visited = set()

    pipelines = []

    with open(file_path, 'r') as f:
        data = json.load(f)

    activities = data.get("properties", {}).get("activities", [])
    for activity in activities:
        pipelines.extend(process_activity(activity, pipeline_dir, visited))

    return pipelines

def process_activity(activity, pipeline_dir, visited):
    pipelines = []
    
    type_properties = activity.get("typeProperties", {})
    pipeline_reference = type_properties.get("pipeline", {}).get("referenceName")
    if pipeline_reference and pipeline_reference not in visited:
        pipelines.append(pipeline_reference)
        visited.add(pipeline_reference)

        pipeline_file = os.path.join(pipeline_dir, f"{pipeline_reference}.json")
        if os.path.exists(pipeline_file):
            pipelines.extend(extract_pipelines(pipeline_file, pipeline_dir, visited))
        else:
            print(f"Warning: File not found for pipeline {pipeline_reference} at {pipeline_file}")
            
    for key in ["ifFalseActivities", "ifTrueActivities", "activities"]:
        nested_activities = type_properties.get(key, [])
        for nested_activity in nested_activities:
            pipelines.extend(process_activity(nested_activity, pipeline_dir, visited))
    
    return pipelines


def main(): 
    pipeline_dir = "workspace/pipeline" 
    master_pipeline_file = os.path.join(pipeline_dir, "pln_master.json")
    all_pipelines = extract_pipelines(master_pipeline_file, pipeline_dir)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "pipeline_dependencies.txt")
    
    with open(output_file, 'w') as f:
        for pipeline in sorted(set(all_pipelines)):
            f.write(f"{pipeline}\n")

    print(f"Pipeline dependencies written to {output_file}")


if __name__ == "__main__":
    main()
