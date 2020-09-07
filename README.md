# kb-coverage
Resources accompanying the paper "Structured knowledge: Have we made progress?  An extrinsic study of KB coverage over 19 years"
## Contents of the submission:
  1. aol_query.txt:                          text file containing queries from AOL
  2. marco_query.txt:                        text file containing queries ("marco" data)
  3. web_query.txt:                          text file containing queries ("web questions")
  4. query_filtering_cascaded.py:            python program to filter queries based on specific criteria 
  5. wiki_analysis.py:                       python program to analyse the wikipedia and wikidata entitty content based on revision dates
  6. mini_sample-input.csv:                  sample input file for "wiki_analysis.py" containing Wikidata Q-code entries
  7. README.md:                              this file
## Getting started:
The programs have been coded using Python 3. To run these one has to have Python 3 or above installed in their systems. Additionally you need the following packages to be         installed:
- nltk:		            To work with language data.
- re:		              To work with regular expressions.
- requests:		        To enable sending HTTP requests using python programs.
- csv:		              To create and work with csv files.
- collections.abc:     Provides a series of Abstract Base Classes for container interface.
- pandas:              To make operations for manipulating csv tables.
- datetime:            To work with dates as date objects.
The statements required to import these are included in the program, and so one does not need to explicitly write them while executing the programs.
## Running the program:
To execute the program from the command shell, do the following steps:
1. You need to make sure that you have the query files in the same folder from which you are trying to execute the programs.
2. To execute the program and generate the required results, type the following after the prompt appears:
 - (i)  python query_filtering_cascaded.py
 - (ii) python wiki_analysis.py 
### This will generate all the below mentioned files:
- Output of executing statement (i): This program will produce a file named "result_cascading.txt" that will contain all the statistics after the filters are applied to the respective query files. Apart from that it will also produce intermediate filtered versions of the query files namely (all filters are applied in a cascaded manner):
  - Files derived out of "marco_query.txt":
    - marco_question_word.csv: filtered file containing queries that contain question words
    - marco_first_question_word.csv: filtered file containing queries whose first word is a question word
    - marco_named_entity.csv: filtered file containing queries that contain named entities
    - marco_temporal_markers.csv: file containing queries such that temporal markers are filtered out
    - marco_how_to_can.csv: file containing queries such that queries of the form "how to..." and "how can..." are filtered out
    - marco_all_filtered.csv: file containing queries such that queries containing personal pronouns are filtered out
    
  Similary for the other query files, the following output files will be generated having similar meaning:
  - Files derived out of "web_query.txt":
     - web_question_word.csv
     - web_first_question_word.csv
     - web_named_entity.csv
     - web_temporal_markers.csv
     - web_how_to_can.csv
     - web_all_filtered.csv
  - Files derived out of "aol_query.txt":
     - aol_question_word.csv
     - aol_first_question_word.csv
     - aol_named_entity.csv
     - aol_temporal_markers.csv
     - aol_how_to_can.csv
     - aol_all_filtered.csv
 - The list of various question words, personal pronouns and temporal markers used for the above filtration are as follows:     
    - question_word=["what","What","How","how","When","when","Where","where","Why","why","Which","which","who","Who"]
    - personal_pronoun=["I","i","you","You","your","Your","my","My"]
    - temporal_markers=["today","Today", "yesterday","Yesterday", "tomorrow","Tomorrow","last","Last","now","Now" ]
   
   

- Output of executing statement (ii): This program will take input from a file that is specified by the variable "topicname" in the program (suppose that the input file is topicname.csv). It will likewise produce an outputfile named topicname_out.csv that contains the analysis. A sample input file is provided with this submission ("mini_sample-input.csv") which will thereby produce an output file named "mini_sample-input_out.csv".



