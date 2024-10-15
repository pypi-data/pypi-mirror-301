import csv
import requests


def bulk(taxon_id:str):

    url = f'https://www.ebi.ac.uk/ena/portal/api/links/taxon?accession={taxon_id}&format=tsv&result=read_run'
    response = requests.get(url)

    # Save the content to a file
    if response.status_code == 200:
        with open('ena_taxon_study.tsv', 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    file_path ='ena_taxon_study.tsv'
    with open(file_path, mode='r', newline='') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        
        # Skip the header (first line)
        next(tsv_reader)
        
        # Extract the first word of each line
        for row in tsv_reader:
            if row:  # Make sure the row is not empty
                print(row[0]) #print for now but in the future this will be where the function to download fastq files will be
