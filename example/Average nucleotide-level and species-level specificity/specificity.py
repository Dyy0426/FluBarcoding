import os
import pandas as pd
import tkinter as tk
from tkinter import simpledialog

def parse_fasta(lines):
    sequences, current_seq_id = {}, ""
    for line in lines:
        if line.startswith(">"):
            current_seq_id = line.strip()
            sequences[current_seq_id] = ""
        else:
            sequences[current_seq_id] += line.strip()
    return sequences

def process_and_export_sequences(input_file_path, output_folder_path):
    def modify_and_write_sequences(test_sequences, barcode_sequences, output_folder_path):
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        output_files = []
        for i, (_, barcode_seq) in enumerate(barcode_sequences):
            gap_indices = {index for index, char in enumerate(barcode_seq) if char == "-"}
            output_filename = f"modified_sequences_{i + 1}.txt"
            full_output_path = os.path.join(output_folder_path, output_filename)
            with open(full_output_path, "w") as output_file:
                for _, test_seq in test_sequences:
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

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    split_index = simpledialog.askinteger("Input", "Please enter the split index for test sequences and barcode sequences:", parent=root, minvalue=1, maxvalue=len(sequences))

    test_sequences = list(sequences.items())[:split_index]
    barcode_sequences = list(sequences.items())[split_index:]

    return modify_and_write_sequences(test_sequences, barcode_sequences, output_folder_path)

def read_sequences_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().replace('-', 'N') for line in file.readlines() if line.strip() and '>' not in line]

def calculate_specificity(barcode_sequence, species_sequences):
    total_nucleotide_diffs = 0
    barcode_length = len(barcode_sequence)
    num_species = len(species_sequences)
    specificity_cases = {n_diffs: 0 for n_diffs in range(1, 11)}

    for species_seq in species_sequences:
        if len(species_seq) < barcode_length:
            continue

        nucleotide_diffs = sum(1 for i in range(barcode_length) if species_seq[i] != barcode_sequence[i])
        total_nucleotide_diffs += nucleotide_diffs

        for n_diffs in specificity_cases:
            specificity_cases[n_diffs] += 100 if nucleotide_diffs >= n_diffs else 0

    average_nucleotide_specificity = (total_nucleotide_diffs / barcode_length / num_species) * 100
    average_specificity_cases = {n_diffs: (specificity / num_species) for n_diffs, specificity in specificity_cases.items()}

    return round(average_nucleotide_specificity, 4), average_specificity_cases

def process_files_specificity(input_fasta_path, barcode_file_path, output_excel_path):
    sequences = parse_fasta(open(input_fasta_path, 'r').readlines())

    output_folder_path = 'test_sequences'
    modify_and_write_sequences_output = process_and_export_sequences(input_fasta_path, output_folder_path)

    barcodes = read_sequences_from_file(barcode_file_path)
    results = []

    for i, barcode in enumerate(barcodes):
        species_file_name = f"modified_sequences_{i + 1}.txt"
        species_file_path = os.path.join(output_folder_path, species_file_name)

        if not os.path.exists(species_file_path):
            continue

        species_sequences = read_sequences_from_file(species_file_path)
        avg_nuc_spec, avg_specificity_cases = calculate_specificity(barcode, species_sequences)

        result = {
            'Barcode': barcode,
            'Species File': species_file_name,
            'Average Nucleotide Specificity': avg_nuc_spec
        }
        result.update({f'Avg Specificity (Diff >= {n_diffs})': spec for n_diffs, spec in avg_specificity_cases.items()})
        results.append(result)

    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index=False)

# Modify paths as needed
input_fasta_path = 'input.fasta'  # Replace with the path to your input FASTA file
barcode_file_path = 'barcodes_input.fasta'  # Replace with the path to your barcode file
output_excel_path = 'output.xlsx'  # Replace with the desired output Excel file path

process_files_specificity(input_fasta_path, barcode_file_path, output_excel_path)
