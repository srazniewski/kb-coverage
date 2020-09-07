# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:09:51 2020

@author: PRIYANKA
"""


from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import nltk
import re


question_word=["what","What","How","how","When","when","Where","where","Why","why","Which","which","who","Who"]
personal_pronoun=["I","i","you","You","your","Your","my","My"]
temporal_markers=["today","Today", "yesterday","Yesterday", "tomorrow","Tomorrow","last","Last","now","Now" ]



def truecasing_by_pos(text):
    """
    This function performs truecasing, i.e. 
    it capitalises words if their Part-of-Speech tag is NN or NNS.
    This function is required for a more precise NER function.
    """
    # tokenize the text into words
    words = nltk.word_tokenize(text)
    # apply POS-tagging on words
    tagged_words = nltk.pos_tag([word.lower() for word in words])
    # apply capitalization based on POS tags
    capitalized_words = [w.capitalize() if t in ["NN","NNS"] else w for (w,t) in tagged_words]
    # capitalize first word in sentence
    capitalized_words[0] = capitalized_words[0].capitalize()
    # join capitalized words
    text_truecase = re.sub(" (?=[\.,'!?:;])", "", ' '.join(capitalized_words))
    return text_truecase


def get_continuous_chunks(text):
    """
    This is a Named Entity Recognition (NER) function (Source: stackoverflow)
    with added feature of Truecasing
    """
    new_text=truecasing_by_pos(text)
    chunked = ne_chunk(pos_tag(word_tokenize(new_text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    if current_chunk:
        named_entity = " ".join(current_chunk)
        if named_entity not in continuous_chunk:
            continuous_chunk.append(named_entity)
            current_chunk = []
    return continuous_chunk

#txt = "Barack Obama is a great person and so is Michelle Obama." 
#print(get_continuous_chunks(txt))

def named_entity_filter(file_pointer, file_ner):
    """
    This function keeps all the queries containing named entities and rejects the rest
    from the given file
    """
    ner_list=[]
    count=0
    for line in file_pointer:
        ner_list=get_continuous_chunks(line)
        if ner_list:
            file_ner.write(line)
            count+=1
            
        else:
            continue
    return count


def how_to_can_filter(file_pointer, file_how):
    """
    This function filters out queries that contain the words like "how to"
    and "how can"
    """
    count=0
    line_list=[]
    for line in file_pointer:
        line_list=line.split()
        l=len(line_list)    
        for i in range(0,l,1):
                
            if line_list[i] == "How" or line_list[i] =="how":
                if line_list[i+1]=="can" or line_list[i+1]=="to":
                    
                    break
                else:
                    continue
        else:
            file_how.write(line)
            count+=1
        line_list=[]        
    return count        




def temporal_markers_filter(file_pointer, file_temporal):
    """
    This function filters out queries that contain temporal markers. The list of 
    temporal markers have been declared at the beginning of this program file
    """
    count=0
    for line in file_pointer:
            
        for word in line.split():
                
            if word in temporal_markers:
                break
        else:
            file_temporal.write(line)
            count+=1
                
    return count        




def personal_pronoun_filter(file_pointer, file_pronoun):
    """
    This function filters out queries that contain personal pronouns. The list of 
    personal pronouns have been declared at the beginning of this program file
    """
    count=0
    for line in file_pointer:
            
        for word in line.split():
                
            if word in personal_pronoun:
                break
        else:
            file_pronoun.write(line)
            count+=1
                
    return count        



def question_word_filter(file_pointer, file_question):
    """
    This function selects queries that contain question words and rejects the rest. The list of 
    question words have been declared at the beginning of this program file
    """
    count=0
    for line in file_pointer:
            
            
        for word in line.split():
                
            if word in question_word:
                    
                file_question.write(line)
                count+=1
                break
    return count               

def first_word_question(file_pointer, file_first_question):
    """
    This function selects queries that contain any of the question words as the 
    first word of the query and rejects the rest. The list of 
    question words have been declared at the beginning of this program file
    """
    count2=0
    for line in file_pointer:
        if line.split()[0] in question_word:
            file_first_question.write(line)
            count2+=1
    return count2

def query_counter(file_pointer):
    """
    This function counts the number of queries in a given file
    """
    count=0
    for line in file_pointer:
        count+=1
    return count


def filtered_output(name):
    """
    This function creates the filtered output files, based on various filters, 
    which are performed by calling the requisite functions
    
    """
    
    ''' keeping queries with only question words '''
    with open(name+"_query.txt", "r", encoding="utf-8") as file_pointer:
        with open(name+"_question_word.csv","w",encoding="utf-8") as file_question:
            count=question_word_filter(file_pointer,file_question)
            #print("No. of sentences with question word:",count )
            print("No. of sentences with question word:",count,file=file_result )
            
    ''' keeping queries with only first words as question words '''
    with open(name+"_question_word.csv", "r", encoding="utf-8") as file_pointer:
        with open(name+"_first_question_word.csv","w",encoding="utf-8") as file_first_question:
            count2=first_word_question(file_pointer, file_first_question)
            #print("No. of sentences with first word as question word:",count2)
            print("No. of sentences with first word as question word:",count2,file=file_result )
            
    ''' keeping queries that contain named entities '''
    with open(name+"_first_question_word.csv", "r", encoding="utf-8") as file_pointer:
        with open(name+"_named_entity.csv","w",encoding="utf-8") as file_ner:
            count=named_entity_filter(file_pointer, file_ner)
            #print("No. of sentences with named entities:",count )             
            print("No. of sentences with named entities:",count,file=file_result ) 
            
    ''' filtering out queries that contain temporal markers '''
    with open(name+"_named_entity.csv", "r", encoding="utf-8") as file_pointer:
        with open(name+"_temporal_markers.csv","w",encoding="utf-8") as file_temporal:
            count=temporal_markers_filter(file_pointer, file_temporal)
            #print("No. of sentences after removing temporal markers:",count )
            print("No. of sentences after removing temporal markers:",count,file=file_result )
    
    
    ''' filtering out queries that contain questions like 'how to..." and "how can ..." '''
    with open(name+"_temporal_markers.csv", "r", encoding="utf-8") as file_pointer:
        with open(name+"_how_to_can.csv","w",encoding="utf-8") as file_how:
            count=how_to_can_filter(file_pointer, file_how)
            #print("No. of sentences after removing how to/can:",count )       
            print("No. of sentences after removing how to/can:",count,file=file_result )         
            
    ''' filtering out queries that contain personal pronouns '''
    with open(name+"_how_to_can.csv", "r", encoding="utf-8") as file_pointer:
        with open(name+"_all_filtered.csv","w",encoding="utf-8") as file_pronoun:
            count=personal_pronoun_filter(file_pointer, file_pronoun)
            #print("No. of sentences after removing personal pronouns:",count )
            print("No. of sentences after removing personal pronouns:",count,file=file_result)

    ''' counting the number of queries left after applying all the filters in a cascading manner'''   
    with open(name+"_all_filtered.csv", "r", encoding="utf-8") as file_pointer:
        query_counts=query_counter(file_pointer)
        print("Total number of queries afer all filtering:",query_counts,file=file_result)
          
         
    

''' This file will have the output '''
with open("result_cascading.txt","w",encoding="utf-8") as file_result:
    
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    print("%%%%%%%%%%%%%%%%    MARCO DATA       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    filtered_output("marco")
   
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    print("%%%%%%%%%%%%%%%%    WEB DATA         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    filtered_output("web")
    
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    print("%%%%%%%%%%%%%%%%    AOL DATA         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",file=file_result)
    filtered_output("aol")
   
