import os
import json

def zeek_to_log(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    field = []
    json_f = []
    for line in lines:
        if line.startswith('#field'):
            fields = line.strip().split('\t')[1:]
        elif not line.startswith('#') and fields:
            values = line.strip().split('\t')
            entry = dict(zip(fields, values))
            json_f.append(entry)
    return json_f

def log_to_json(in_dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for filename in os.listdir(in_dir):
        if filename.endswith(".log"):
            log_path = os.path.join(in_dir, filename)
            json_out = zeek_to_log(log_path)

            json_file = filename.replace(".log", ".json")
            with open(os.path.join(out_dir, json_file), 'w') as jf:
                json.dump(json_out, jf, indent=2)
    print(f"JSON files saved in: {out_dir}")

def main():
    input_logs = os.path.expanduser("~/project")       
    output_json = "zeek_json_file"
    log_to_json(input_logs, output_json)

if __name__=="__main__":
    main()
