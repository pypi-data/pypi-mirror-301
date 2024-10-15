from ftplib import FTP
import os
from typing import List, Optional
from io import BufferedWriter

import rich.progress as prog
from rich.progress import Progress
import toml

def quit_connection(message: Optional[str], ftp: FTP):
    if message is not None:
        print(message)
    # quit() can throw an exception if ftp server responds with error
    try:
        ftp.quit()
    except Exception as e:
        # This is more like a log message, just something to know that the ftp QUIT command failed.
        # This is not a critical error, so we can just close the connection with ftp.close().
        print("ftp QUIT command failed, trying to close the connection with ftp.close()", e)
        ftp.close()

# def download_with_retries(ftp, file_name, local_file_path, retries, delay):
#     for attempt in range(retries):
#         try:
#             with open(local_file_path, 'wb') as f:
#                 ftp.retrbinary(f"RETR {file_name}", f.write)
#             return True 
#         except ftplib.error_temp as e:
#             print(f"Temporary error: {e}, retrying... ({attempt + 1}/{retries})")
#             # halts execution of the program for a specified number of seconds
#             time.sleep(delay)
#         except Exception as e:
#             return False
#     # if all retries fail, return False
#     return False

def handle_config_ena_download() -> bool:
    '''    
    Reads a TOML file and runs the commands specified in the 'download_args' section.
    
    Returns True if parsing the download part of config file succeeds and results in data, and False otherwise.
    '''

    config_file_path = "config.toml"

    if not os.path.isfile(config_file_path):  
        return False
    
    # read the TOML file
    try:
        config = toml.load(config_file_path)
    except Exception as e:
        if type(e) == toml.TomlDecodeError:
            print("ERROR: Invalid TOML file. Please provide a valid TOML file.")
        return False

    accession_list_config = []
    output_directory_config = None
    if 'download_args' in config:
        arguments = config['download_args']
        
        for key, value in arguments.items():
            if (key == '-list_of_accessions'):
                if isinstance(value, list):
                    accession_list_config = value
                else:
                    print("ERROR: Value for key '-list_of_accessions' in config file must be a list.")
                    return False
            elif (key == '-output_dir'):
                # TODO: possibly add validations for type of value that output_dir should be
                output_directory_config = value
            else:
                print("ERROR: Found unexpected key in download_args section of config file: {}".format(key))
                return False
            
        if (accession_list_config == []):
            print("ERROR: No accession numbers found in the config file.")
            return False
        
        if (output_directory_config != None):
            for item in accession_list_config:
                ena_download(item, output_directory_config)

        if (output_directory_config == None):
            for item in accession_list_config:
                ena_download(item, None)

        return True        

    else:
        # no 'download_args' section found in the config file
        return False


def ena_download(sra_accession: str, output_dir: str = None) -> List[str]: 

    # TODO: what to do in the case that someone provides an accession number in the cli and also
    # provides a config file with a list of accession numbers? should we just apppend that number 
    # to the list if it is not already in the list?

    # small argument validations for the sra_accession parameter
    if (not sra_accession.isalnum()):
        print("Invalid SRA accession number. Please provide a valid SRA accession number.")
        return

    ftp = FTP('ftp.sra.ebi.ac.uk')
    ftp.login()

    prefix = sra_accession[:6]
    last_digit_of_accession = sra_accession[len(sra_accession)-1]

    # handles different format of directory for shorter accession numbers
    if (len(sra_accession) < 10):
        directory = f'/vol1/fastq/{prefix}/{sra_accession}'
    else:
        directory = f'/vol1/fastq/{prefix}/00{last_digit_of_accession}/{sra_accession}'

    try:
        ftp.cwd(directory)
    except Exception:
        quit_connection("Failed to access the directory for the provided accession number.\n"
                 "Please ensure that the accession number is correct and the corresponding\n"
                 "FASTQ files are available on ENA.", ftp)
        return

    file_names = ftp.nlst()
    if (file_names == []):
        quit_connection("No files found for the given SRA accession number.", ftp)
        return
    
    if (output_dir != None):
        if not os.path.exists(output_dir):
            quit_connection("Output directory given for ENA downloading results does not exist.", ftp)
            return

    output_files = []

    with create_progress_bar() as progress:
        for file_name in file_names:
            size = ftp.size(f"{file_name}")
            task = progress.add_task(f"Downloading {file_name}", total=size)
            
            # build local file path
            if (output_dir != None):
                local_file_path = os.path.join(output_dir, file_name)
            else:
                local_file_path = file_name

            output_files.append(local_file_path)
            
            # skip download if the entire file already exists
            if os.path.isfile(local_file_path) and os.path.getsize(local_file_path) == size:
                progress.update(task, advance=size)
                continue

            # Use for later if we want to implement downloads with retries 

            #       if (download_with_retries(ftp, file_name, local_file_path, 3, 2)):
            #           print(f"Downloaded {file_name} successfully!")
            #       else:
            #           print(f"Failed to download {file_name}.")

            with open(local_file_path, 'wb') as f:
                callback = lambda data : write_file(f, data, progress, task)
                ftp.retrbinary(f"RETR {file_name}", callback)

            
            
    quit_connection(None, ftp)
    return output_files


def write_file(file: BufferedWriter, data: bytes, progress: Progress, task: prog.TaskID):
    '''
    Writes data to a file buffer and updates the task for a progress bar
    '''
    file.write(data)
    progress.update(task, advance=len(data))


def create_progress_bar() -> Progress:
    '''
    Creates a progress bar configured for ena downloading.
    '''
    return Progress(prog.SpinnerColumn(),
                    prog.TextColumn("[progress.description]{task.description}"),
                    prog.BarColumn(),
                    prog.DownloadColumn(),
                    prog.TaskProgressColumn(),
                    prog.TimeElapsedColumn())
