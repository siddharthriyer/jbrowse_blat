# jbrowse_blat
Code and instructions for using locally hosted JBrowse2 and finding regions by web-based blat query

# Instructions

I have detailed instructions below for setting up the necessary software on a completely fresh Mac or Linux. If you already have a given software package you can skip those steps.

1. Open Terminal or the shell, and install HomeBrew.

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Install python, wget, npm, and samtools with Homebrew.

        brew install python wget npm samtools

3. Install BeautifulSoup4 and requests for python.

        pip install beautifulsoup4 requests

4. Install npx and jbrowse command line tools.

        npm install npx
        npm install -g @jbrowse/cli

5. Make a folder called genome_viewing. Navigate to this folder in terminal (replace /path/to/genome_viewing with the real path, and install JBrowse 2.
       

        mkdir genome_viewing && cd genome_viewing
        jbrowse create jbrowse2

7. Install and set up the human genome (GrCh38 in this example) with annotations (GenCode v46).

        cd jbrowse2
        wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
        gunzip GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
        mv GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz grch38_compressed.fna
        samtools faidx grch38_compressed.fna
        mkdir tracks && cd tracks
        wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_46/gencode.v46.annotation.gff3.gz
        gunzip gencode.v46.annotation.gff3.gz
        

8. Download the config.json file in this repository to the jbrowse2 folder. Download the python files in this repository to the genome_viewing folder.
9. At this point, confirm that JBrowse2 is functional by running the following code. Open the link to the server (https://localhost:3000) in your browser, click "linear genome view", and click "open track selector" after selecting a chromosome. You should see options to view the reference sequence and the GenCode annotations. If any of these steps doesn't work, something has gone wrong.

        cd /path/to/genome_viewing/jbrowse2
        npx serve .

10. Change directories to the genome_viewing folder and run the python script. Enter your query sequence when prompted, and it should open an HTML file in your default browser with links to the locations of the resulting hit locations.

        cd /path/to/genome_viewing/
        python web_blat_single.py

If you have any questions or concerns, contact Siddharth Iyer (iyers@mit.edu).
