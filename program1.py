
input_filename = "input.txt"
output_filename = "output.txt"
with open(input_filename, "r") as infile:
    lines = infile.readlines()
total_lines = len(lines)
first_two_lines = lines[:2]
with open(output_filename, "w") as outfile:
    outfile.writelines(first_two_lines)
print(f"Total number of lines: {total_lines}")
print(f"First two lines written to {output_filename}")