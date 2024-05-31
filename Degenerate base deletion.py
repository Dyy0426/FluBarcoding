import os
import re

def process_fasta_files(folder_path, modify_titles=False, new_title=None, rename_to_filename=False):
    # Identify all .fasta or .fas files in the folder
    fasta_files = [f for f in os.listdir(folder_path) if f.endswith('.fasta') or f.endswith('.fas')]

    for file_name in fasta_files:
        file_path = os.path.join(folder_path, file_name)
        # Read the original file
        with open(file_path, 'r') as file:
            sequences = file.readlines()

        # Process each line
        new_sequences = []
        sequence_number = 1  # Initialize sequence number
        for line in sequences:
            if line.startswith('>'):  # Sequence title
                if modify_titles and new_title:
                    # Modify the title to user input and add sequence number
                    new_sequences.append(f">{new_title}({sequence_number})\n")
                elif rename_to_filename:
                    # Rename the title to the filename and add sequence number
                    title = f">{os.path.splitext(file_name)[0]}({sequence_number})\n"
                    new_sequences.append(title)
                else:
                    # Keep the original title and add sequence number
                    new_sequences.append(f"{line.strip()}({sequence_number})\n")
                sequence_number += 1
            else:
                # Remove degenerate bases
                cleaned_sequence = re.sub('[RYMKSWHBVDNZ]', '', line, flags=re.IGNORECASE)
                new_sequences.append(cleaned_sequence)

        # Output the file, replacing the original file
        with open(file_path, 'w') as new_file:
            new_file.writelines(new_sequences)
        print(f"Processed and replaced {file_name}")

# Example usage
folder_path = 'C:\...'
modify_titles = input("Do you want to modify the sequence titles to a custom title? (yes/no): ").lower() == 'yes'
rename_to_filename = input("Do you want to rename all sequence titles to the file name? (yes/no): ").lower() == 'yes'

if modify_titles:
    new_title = input("Enter the new title (without '>'): ")
    process_fasta_files(folder_path, modify_titles, new_title, rename_to_filename)
elif rename_to_filename:
    process_fasta_files(folder_path, False, None, rename_to_filename)
else:
    process_fasta_files(folder_path)
