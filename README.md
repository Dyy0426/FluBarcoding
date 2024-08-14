# FluBarcoding
## 1. Statistical analysis of data on conserved regions from DNAsp

## 2. Degenerate base deletion
### (1) Introduction
The process_fasta_files script is designed to process all FASTA files (.fasta or .fas) within a specified folder. It offers functionality to modify sequence titles, rename sequence titles to match the file name, and clean up sequences by removing degenerate bases.
### (2) Dependencies
This script does not require any external Python packages. It only relies on Python's built-in modules: os and re.
### （3）Usage
1. Set the folder path where your FASTA files are stored.
2. Choose your options:
Modify titles to a custom title.

Rename sequence titles to the filename.

Keep the original titles with sequence numbering.

3. Run the script:
```python
folder_path = 'C:\\path_to_your_folder'  # Replace with your folder path
modify_titles = input("Do you want to modify the sequence titles to a custom title? (yes/no): ").lower() == 'yes'
rename_to_filename = input("Do you want to rename all sequence titles to the file name? (yes/no): ").lower() == 'yes'

if modify_titles:
    new_title = input("Enter the new title (without '>'): ")    
    process_fasta_files(folder_path, modify_titles, new_title, rename_to_filename)    
elif rename_to_filename:
    process_fasta_files(folder_path, False, None, rename_to_filename)   
else:
    process_fasta_files(folder_path)
```
### （4）Script Functionality
1. File Identification: The script scans the specified folder for .fasta or .fas files.

2. Sequence Title Modification: You can choose to replace each sequence's title with a custom title and add a sequence number. Alternatively, titles can be replaced with the file name, along with a sequence number.

3. Sequence Cleaning: The script removes degenerate bases (such as R, Y, M, K, S, W, H, B, V, D, N, Z) from the sequences, ensuring only standard bases (A, T, C, G) remain.

4. Output: The script overwrites the original FASTA files with the processed sequences.
## 3. 1D code establishment
### (1) Introduction
The replace_bases_and_format script is designed to process a text-based file (either .docx or .txt), replacing specific nucleotide bases (A, T, G, C) with a custom character (|) and formatting them with specific fonts, sizes, and colors. The output is a formatted Word document (.docx) that visually represents the modified sequence data.
### (2) Dependencies
To run this script, you need the following Python packages:
pip install python-docx #For reading and writing .docx files.
### （3）Usage
```
from docx import Document
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

#Define input and output files
input_file = 'input.docx'  # Replace with your input file path. Prepare a .docx or .txt file containing nucleotide sequences where bases A, T, G, C will be processed.
output_file = 'output.docx'  # Replace with your desired output file path. Specify the output file path for the new formatted Word document.

#Run the script
replace_bases_and_format(input_file, output_file)
```
### （4）Script Functionality
1)	Input File Handling: The script accepts .docx and .txt files. It reads the content, preparing it for processing.
2)	Base Replacement:
The bases A, T, G, C are replaced with the character |.

Each base is formatted with:

A: Font "Showcard Gothic", size 14pt, color RGB(128, 118, 163)

T: Font "Showcard Gothic", size 14pt, color RGB(255, 0, 0)

G: Font "Showcard Gothic", size 16pt, color RGB(86, 152, 195)

C: Font "Showcard Gothic", size 16pt, color RGB(0, 176, 80)

3)	Output: The modified text is saved as a new .docx file with the specified formatting.

### （5）Notes
1）Ensure the font "Showcard Gothic" is available on your system. If not, you can modify the script to use another font.
2）The script assumes standard text sequences; if you have special formatting or non-standard text, additional processing might be required.
## 4. Average nucleotide-level and species-level recall rate
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
```
input_fasta_path = ‘input.fasta’ # Replace with the path to your input FASTA file
barcode_file_path = ‘barcodes_input.fasta’ # Replace with the path to your barcode file
output_excel_path = ‘output.xlsx’ # Replace with the desired output Excel file path

process_files_recall(input_fasta_path, barcode_file_path, output_excel_path)
```
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

## 5. Average nucleotide-level and species-level specificity
### (1) Introduction
This repository provides a Python script to analyze the specificity of DNA sequences using barcode sequences. The script processes sequences in FASTA format, computes the average nucleotide specificity, and generates an Excel file containing the results.
### (2) Dependencies
Before running the script, ensure that the following Python libraries are installed:
Pip install pandas, tkinter
import pandas
import tkinter (This is usually included in Python standard libraries)
### (3) Script Workflow
1)	Input Files: Load the input FASTA and barcode files.
2)	Sequence Splitting: Split sequences into test and barcode groups based on user input.
3)	Specificity Calculation: Modify sequences, then calculate and compile specificity results.
4)	Excel Export: Export the results to an Excel file for analysis.
### (4) Example Usage
```
input_fasta_path = ‘input.fasta’ # Replace with the path to your input FASTA file
barcode_file_path = ‘barcodes_input.fasta’ # Replace with the path to your barcode file
output_excel_path = ‘output.xlsx’ # Replace with the desired output Excel file path

process_files_specificity(input_fasta_path, barcode_file_path, output_excel_path)
```
### （5） Functions Overview
parse_fasta(lines): Parses sequences from a list of lines in FASTA format.
process_and_export_sequences(input_file_path, output_folder_path): Modifies sequences based on barcode gaps and exports them to text files.
calculate_specificity(barcode_sequence, species_sequences): Calculates the average nucleotide specificity and specificity cases.
process_files_specificity(input_fasta_path, barcode_file_path, output_excel_path): The main function that processes the input files and generates the output Excel file.
### （6）Notes
1.	Ensure the input FASTA file is formatted correctly for accurate results.
2.	The script expects the input sequences to be properly aligned with the barcode sequences.
