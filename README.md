# kb-coverage
Resources accompanying the paper "Structured knowledge: Have we made progress?  An extrinsic study of KB coverage over 19 years"
Contents of the submission:
  1. aol_query.txt:                          text file containing queries from AOL
  2. json_query.txt:                         text file containing queries ("marco" data)
  3. web_query.txt:                          text file containing queries ("web questions")
  4. query_filtering_cascaded.py:            python program 
  5. wiki_analysis.py:                       python program
Getting started:
  The programs have been coded using Python 3. To run these one has to have Python 3 or above installed in their systems. Additionally you need the following packages to be         installed:
		nltk:		            To work with language data.
		re:		              To work with regular expressions.
		requests:		        To enable sending HTTP requests using python programs.
		csv:		              To create and work with csv files.
    collections.abc:     Provides a series of Abstract Base Classes for container interface.
    pandas:              To make operations for manipulating csv tables.
    datetime:            To work with dates as date objects.
		
	The statements required to import these are included in the program, and so one does not need to explicitly write them while executing the programs.
  
Running the program:
	To execute the program from the command shell, do the following steps:
		1. You need to make sure that you have the query files in the same folder from which you are trying to execute the programs.
		2. To execute the program and generate the required results, type the following after the prompt appears:
                (i)  python query_filtering_cascaded.py
                (ii) python wiki_analysis.py 
	This will generate all the below mentioned files:
	      Output of executing statement (i):
		This program will produce a file named "result_cascading.txt" that will contain all the statistics after the filters are applied to the respective query files. apart from that it will also produce intermediate filtered versions of the query files. 	      
		Output of executing statement (ii):
		This program will take input from a file that is specified by the variable "topicname" in the program (suppose that the input file is topicname.csv). It will likewise           produce an outputfile named topicnmae_out.csv that contains the analysis. A sample input file is provided with this submission ("mini_sample-input.csv").



