import argparse
import os



def fixFile(file_path, outdir):
    with open(file_path, 'r') as f_in:
        lines = f_in.readlines()

    processed_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i]
        
        # Check if the current line starts with 'ATOM' or 'HETATM'
        if current_line.startswith(('ATOM', 'HETATM')):
            # Look at the next line if it exists
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # Check if the next line starts with '1'
                if next_line.strip().startswith('1'):
                    # Concatenate the two lines, removing the newline from the first
                    processed_line = current_line.strip() + " " + next_line
                    processed_lines.append(processed_line)
                    i += 2  # Skip the next line as it's already processed
                else:
                    # No match, so just append the current line
                    processed_lines.append(current_line)
                    i += 1
            else:
                # Last line of the file, so just append it
                processed_lines.append(current_line)
                i += 1
        else:
            # The line doesn't start with 'ATOM' or 'HETATM', so append it as is
            processed_lines.append(current_line)
            i += 1

    # Write the modified content back to the file
    with open(outdir + file_path.split("/")[-1], 'w') as f_out:
        f_out.writelines(processed_lines)

    print(f"File '{file_path}' has been processed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcedir", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    
    for file in os.listdir(args.sourcedir):
        fixFile(args.sourcedir + file, args.outdir)