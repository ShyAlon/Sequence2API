import re
from collections import defaultdict


TITLE_PATTERN = r"^title\s+(?P<title>.*)$"
API_CALL_PATTERN = r"(?i)(?P<component>\w+)\s*(?:->\s*|\s*-+\s*->\s*)\s*(?P<target>\w+)\s*:\s*(?P<message>\w+)\s*(?:\((?P<arguments>.*)\))?"
API_RETURN_PATTERN = r"(?i)(?P<component>\w+)\s*(?:-->\s*|\s*-+\s*-->\s*)\s*(?P<target>\w+)\s*:\s*(?P<message>\w+)\s*(?:\((?P<arguments>.*)\))?"


def extract_api_from_sequence_diagram(line, targets):
    if not line:
        return  # Skip empty lines

    title_match = re.match(TITLE_PATTERN, line)
    if title_match:
        title = title_match.group("title")
        return
    
    api_return_match = re.match(API_RETURN_PATTERN, line)
    if api_return_match:
        component = api_return_match.group("component")
        target = api_return_match.group("target")
        message = api_return_match.group("message")
        arguments = api_return_match.group("arguments")  # Extract arguments if present
        arguments = [arg.strip() for arg in arguments.split(",")] if arguments else []
        if target not in targets:
            targets[target] = []
        targets[target].append([component, target, message, arguments, "return"])
        return

    api_call_match = re.match(API_CALL_PATTERN, line)
    if api_call_match:
        component = api_call_match.group("component")
        target = api_call_match.group("target")
        message = api_call_match.group("message")
        arguments = api_call_match.group("arguments")  # Extract arguments if present
        arguments = [arg.strip() for arg in arguments.split(",")] if arguments else []
        if target not in targets:
            targets[target] = []
        targets[target].append([component, target, message, arguments, "call"])
        return


def extract_api_from_sequence_diagram_file(filename):
    components = defaultdict(list)

    for line in open(filename, "r"):
        line = line.strip()
        extract_api_from_sequence_diagram(line, components)

    return components


# Example usage
filename = "sequences.txt"
components = extract_api_from_sequence_diagram_file(filename)

print("API entries:")
for component, entries in components.items():
    print(f"\t{component}:")
    for entry in entries:
        if entry[4] == "call":
            print(f"Function Call \t\t{entry[0]} -> {entry[1]}: {entry[2]}({', '.join(entry[3])})")
        else:
            print(f"Return Value \t\t{entry[0]} <- {entry[1]}: {entry[2]}({', '.join(entry[3])})")
        #print(f"\t\t{entry}")
