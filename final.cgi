#!/usr/local/bin/python3

import mysql.connector
import cgi
import json

def main():
	print("Content-Type: application/json\n\n")
	form = cgi.FieldStorage()
	term = form.getvalue('search_term')


	# Connect to MySQL database to store information
	conn = mysql.connector.connect(user='evogel5', password='password', host='localhost', database='evogel5')
    
	cursor = conn.cursor()

	# Query the protein qualities
	qry = """
	SELECT f.uniquename, f.residues, f.seqlen, f.gc, floc.fmin, floc.fmax, floc.strand, fprop.value, fprop.translation, fprop.translationlen
	FROM feature f 
	JOIN featureloc floc ON f.feature_id = floc.feature_id
	JOIN featureprop fprop ON f.feature_id = fprop.feature_id
	WHERE fprop.value LIKE %s;
	"""
	cursor.execute(qry, ('%' + term + '%', ))

	# Data structure to hold information about genbank file and protein
	results = { 'match_count': 0, 'matches': list(), 'match_name': '', 'match_url': '', 'match_accession': '', 'match_version': '', 'match_genus': '', 'match_species': '', 'match_common_name': ''}
	
	# Add protein information to results
	for (uniquename, residues, seqlen, gc, fmin, fmax, strand, value, translation, translationlen) in cursor:
		results['matches'].append({'uniquename': uniquename, 'residues': residues, 'seqlen': seqlen, 'gc': float(gc), 'fmin': fmin, 'fmax': fmax, 'strand': strand, 'value': value, 'translation': translation, 'translationlen': translationlen})
		results['match_count'] += 1

	# Query informition on genbank file
	qry = """
	SELECT db.name, db.url, dbxref.accession, dbxref.version, o.genus, o.species, o.common_name
	FROM feature f
	JOIN dbxref ON f.dbxref_id = dbxref.dbxref_id
	JOIN db ON dbxref.db_id = db.db_id
	JOIN organism o ON f.organism_id = o.organism_id
	JOIN featureprop fprop ON f.feature_id = fprop.feature_id
	WHERE fprop.value LIKE %s;
	"""
	cursor.execute(qry, ('%' + term + '%', ))

	# Add genbank information to results
	for (db_name, url, accession, version, genus, species, common_name) in cursor:
		# Turns tuple into string
		results['match_name'] = ''.join(db_name)
		results['match_url'] = ''.join(url)
		results['match_accession'] = ''.join(accession)
		results['match_version'] = ''.join(version)
		results['match_genus'] = ''.join(genus)
		results['match_species'] = ''.join(species)
		results['match_common_name'] = ''.join(common_name)

	# Close connection to server
	conn.close()

	# Pass resutls as a JSON object to JavaScript file
	print(json.dumps(results))

if __name__ == '__main__':
	main()