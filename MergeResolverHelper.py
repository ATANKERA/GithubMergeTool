import re

def extract_merge_conflict_markers():
    # Prompt the user to paste the merged file content
    print("Paste the merged file contents below (end with Ctrl+D or Ctrl+Z):")
    try:
        file_contents = ""
        while True:
            line = input()
            file_contents += line + "\n"
    except EOFError:
        pass

    # Regex patterns to find the first word after `<<<<<<< ` and `>>>>>>>`
    left_marker_pattern = r"<<<<<<< (\w+)"
    right_marker_pattern = r">>>>>>> (\w+)"

    # Find the first match for each pattern
    left_match = re.search(left_marker_pattern, file_contents)
    right_match = re.search(right_marker_pattern, file_contents)

    # Extract the words
    left_word = left_match.group(1) if left_match else None
    right_word = right_match.group(1) if right_match else None

    # Print the results
    print("\nResults:")
    if left_word:
        print(f"First word after '<<<<<<< ': {left_word}")
    else:
        print("No '<<<<<<< ' marker found.")

    if right_word:
        print(f"First word after '>>>>>>>': {right_word}")
    else:
        print("No '>>>>>>> ' marker found.")

    return left_word, right_word, file_contents

def pickVersion(mine, theirs):
    # Prompt the user to choose between 'mine' and 'theirs'
    while True:
        print("Choose the version to keep:")
        print("1. Mine (Your version)")
        print("2. Theirs (Their version)")

        choice = input("Enter 1 for 'Mine' or 2 for 'Theirs': ").strip()

        if choice == '1':
            return 2
        elif choice == '2':
            return 1
        else:
            print("Invalid input. Please enter '1' or '2'.")


def merge(merged_content, choice, left_word, right_word):
    # The conflict markers we want to remove
    if choice == 1:
        # Match the conflict markers for 'mine' (i.e., keep the section marked with '<<<<<<< mine')
        regex = r"<<<<<<< " + re.escape(left_word) + r"\n([\s\S]*?)=======\n"
        merged_content = re.sub(regex, "", merged_content, flags=re.MULTILINE)

    elif choice == 2:
        # Match the conflict markers for 'theirs' (i.e., keep the section marked with '>>>>>>> theirs')
        regex = r"=======\n([\s\S]*?)>>>>>>> " + re.escape(right_word) + r"\n"
        merged_content = re.sub(regex, "", merged_content, flags=re.MULTILINE)

    else:
        raise ValueError("Invalid choice. Please choose either 1 or 2.")
    
    merged_content = re.sub(r"<<<<<<< " + re.escape(left_word) + r"\n", "", merged_content)  # Remove <<<<<<< left_word
    merged_content = re.sub(r">>>>>>> " + re.escape(right_word) + r"\n", "", merged_content)  # Remove >>>>>>> right_word
    
    return merged_content

# Call the function to extract conflict markers and content
a, b, merged_file_content = extract_merge_conflict_markers()

# Allow the user to pick which version to keep
version = pickVersion(a, b)

# Apply the merge based on the user's choice
output = merge(merged_file_content, version, a, b)

print("Merged content after applying your choice:")
print(output)


def save_to_file(content):
    # Save the merged content to 'mergedfile.txt'
    with open("mergedfile.txt", "w") as file:
        file.write(content)
    print("\nMerged content saved to 'mergedfile.txt'.")

save_to_file(output)