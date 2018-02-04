#!/usr/local/bin/python3

import mysql.connector
from Bio import SeqIO
from Bio.SeqUtils import GC
import json
import sys

def main():

	input_file = sys.argv[1]

	# Keep track of ID
	db_id = 0
	dbxref_id = 0
	organism_id = 0
	feature_id = 0
	featureloc_id = 0
	featureprop_id = 0
	organism_id = 0

	# Reads in one genome in the file
	record = SeqIO.read(input_file, "genbank")

	# Chado varibles
	# db table variables
	db_id += 1
	annotation_provider = '-'
	url = '-'
	# dbxref table variables
	dbxref_id += 1
	accession = record.name
	version = record.id
	# feature table variables
	uniquename = '-'
	residues = '-'
	seqlen = 0
	gc = 0
	feature_table = []
	# featureloc table variables
	fmin = 0
	fmax = 0
	strand = 0
	featureloc_table = []
	# featureprop table variables
	value = '-'
	translation = '-'
	translationlen = 0
	featureprop_table = []
	# organism table variables
	organism_id += 1
	genus = '-'
	species = '-'
	common_name = '-'
	organism = record.annotations['organism']

	# Obtains annotation provider and url
	structured_comment_ordereddict = record.annotations["structured_comment"]
	structured_comment_dict = json.loads(json.dumps(structured_comment_ordereddict))
	if 'Annotation Provider' in structured_comment_dict['Genome-Annotation-Data']:
		annotation_provider = structured_comment_dict['Genome-Annotation-Data']['Annotation Provider']
	if 'URL' in structured_comment_dict['Genome-Annotation-Data']:
		url = structured_comment_dict['Genome-Annotation-Data']['URL']

	# Obtains organism's genus and species
	for annotation in organism:
		common_name = record.annotations['organism']
		temp = record.annotations['organism'].split(' ')
		genus = temp[0]
		species = ' '.join(temp[1:])

	# Obtains the variables in the feature, featureloc, and featureprop tables
	for feature in record.features:

		# Temporary feature variables
		feature_temp_data = []
		# Tempary featureloc variables
		featureloc_temp_data = []
		# Tempary featureloc variables
		featureprop_temp_data = []

		# Only looks for CDS features to get the proteins
		if feature.type == "CDS":

			# Increment IDs for each protein found
			feature_id += 1
			featureloc_id += 1
			featureprop_id += 1

			# Obtains the nucleotide sequence for the protein
			residues = feature.extract(record.seq)

			# Obtains the locations of the nucleotide sequence
			location = feature.location
			fmin = location.start.position
			fmax = location.end.position
			strand = feature.strand

			# Verify that there is a real locus tag
			if 'locus_tag' in feature.qualifiers:
				uniquename = feature.qualifiers['locus_tag'][0]

			# Verify that there is a real protein
			if 'product' in feature.qualifiers:
				value = feature.qualifiers['product'][0]
				
			# Verify that there is a translation sequence
			if 'translation' in feature.qualifiers:
				translation = feature.qualifiers['translation'][0]
				# Translated sequence length
				translationlen = len(translation)

			# Verify that there is a nucleotide sequnce
			if residues != '':
				residues = str(residues)
				# Nucelotide sequence length
				seqlen = len(residues)
				# Calcualtes GC content
				gc = GC(residues)

			# Feature variables			
			feature_temp_data.append(feature_id)
			feature_temp_data.append(dbxref_id)
			feature_temp_data.append(organism_id)
			feature_temp_data.append(uniquename)
			feature_temp_data.append(residues)
			feature_temp_data.append(seqlen)
			feature_temp_data.append(gc)
			# Featureloc variables
			featureloc_temp_data.append(featureloc_id)
			featureloc_temp_data.append(feature_id)
			featureloc_temp_data.append(fmin)
			featureloc_temp_data.append(fmax)
			featureloc_temp_data.append(strand)
			# Featureprop variables
			featureprop_temp_data.append(featureprop_id)
			featureprop_temp_data.append(feature_id)
			featureprop_temp_data.append(value)
			featureprop_temp_data.append(translation)
			featureprop_temp_data.append(translationlen)

			# Add all the variables to feature table
			feature_table.append(feature_temp_data)
			# Add all the variables to featureloc table
			featureloc_table.append(featureloc_temp_data)
			# Add all the variables to featureprop table
			featureprop_table.append(featureprop_temp_data)

	conn = mysql.connector.connect(user='evogel5', password='password', host='localhost', database='evogel5')

	cursor = conn.cursor()

	# If the table already exists delete
	cursor.execute("""drop table if exists db""")
	cursor.execute("""drop table if exists dbxref""")
	cursor.execute("""drop table if exists feature""")
	cursor.execute("""drop table if exists featureloc""")
	cursor.execute("""drop table if exists featureprop""")
	cursor.execute("""drop table if exists organism""")

	conn.commit()

	# Create all the chado tables that will be used
	cursor.execute("""create table db (
		db_id int(11) primary key not NULL,
		name varchar(50) not NULL,
		url varchar(255))""")
	cursor.execute("""create table dbxref (
		dbxref_id int(11) primary key not NULL,
		db_id int(11) not NULL,
		accession varchar(255) not NULL,
		version varchar(50) not NULL)""")
	cursor.execute("""create table feature (
		feature_id int(11) primary key not NULL,
		dbxref_id int(11),
		organism_id int(11) not NULL,
		uniquename varchar(255) not NULL,
		residues longtext,
		seqlen int(11),
		gc decimal(10,3))""")
	cursor.execute("""create table featureloc (
		featureloc_id int(11) primary key not NULL,
		feature_id int(11) not NULL,
		fmin int(11),
		fmax int(11),
		strand smallint(6))""")
	cursor.execute("""create table featureprop (
		featureprop_id int(11) primary key not NULL,
		feature_id int(11) not NULL,
		value varchar(2000) not NULL,
		translation longtext,
		translationlen int(11))""")
	cursor.execute("""create table organism (
		organism_id int(11) primary key not NULL,
		genus varchar(255) not NULL,
		species varchar(255) not NULL,
		common_name varchar(255))""")

	# Insert the variables into the chado tables
	qry = "insert into db values (%s, %s, %s)"
	cursor.execute(qry, (db_id, annotation_provider, url))

	qry = "insert into dbxref values (%s, %s, %s, %s)"
	cursor.execute(qry, (dbxref_id, db_id, accession, version))

	for item in feature_table:
		qry = "insert into feature values (%s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(qry, (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))

	for item in featureloc_table:
		qry = "insert into featureloc values (%s, %s, %s, %s, %s)"
		cursor.execute(qry, (item[0], item[1], item[2], item[3], item[4]))

	for item in featureprop_table:
		qry = "insert into featureprop values (%s, %s, %s, %s, %s)"
		cursor.execute(qry, (item[0], item[1], item[2], item[3], item[4]))

	qry = "insert into organism values (%s, %s, %s, %s)"
	cursor.execute(qry, (organism_id, genus, species, common_name))

	conn.commit()
	cursor.close()

if __name__ == '__main__':
    main()