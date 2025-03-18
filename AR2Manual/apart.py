import sys
import re

def process_heading(heading_text):
    heading_text = heading_text.strip()
    pattern = re.compile(r'^(\d+(?:\.\d+)*\.)\s+(.*)$')
    match = pattern.match(heading_text)
    if match:
        number_part = match.group(1).replace('.', '_')
        title_part = match.group(2).replace(' ', '_')
    else:
        number_part = ''
        title_part = heading_text.replace(' ', '_').replace('.', '_')
    filename = f"_{number_part}{title_part}.md"
    return filename

def main():
    if len(sys.argv) < 2:
        print("Usage: python apart.py file_name.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    current_section = []
    current_filename = None

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('# '):
            if current_filename is not None:
                with open(current_filename, 'w', encoding='utf-8') as f_out:
                    f_out.writelines(current_section)
                current_section = []
            
            heading_text = line[2:].strip()
            new_filename = process_heading(heading_text)
            current_filename = new_filename
            current_section.append(line)
        else:
            if current_filename is not None:
                current_section.append(line)
    
    if current_filename is not None and current_section:
        with open(current_filename, 'w', encoding='utf-8') as f_out:
            f_out.writelines(current_section)

if __name__ == "__main__":
    main()