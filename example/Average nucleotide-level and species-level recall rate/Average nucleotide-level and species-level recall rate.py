import os
import tkinter as tk
from tkinter import simpledialog
import pandas as pd

def parse_fasta(lines):
    sequences, current_seq_id = {}, ""
    for line in lines:
        if line.startswith(">"):
            current_seq_id = line.strip()
            sequences[current_seq_id] = ""
        else:
            sequences[current_seq_id] += line.strip()
    return sequences

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

def calculate_recall_rates(barcode_sequence, species_sequences):
    total_correct_nucleotides = 0
    barcode_length = len(barcode_sequence)
    num_species = len(species_sequences)
    recall_rates = {threshold: 0 for threshold in range(90, 100)}

    for species_seq in species_sequences:
        if len(species_seq) < barcode_length:
            continue

        correct_nucleotides = sum(1 for i in range(barcode_length) if species_seq[i] == barcode_sequence[i])
        total_correct_nucleotides += correct_nucleotides

        individual_recall = correct_nucleotides / barcode_length * 100
        for threshold in recall_rates:
            recall_rates[threshold] += 1 if individual_recall > threshold else 0

    average_nucleotide_recall_rate = (total_correct_nucleotides / barcode_length / num_species) * 100
    average_recall_rates = {threshold: (recall / num_species) * 100 for threshold, recall in recall_rates.items()}

    return round(average_nucleotide_recall_rate, 4), average_recall_rates

def process_files_recall(input_fasta_path, barcode_file_path, output_excel_path):
    sequences = parse_fasta(open(input_fasta_path, 'r').readlines())

    root = tk.Tk()
    root.withdraw()
    split_index = simpledialog.askinteger("Input", "Please enter the split index for test sequences and barcode sequences:", parent=root, minvalue=1, maxvalue=len(sequences))

    test_sequences = list(sequences.items())[:split_index]
    barcode_sequences = list(sequences.items())[split_index:]

    output_folder_path = 'test_sequences'
    modified_files = modify_and_write_sequences(test_sequences, barcode_sequences, output_folder_path)

    barcodes = read_sequences_from_file(barcode_file_path)
    results = []

    for i, barcode in enumerate(barcodes):
        species_file_name = f"modified_sequences_{i + 1}.txt"
        species_file_path = os.path.join(output_folder_path, species_file_name)

        if not os.path.exists(species_file_path):
            continue

        species_sequences = read_sequences_from_file(species_file_path)
        avg_nuc_recall, avg_recall_rates = calculate_recall_rates(barcode, species_sequences)

        result = {
            'Barcode': barcode,
            'Species File': species_file_name,
            'Average Nucleotide Recall Rate': avg_nuc_recall
        }
        result.update({f'Avg Recall Rate > {threshold}%': rate for threshold, rate in avg_recall_rates.items()})
        results.append(result)

    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index=False)

def read_sequences_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and '>' not in line]

# 使用函数
input_fasta_path = 'input.fasta'  # Replace with the path to your input FASTA file
barcode_file_path = 'barcodes_input.fasta'  # Replace with the path to your barcode file
output_excel_path = 'output.xlsx'  # Replace with the desired output Excel file path

process_files_recall(input_fasta_path, barcode_file_path, output_excel_path)
