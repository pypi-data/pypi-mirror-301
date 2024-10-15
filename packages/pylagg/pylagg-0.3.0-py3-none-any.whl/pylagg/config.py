import os
import toml

from pylagg.cut_adapt import trim
import pylagg.cgr as cgr 
import pylagg.ena_download as ena


def config_accession_to_cgr(accession: str, config_file: str):
  current_dir = os.getcwd()

  if not os.path.isfile(config_file):
        print(f"The file '{config_file}' does not exist.")
        exit(0)

  try:
        config = toml.load(config_file)
  except:
        print("Error in the config file. Please check your formatting and spelling and try again. ")
        exit(0)
  

  output_dir = config.get('Files', {}).get('output',None)


  if output_dir == None:
      output_dir=current_dir
      

  SRA_file = ena.ena_download(accession, output_dir) #needs to be a string not a list

  # Check if the 'cutadapt' section exists
  if 'cutadapt' in config and bool(config['cutadapt']):
    trimmed_file = trim(SRA_file,config)
    if config.get('Files', {}).get('fastq', False) == False:
       os.remove(SRA_file)
    #run jellyfish with trimmed file
    if config.get('Files', {}).get('trim', False) == False:
      os.remove(trimmed_file)

  else:
      print("jellyfish")
      #run Jellyfish with SRA file
  
  #count_path will be the jellyfish produced kmer count
  counts_path = "test.counts"
  with open(counts_path, 'r') as f:
    cgr.config_count_file_to_image_file(f, counts_path.replace(".counts", ".png"),config)
  if config.get('Files', {}).get('counts', False) == False:
    os.remove(counts_path)

  
  
