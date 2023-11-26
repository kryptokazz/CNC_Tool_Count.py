import os
import re
from collections import defaultdict

def count_tools_in_file(file_path):
    tool_counts = defaultdict(int)
    tool_pattern = re.compile(r'\bT\d{2,3}\b')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if 'G54' in line and '(' not in line and ')' not in line:
                    break
                matches = tool_pattern.findall(line)
                for match in matches:
                    tool_counts[match] += 1
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

    return tool_counts

def count_tools_recursively(directory):
    tool_counts_per_file = defaultdict(dict)
    total_tool_counts = defaultdict(int)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.EIA') and not file.endswith('1000.EIA'):
                file_path = os.path.join(root, file)
                file_tool_counts = count_tools_in_file(file_path)
                if file_tool_counts is not None:
                    tool_counts_per_file[file_path] = file_tool_counts
                    for tool, count in file_tool_counts.items():
                        total_tool_counts[tool] += count
                else:
                    tool_counts_per_file[file_path] = {}

    return tool_counts_per_file, total_tool_counts

def write_results_to_file(tool_counts_per_file, total_tool_counts, filename="tool_counts_output.txt"):
    with open(filename, 'w') as file:
        for file_path, counts in tool_counts_per_file.items():
            file.write(f"File: {file_path}\n")
            if counts:
                for tool, count in counts.items():
                    file.write(f"  {tool}: {count}\n")
            else:
                file.write("  No tools found or file contains 'G54' before any tool labels.\n")

        file.write("\nTotal Tool Counts Across All Files:\n")
        for tool, count in total_tool_counts.items():
            file.write(f"{tool}: {count}\n")

# Main execution
base_directory_path = input("Enter the path to the directory: ")
tool_counts_per_file, total_tool_counts = count_tools_recursively(base_directory_path)

# Write to a text file in the current directory
write_results_to_file(tool_counts_per_file, total_tool_counts)

