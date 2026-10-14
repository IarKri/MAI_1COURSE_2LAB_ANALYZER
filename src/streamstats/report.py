import json

def report (statistics, output_file):
    statistics = json.dumps(statistics, indent = 2)
    if output_file:
        with open(f"reports/{output_file}", "w", encoding="utf-8") as json_file:
            json_file.write(statistics)
    else:
        print(statistics)
