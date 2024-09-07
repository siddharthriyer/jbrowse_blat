import csv
import requests
import webbrowser
import os

# UCSC BLAT URL for programmatic access with JSON output
BLAT_URL = "https://genome.ucsc.edu/cgi-bin/hgBlat"

# JBrowse2 configuration (update these paths based on your setup)
JBROWSE_URL = "http://localhost:3000/?config=config.json"
ASSEMBLY_NAME = "grch38_compressed.fna"  # Update with your default assembly name

# Function to submit BLAT query and retrieve JSON results
def query_blat(query_sequence, genome="hg38", query_type="DNA"):
    # Submit the GET request to the UCSC BLAT server
    url = BLAT_URL.format(query_sequence)

    # Send HTTP GET request to the URL
    response = requests.get(url)
    
    # If response is successful, return the JSON data
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying BLAT for sequence {query_sequence[:30]}: {response.status_code}")
        return None

# Function to parse BLAT JSON results and generate JBrowse2 links
def parse_blat_results(blat_json):
    links = []

    # Ensure 'blat' and 'fields' are present in the JSON response
    if 'blat' in blat_json and 'fields' in blat_json:
        fields = blat_json['fields']
        blat_results = blat_json['blat']

        # Extract relevant fields for each alignment
        for result in blat_results:
            # Create a dictionary for each result with field names as keys
            result_dict = dict(zip(fields, result))
            
            # Extract the query name, target name (chromosome), start, and end positions
            query_name = result_dict['qName']
            target_name = result_dict['tName']  # Chromosome name
            alignment_start = result_dict['tStart']  # Start position
            alignment_end = result_dict['tEnd']  # End position

            # Calculate percentage identity if possible
            matches = result_dict['matches']
            mismatches = result_dict['misMatches']
            total_bases = matches + mismatches
            if total_bases > 0:
                perc_identity = (matches / total_bases) * 100
            else:
                perc_identity = 0

            # Create JBrowse2 URL
            jbrowse_link = f"{JBROWSE_URL}&assembly={ASSEMBLY_NAME}&loc={target_name}:{alignment_start}..{alignment_end}"
            link_text = f"{query_name} aligned to {target_name}:{alignment_start}-{alignment_end} (Identity: {perc_identity:.2f}%)"
            links.append((jbrowse_link, link_text))
    else:
        print("No BLAT results found or invalid JSON format.")
    
    return links

# Function to create an HTML file with sections for each sequence's results
def generate_html(sections, output_file="blat_jbrowse_links.html"):
    with open(output_file, "w") as f:
        f.write("<html><body>\n")
        f.write("<h1>BLAT Results and JBrowse2 Links</h1>\n")
        
        # Iterate over each section (sequence) and its corresponding links
        for seq_name, links in sections.items():
            f.write(f"<h2>Results for sequence: {seq_name}</h2>\n")
            f.write("<ul>\n")
            for link, text in links:
                f.write(f'<li><a href="{link}" target="_blank">{text}</a></li>\n')
            f.write("</ul>\n")
        
        f.write("</body></html>\n")
    
    print(f"HTML file '{output_file}' generated successfully.")
    return output_file

# Function to open the HTML file in the default web browser
def open_in_browser(html_file):
    webbrowser.open(f"file://{os.path.realpath(html_file)}")

# Function to read sequences from a CSV file
def read_sequences_from_csv(csv_file):
    sequences = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sequences.append(row[0])  # Assuming each row contains one sequence in the first column
    return sequences

# Main function to run the entire workflow
def main():
    csv_file = input("Enter the path to the CSV file containing the sequences: ")
    sequences = read_sequences_from_csv(csv_file)

    sections = {}
    
    # Step 1: Query BLAT for each sequence
    for seq in sequences:
        seq_name = seq[:30]  # Use the first 30 characters of the sequence as its name
        print(f"Submitting query to BLAT for sequence: {seq_name}...")
        blat_json = query_blat(seq)

        # Step 2: Parse BLAT results
        if blat_json:
            print("Parsing BLAT results...")
            links = parse_blat_results(blat_json)
            sections[seq_name] = links  # Store the links in the section for this sequence
        else:
            print(f"Failed to retrieve BLAT results for sequence: {seq_name}.")

    # Step 3: Generate HTML with JBrowse2 links
    if sections:
        html_file = generate_html(sections)

        # Step 4: Open HTML file in browser
        print("Opening results in the default web browser...")
        open_in_browser(html_file)
    else:
        print("No links generated. Exiting.")

if __name__ == "__main__":
    main()