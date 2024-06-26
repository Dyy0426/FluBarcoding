import os
import pandas as pd

def read_sequences_from_file(file_path):
    """
    Read sequences from a file, ignoring lines that start with '>'.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip() and '>' not in line]

def calculate_recall_rates(barcode_sequence, species_sequences):
    """
    Calculate recall rates at different thresholds.
    """
    total_correct_nucleotides = 0
    barcode_length = len(barcode_sequence)
    num_species = len(species_sequences)
    recall_rates = {threshold: 0 for threshold in range(1, 100)}

    for species_seq in species_sequences:
        # Check the length of the species nucleic acid sequence
        if len(species_seq) < barcode_length:
            continue  # Skip if the species sequence is shorter than the barcode segment

        correct_nucleotides = sum(1 for i in range(barcode_length) if species_seq[i] == barcode_sequence[i])
        total_correct_nucleotides += correct_nucleotides

        # Calculate individual recall rate
        individual_recall = correct_nucleotides / barcode_length * 100
        for threshold in recall_rates:
            recall_rates[threshold] += 1 if individual_recall > threshold else 0

    average_nucleotide_recall_rate = (total_correct_nucleotides / barcode_length / num_species) * 100
    average_recall_rates = {threshold: (recall / num_species) * 100 for threshold, recall in recall_rates.items()}

    return round(average_nucleotide_recall_rate, 4), average_recall_rates

def process_files(barcode_file_path, species_folder_path, output_excel_path):
    """
    Process all files and export results to an Excel file.
    """
    barcodes = read_sequences_from_file(barcode_file_path)
    results = []

    for i, barcode in enumerate(barcodes):
        species_file_name = f"example_{i + 1}.txt"
        species_file_path = os.path.join(species_folder_path, species_file_name)

        # Check if the file exists
        if not os.path.exists(species_file_path):
            continue  # Skip if the file does not exist

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

# Modify paths as needed
barcode_file_path = 'input.txt'  # Replace with the path to the barcode file
species_folder_path = 'test sequences'  # Replace with the path to the species nucleic acid sequence library folder
output_file_path = 'output.xlsx'  # Replace with the desired output Excel file path

process_files(barcode_file_path, species_folder_path, output_file_path)
