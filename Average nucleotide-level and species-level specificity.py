import os
import pandas as pd

def read_sequences_from_file(file_path):
    """
    Read sequences from a file, ignoring lines that start with '>' and replacing '-' with 'N'.
    """
    with open(file_path, 'r') as file:
        return [line.strip().replace('-', 'N') for line in file.readlines() if line.strip() and '>' not in line]

def calculate_specificity(barcode_sequence, species_sequences):
    """
    Calculate specificity based on nucleotide differences between the barcode sequence and species sequences.
    """
    total_nucleotide_diffs = 0
    total_species_specificity = 0
    barcode_length = len(barcode_sequence)
    num_species = len(species_sequences)
    specificity_cases = {n_diffs: 0 for n_diffs in range(1, 11)}

    for species_seq in species_sequences:
        # Check the length of the species nucleic acid sequence
        if len(species_seq) < barcode_length:
            continue  # Skip if the species sequence is shorter than the barcode segment

        nucleotide_diffs = sum(1 for i in range(barcode_length) if species_seq[i] != barcode_sequence[i])
        total_nucleotide_diffs += nucleotide_diffs

        # Calculate specificity for different numbers of differences
        for n_diffs in specificity_cases:
            specificity_cases[n_diffs] += 100 if nucleotide_diffs >= n_diffs else 0

    average_nucleotide_specificity = (total_nucleotide_diffs / barcode_length / num_species) * 100
    average_specificity_cases = {n_diffs: (specificity / num_species) for n_diffs, specificity in specificity_cases.items()}

    return round(average_nucleotide_specificity, 4), average_specificity_cases

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
barcode_file_path = 'input.txt'  # Replace with the path to the barcode file
species_folder_path = 'C:/...'  # Replace with the path to the species nucleic acid sequence library folder
output_file_path = 'output.xlsx'  # Replace with the desired output Excel file path

process_files(barcode_file_path, species_folder_path, output_file_path)
