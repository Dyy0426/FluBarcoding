import os
import tkinter as tk
from tkinter import simpledialog

def process_and_export_sequences(input_file_path, output_folder_path):
    def parse_fasta(lines):
        """
        Parse FASTA formatted sequences from given lines.
        """
        sequences, current_seq_id = {}, ""
        for line in lines:
            if line.startswith(">"):
                current_seq_id = line.strip()
                sequences[current_seq_id] = ""
            else:
                sequences[current_seq_id] += line.strip()
        return sequences

    def modify_and_write_sequences(test_sequences, barcode_sequences, output_folder_path):
        """
        Modify test sequences by removing gaps based on barcode sequences and write to output files.
        """
        # Check if the output directory exists, create if it doesn't
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        output_files = []
        for i, (_, barcode_seq) in enumerate(barcode_sequences):
            # Identify gap positions in the barcode sequence
            gap_indices = {index for index, char in enumerate(barcode_seq) if char == "-"}
            output_filename = f"example_{i + 1}.txt"
            full_output_path = os.path.join(output_folder_path, output_filename)
            with open(full_output_path, "w") as output_file:
                for _, test_seq in test_sequences:
                    # Remove characters at gap positions from the test sequence
                    modified_seq = ''.join(char for index, char in enumerate(test_seq) if index not in gap_indices)
                    output_file.write(modified_seq + "\n")
            output_files.append(full_output_path)
        return output_files

    file_extension = input_file_path.split('.')[-1].lower()
    is_fasta_format = file_extension in ['fasta', 'fas', 'txt']

    with open(input_file_path, 'r') as file:
        if is_fasta_format:
            sequences = parse_fasta(file.readlines())
        else:
            raise ValueError("Unsupported file format")

    # Create a popup window to request input
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    split_index = simpledialog.askinteger("Input", "Please enter the split index for test sequences and barcode sequences:", parent=root, minvalue=1, maxvalue=len(sequences))

    test_sequences = list(sequences.items())[:split_index]
    barcode_sequences = list(sequences.items())[split_index:]

    return modify_and_write_sequences(test_sequences, barcode_sequences, output_folder_path)

# Using the function
input_file_path = 'input.fasta'  # Replace with your file path
output_folder_path = 'output_directory'  # Replace with your output directory path
output_files = process_and_export_sequences(input_file_path, output_folder_path)
