import subprocess
import os
from typing import List
import toml
import rich.progress as prog
from rich.progress import Progress

def get_zcat_command() -> str:
    '''
    Checks if zcat or gzcat exist on the machine, returns whichever is functional!
    '''
    try:
        subprocess.check_output("zcat --help", shell=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.check_output("gzcat --help", shell=True)
        except subprocess.CalledProcessError:
            raise Exception("Error working with fastq.gz file! zcat or gzcat not found on this machine!")
        else:
            return "gzcat"
    else:
        return "zcat"
    

def check_jellyfish():
    '''
    Checks if jellyfish is installed. Raises an exception if not.
    '''
    try:
        subprocess.check_output("jellyfish --help", shell=True)
    except subprocess.CalledProcessError:
        raise Exception("Jellyfish not found! Please install Jellyfish to count kmers!")


def try_command(command: str, err_msg: str):
    '''
    Runs and command and if there's an error, raises an exception with the provided error message.
    '''
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"{err_msg}{e}")
    

def handle_config_jellyfish(k: int, file_paths: List[str]) -> dict:
    '''
    Reads a TOML file and runs the commands specified in the 'jellyfish_args' section.
    
    Returns a dictionary of the jellyfish arguments from the config file if parsing the jellyfish
    part of config file succeeds.

    Otherwise, returns None.
    '''

    config_file_path = "config.toml"
    config_keys_valid_options = ["-kmer_length", "-hash_size", "-threads", "-input_file_paths", "-output_file_path"]

    if not os.path.isfile(config_file_path):  
        return None
    
    # read the TOML file
    try:
        config = toml.load(config_file_path)
    except Exception as e:
        if type(e) == toml.TomlDecodeError:
            print("ERROR: Invalid TOML file. Please provide a valid TOML file.")
        exit(0)

    args = {}
    # check if the 'jellyfish_args' section exists
    if 'jellyfish_args' in config:
        jellyfish_args = config['jellyfish_args']
        
        # iterate through the jellyfish_args section of the config file
        for key, value in jellyfish_args.items():

            if key not in config_keys_valid_options:
                # ignore invalid keys but let the user know there was one in the file
                print(f"ERROR: Invalid key: '{key}' was found in the 'jellyfish_args' section of the config file.")
                exit(0)
            elif value != "" and value != None:
                # key and value are valid, add to args dictionary
                # TODO: possibly add validations for type of value it should be
                args[key] = value
        
        # if the required args are not present in the config file and valid, exit the program
        if ('-kmer_length' not in args) or ('-input_file_paths' not in args):

            if ('-kmer_length' not in args) and (k != None) and (k != "") and (k > 0):
                args['-kmer_length'] = k
            if ('-input_file_paths' not in args) and file_paths != None and file_paths != "":
                args['-input_file_paths'] = file_paths
            # k and file_paths are unacceptable values, and the required args are not present in the config file
            if ('-kmer_length' not in args) or ('-input_file_paths' not in args):
                print("ERROR: Kmer length and input file paths are required. Please provide a value for these keys.")
                exit(0)
        
        if (args['-kmer_length'] < 1):
            print("ERROR: Kmer length must be a positive integer.")
            exit(0)

        if (args['-input_file_paths'] == "") or (args['-input_file_paths'] == None):
            print("ERROR: Must provide at least one input file path.")
            exit(0)   
    else:
        # no 'jellyfish_args' section found in the config file
        return None
    
    return args


def fastq_to_kmer_counts(file_paths: List[str],
                         k: int,
                         output_dir: str = "",
                         threads: int = 10, 
                         hash_size: int = 100_000_000) -> str:
    '''
    Takes a path to a 'fastq' or zipped `fastq.gz' file and uses Jellyfish
    to count the provided number of kmers of length 'k'.

    Returns the local path to the output counts file.
    '''
    check_jellyfish()

    # Note that the config file will override the the arguments passed to this funcation
    parse_config_result = handle_config_jellyfish(k, file_paths)

    if parse_config_result != None:
        # use the values from the config file for the 
        k = parse_config_result['-kmer_length']
        file_paths = parse_config_result['-input_file_paths']

        # check if the other values are present in the config file, if not use default values
        if parse_config_result.get('-threads') != None:
            threads = parse_config_result['-threads']
        else:
            print("Threads not found in config file. Using default value of 10.")

        if parse_config_result.get("-hash_size") != None:
            hash_size = parse_config_result['-hash_size']
        else:
            print("Hash size not found in config file. Using default value of 100,000,000.")

        if parse_config_result.get("-output_file_path") != None:
            output_dir = parse_config_result['-output_file_path']
        else:
            print("Output file path not found in config file. Using default value of current directory.")

    # Use the accession number as the base name
    base_path = f"{output_dir}/{os.path.basename(file_paths[0].replace('_1', ''))}"

    # Modify the file extension to .jf for the output
    jf_file = base_path.replace('.fastq', f'_{k}.jf').replace('.gz', '')

    # The base command for kmer counting
    count_command = f"jellyfish count -m {k} -s {hash_size} -C -t {threads} -o {jf_file}"

    # modifies the base command depending on if the files are zipped or not
    if file_paths[0].endswith('.fastq.gz'):
        zcat_command = get_zcat_command()
        count_command = f"{zcat_command} {' '.join(file_paths)} | {count_command} /dev/fd/0"
    else:
        count_command = f"{count_command} {' '.join(file_paths)}"

    # Run count and dump jellyfish commands
    with create_progress_bar() as progress:
        task = progress.add_task(f"Counting {k}-mers...", total=None)

        try_command(count_command, err_msg="Error running Jellyfish count: ")

        counts_file = jf_file.replace(".jf", ".counts")
        dump_command = f"jellyfish dump -c {jf_file} > {counts_file}"

        try_command(dump_command, err_msg="Error running Jellyfish dump: ")
        progress.update(task, total=1, advance=1)
    
    return counts_file

def create_progress_bar() -> Progress:
    '''
    Returns a progress bar configured for k-mer counting progress.
    '''
    return Progress(prog.SpinnerColumn(),
                    prog.TextColumn("[progress.description]{task.description}"),
                    prog.BarColumn(),
                    prog.TimeElapsedColumn())