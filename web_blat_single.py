import requests
import webbrowser
import os
import json

# UCSC BLAT URL for programmatic access with JSON output
BLAT_URL = "https://genome.ucsc.edu/cgi-bin/hgBlat?userSeq={}&type=DNA&db=hg38&output=json"

# JBrowse2 configuration (update these paths based on your setup)
JBROWSE_URL = "http://localhost:3000/?config=config.json"
ASSEMBLY_NAME = "grch38_compressed.fna"  # Update with your default assembly name

# Function to submit BLAT query and retrieve JSON results
def query_blat(query_sequence, genome="hg38", query_type="DNA"):
    # params = {
    #     "userSeq": query_sequence,
    #     "type": query_type,
    #     "db": genome,
    #     "output": "json"
    # }

    
    # Submit the GET request to the UCSC BLAT server
    url = BLAT_URL.format(query_sequence)

    # Send HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content to a file
        with open("file.json", "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file. HTTP Status Code: {response.status_code}")

    # response = requests.get(BLAT_URL, params=params)
    
    # If response is successful, return the JSON data
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error querying BLAT: {response.status_code}")
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

# Function to create an HTML file with links for JBrowse2
def generate_html(links, output_file="blat_jbrowse_links.html"):
    with open(output_file, "w") as f:
        f.write("<html><body>\n")
        f.write("<h2>BLAT Results and JBrowse2 Links</h2>\n")
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

# Main function to run the entire workflow
def main():
    query_sequence = input("Enter the query sequence: ")

    # Step 1: Query BLAT
    print("Submitting query to BLAT...")
    blat_json = query_blat(query_sequence)

    # Step 2: Parse BLAT results
    if blat_json:
        print("Parsing BLAT results...")
        links = parse_blat_results(blat_json)

        # Step 3: Generate HTML with JBrowse2 links
        if links:
            html_file = generate_html(links)

            # Step 4: Open HTML file in browser
            print("Opening results in the default web browser...")
            open_in_browser(html_file)
        else:
            print("No links generated. Exiting.")
    else:
        print("Failed to retrieve BLAT results.")

if __name__ == "__main__":
    main()