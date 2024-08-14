# FluBarcoding
## Statistical analysis of data on conserved regions from DNAsp

## Degenerate base deletion.py
## 1D code establishment
## Average nucleotide-level and species-level specificity
### (1) Introduction
This script processes DNA sequences provided in FASTA format. It compares species sequences against barcode sequences to calculate the Average Nucleotide Recall Rate (ANRR) and the average recall rates at different thresholds. The script splits the input sequences into test sequences and barcode sequences based on a user-defined index, modifies the test sequences according to the structure of the barcode sequences, and then calculates the recall rates. The results are saved in an Excel file.
### (2) Dependencies
Before running the script, ensure that the following Python libraries are installed:
Pip install pandas, tkinter
import pandas
import tkinter (This is usually included in Python standard libraries)
### (3) Script Workflow
1)	Parsing FASTA Files:The script begins by reading and parsing the input FASTA file. Each sequence is identified by its ID (the line starting with >), and the sequences are stored in a dictionary.
2)	User Input: A simple dialog box will appear asking for the split index, which determines how the sequences will be divided into test sequences and barcode sequences.
3)	Modifying Test Sequences: The script modifies the test sequences by removing the gaps present in the corresponding barcode sequences and writes the modified sequences into separate files.
4)	Calculating Recall Rates: The script then reads the barcode sequences from a specified file and calculates the recall rates by comparing each modified test sequence with the corresponding barcode sequence.
5)	Saving Results: Finally, the script saves the calculated recall rates, including the ANRR and threshold-specific recall rates, into an Excel file.
### (4) Example Usage
input_fasta_path = ‘input.fasta’ # Replace with the path to your input FASTA file
barcode_file_path = ‘barcodes_input.fasta’ # Replace with the path to your barcode file
output_excel_path = ‘output.xlsx’ # Replace with the desired output Excel file path

process_files_recall(input_fasta_path, barcode_file_path, output_excel_path)
### (5) Functions Overview
parse_fasta(lines): Parses FASTA sequences from a list of lines.
modify_and_write_sequences(test_sequences, barcode_sequences, output_folder_path): Modifies test sequences by removing gaps and writes them to files.
calculate_recall_rates(barcode_sequence, species_sequences): Calculates ANRR and average recall rates at different thresholds.
process_files_recall(input_fasta_path, barcode_file_path, output_excel_path): The main function that processes the input files and generates the output Excel file.
read_sequences_from_file(file_path): Reads sequences from a specified file.
### (6) Notes
1.	The script requires user interaction to input the split index for dividing the sequences.
2.	Ensure that the input FASTA file is properly formatted and that the barcode file contains valid sequences for accurate results.
3.	The output files will be saved in the current working directory unless specified otherwise.

## Average nucleotide-level and species-level recall rate
This repository contains a Python script for processing FASTA files to analyze barcode sequences against test sequences, calculating specificity, and exporting results to an Excel file. The script is designed to handle DNA sequence data, calculate nucleotide specificity, and facilitate data sharing through an online platform.
