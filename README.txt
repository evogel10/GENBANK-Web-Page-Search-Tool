* ABOUT *

Web-based bioinformatics analysis application for consolidating a Genbank 
file into a searchable look up for gene products and associated 
characterstics.

Source code can be obtained here:

http://bfx.eng.jhu.edu/evogel5/Final/evogel5_final.tar.gz

Utilize tool here:

http://bfx.eng.jhu.edu/evogel5/Final/final.html

* REQUIREMENTS *

Python 2.6.6

Biopyton 1.69

mysql  Ver 14.14 Distrib 5.1.73, for redhat-linux-gnu (x86_64) using 
readline 5.1

Storage for Genbank files. Storage size will depend on content of file. 
Two example files included range from 1 to 6 MB.

* DETAILED USAGE *

1. Go to project page at http://bfx.eng.jhu.edu/evogel5/Final/final.html.

2. Enter a protein product you would like to search for from the Genbank 
file.

	2a. Currently Saccharomyces cerevisiae S288c chromosome X, complete 
	sequence, is loaded into the database as the Genbank file. The 
	directory contains another Genbank file for Staphylococcus schleiferi 
	strain 5909-02, complete genome. If you wish to change the Genbank 
	file to search use the following command in the terminal directory 
	the files are located:

	./final_chado_database.py Filename

3. Once the search results return with the protein(s) you will be able to 
see the database, url, accession number, accession version, genus, species, 
and common name of the organism the protein(s) is/are from. You may also 
click on the collapsible boxes to view the uniquename, residue, residue length, 
GC content, start and end of the sequence, strand the sequence is on, protein 
product name, translation sequence, and translation length.

4. You may now search another protein or use the data acquired to search in 
the links provided to NCBI, BLAST, UniProt, EMBL, or USUC.