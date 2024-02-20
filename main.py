import re
from collections import defaultdict


TITLE_PATTERN = r"^title\s+(?P<title>.*)$"
#API_CALL_PATTERN = r"(?i)(?P<component>[\w\s\(\)]+(?<![:->]))*?->(?P<target>[\w\s\(\)]+(?<![:]))*?:(?P<message>[\w\s\(\)]+)"
API_CALL_PATTERN = r"(?i)(?P<component>[^\s:->]+(?:\s+[^\s:->]+)*?)\s*->\s*(?P<target>[^\s:->]+(?:\s+[^\s:->]+)*?)\s*:\s*(?P<message>.*)"
#API_RETURN_PATTERN = r"(?i)(?P<component>[\w\s\(\)]+(?<![:->]))*?-->(?P<target>[\w\s\(\)]+(?<![:]))*?:(?P<message>[\w\s\(\)]+)"
API_RETURN_PATTERN = r"(?i)(?P<component>[^\s:->]+(?:\s+[^\s:->]+)*?)\s*-->\s*(?P<target>[^\s:->]+(?:\s+[^\s:->]+)*?)\s*:\s*(?P<message>.*)"


def extract_api_from_sequence_diagram(line, targets):
    if not line:
        return  # Skip empty lines

    title_match = re.match(TITLE_PATTERN, line)
    if title_match:
        title = title_match.group("title")
        #print("Title:", title)
        return
    #print("Line:", line)
    api_return_match = re.match(API_RETURN_PATTERN, line, )
    if api_return_match:
        component = api_return_match.group("component")
        target = api_return_match.group("target")
        message = api_return_match.group("message")
        if target not in targets:
            targets[target] = []
        targets[target].append([component, target, message, "return"])
        #print(f"Return Value \t\t{component} <- {target}: {message}")
        return
    #else:
        #print("Not a return:", line)

    api_call_match = re.match(API_CALL_PATTERN, line)
    if api_call_match:
        component = api_call_match.group("component")
        target = api_call_match.group("target")
        message = api_call_match.group("message")
        if target not in targets:
            targets[target] = []
        targets[target].append([component, target, message, "call"])
        #print(f"Call Value \t\t{component} <- {target}: {message}")
        return
    #else:
        #print("Not a function:", line)

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
        if entry[3] == "call":
            print(f"Function Call \t\t{entry[0]} -> {entry[1]}: {entry[2]}")
        else:
            print(f"Return Value \t\t{entry[0]} <- {entry[1]}: {entry[2]}")
        #print(f"\t\t{entry}")
