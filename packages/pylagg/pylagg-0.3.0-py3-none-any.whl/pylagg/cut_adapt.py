from cutadapt.cli import main
import os
import toml

def trim(input_file: str,config: dict):

    

    command = []  # Initialize an empty list to hold the commands

     
    arguments = config['cutadapt']
    
    # Iterate through each key and its associated list
    for key, value in arguments.items():
        if isinstance(value, list):
            for item in value:
                command.append(f"{key}")

                # Only append the item if it's not an empty string
                if item:
                    command.append(f"{item}")
        else:
            # Append the key
            command.append(f"{key}")

            # Check if value is not an empty list or empty string and append it
            if value not in ["", []]:
                command.append(f"{value}")
    
    if '-o' not in command:
        # Automatically generate the output file name by adding "_trimmed" before the extension
       
        name, ext = os.path.splitext(input_file)
        name, second_ext = os.path.splitext(name)
        output_file= f"{name}_trimmed{second_ext}{ext}"
        command.append('-o')
        out_dir = config.get('Files', {}).get('output',None)


        if out_dir != None:
            output_file =os.path.join(out_dir,output_file)
            command.append(output_file)
        else:
            command.append(output_file)

 
    command.append(input_file)

    print(f"Running command: {' '.join(command)}\n")
    main(command)

    return output_file
    