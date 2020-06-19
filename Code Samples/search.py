#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  search.py
#  
#  Copyright 2018 Girishkumar <girishkumar@girishkumar-tcslab>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  



import os
import re
import logging
import codecs
import nltk
from nltk.corpus import stopwords as __sw
from nltk.corpus import wordnet as wn
from tqdm import tqdm
from nltk import corenlp
from nltk import word_tokenize
from nltk import sent_tokenize

from concordance import process as create_concordance


corenlp_parser = corenlp.CoreNLPParser('http://10.129.2.170:9000')

# In the next version, we should check list of stopwords as these words will not be indexed.
stopwords = __sw.words()

#logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


def get_filelist(path):
    '''Travese (recursively) the given directory (`path') and return 
    list of all files.
    '''

    filelist = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            filelist.append( file_path )

    return filelist


def tokenize(text):
    '''Tokenize the given text and return a list of tokens/words.'''
    words = re.findall(r"[\w']+", text) # \w is quivalent to [a-zA-Z0-9_]
    return words


def prepare_vocab(corpus_path='./raw_corpus/'):
    '''Extract list of uniq words from the corpus.'''

    V = set()
    filelist = get_filelist( corpus_path )

    logging.info('Preparing vocabulary from the corpus..')
    for filename in tqdm(filelist):
        with open( filename ) as ifile:
            text = ifile.read() 
            words = tokenize(text) # Replace this with proper text.tokenize()
            V = V.union( set(words) )

    return V


def derivationally_related_forms(w):
    '''Returns a set of derivationally related words of the given word `w'. '''
    syns = wn.synsets(w)
    result = [w]
    for syn in syns:
        for lemma in syn.lemmas():
            if lemma.name() == w: 
                for e in lemma.derivationally_related_forms():
                    result = result + [e.name(), e.synset().name().split('.')[0]]
    return set(result)
    

    
def extend_vocab(V):
    '''Given list/set of words, this function, returns an 'extended' 
    vocabulary.
    
        Extend(V) = Union_{w \in V} derivationally\_related\_forms(w)
    '''
    result = set()
    logging.info('Extending the given vocabulary..')
    for w in tqdm(V):
        result = result.union( derivationally_related_forms(w) )
        
    return result



def __replace_spl_tokens(word):
        '''
                function to replace special unicode words in corpus.
        '''
        if word == '-LRB-':
                return '('
        if word == '-RRB-':
                return ')'
        if word == '-LSB-':
            return '['
        if word == '-RSB-':
            return ']'
        return word


def imp(line):
    '''
    function to check if given line (from html extracted corpus) important or not.
    i.e. lines containing [Blank line , <doc....> , </doc> etc. ] are not important every other line in corpus is important
    important line then return 1; else return 0.
    '''
    
    line_ = line.strip()
    
    if not line:
        return False

    if line_.startswith('<doc') or line_.startswith('</doc>'):
        return False

    return True


def prepare_corpus_file(ifilename, ofilename):
    '''Transform the given input file to required format (plain text; one 
    sentence per line).
    
    We have considered using the following for tokenization (but, we have 
    used version-2 in final code):
    
    # version 1 : using regex to tokenize text into strings.
    #sentences = re.compile("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s").split(text)
    
    # version 2 : using nltk.sent_tokenize() to tokenize text into strings 
    #sentences = sent_tokenize(text)
    
    # version 3 :
    #tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    #sentences = tokenizer.tokenize(text)
    '''
    with open(ifilename) as ifile:
        lines = ifile.readlines()
        
        text = ''
        # filter unnecessory lines
        for line in lines:
            if imp(line):
                text = text + line
                        
        text = codecs.decode(text, 'utf8')
        sentences = sent_tokenize(text) # For different version, see the function documentation.
        
        with codecs.open(ofilename, 'w', encoding='utf-8'):
            
            for sentence in sentences:
                words = word_tokenize( sentence )
                words = map(__replace_spl_tokens, words)
                
                # Write the tokenized sentence into the refined corpus file
                ofile.write( ' '.join(words) )


def prepare_corpus(input_dir, output_dir='./corpus_sent_tokenized_3'):
    '''Process each document from the source directory and do the sentence
    tokenization. In the output directory, there will a file for each file in
    input directory with a sentence in each line.
    '''
    start_idx = len(input_dir)
    
    for root, dirs, filenames in tqdm(os.walk(input_dir)):
        for filename in filenames:
            
            print start_idx, root, filename
            o_root = root[start_idx:]
            
            if o_root and o_root[0] == os.path.sep:
                o_root = o_root[1:]
            
            if o_root:
                # If output directory doen't exist, create one
                o_path = os.path.join(output_dir, o_root)
                if not os.path.exists(o_path):
                    os.mkdir(o_path)
            else:
                o_path = output_dir
            
            ifile_path = os.path.join(root, filename)
            ofile_path = os.path.join(o_path, filename)

            print ifile_path, ofile_path
            prepare_corpus_file(ifile_path, ofile_path)
                        

def __prepare_index__(base_dir='./raw_corpus/', output_dir='./index/', vocab=None):
    '''Creates an index for searching. The index will be used for special 
    pattern matching. If `vocab' is given, than this will create index for 
    only words in the vocab.
    
    WE ARE NO MORE USING THIS PROCEDURE FOR INDEXING.
    NOW, WE ARE PREPARING INDEX USING concordance.py FILE.
    
    The index will have the following format:
        (SHOULD WE STORED THIS DATA IN JSON FORMAT???)
        * For each word `w', there will be a file named `w'
        * In `w' file, each line contains following: name of a file (followed 
          by list of sentence numbers) in which the word is present.
        * There will be a seperate file for each word considered at a surface
          level. For instance, there will a file for `student' and a file for
          `students'.
          
    In sideline, this function also extract NOUN+NOUN sequences.
    
    Parameters
    ---------
    base_dir: str (default: './raw_corpus/')
        Name of a directory where a raw corpus (mostly wikepedia dump) is 
        stored.
    output_dir: str (default: './index/')
        Name of a directory where index files will be stored.
    vocab: list/set (default: None)
        Vocabulary. Index will we created for only these words. By default, 
        index will be created for all words.
    '''

    # For each word, there will a file in index
    idx_file_dict = {}

    data_filelist = get_filelist( base_dir ) # Get list of all files in the corpus directory.
    data_filelist.sort()                     # Sort it for same ordering across the multiple runs
    with open(os.path.join(output_dir, '___all_data_files___'), 'w') as ofile: # Write the list to a special file
        ofile.write( '\n'.join(data_filelist) )

    # Traverse (recursively) throught each file `f'
    for data_file_no, data_filename in enumerate(data_filelist):
        with open(data_filename, 'r') as ifile: 
            
            # For each sentence (Assuming each line contains a sentence)
            for line_no, line in enumerate( ifile ):
                
                # For each word `w' in sentence
                words = tokenize( line ) # \w is quivalent to [a-zA-Z0-9_]
                for word in words:

                    if word in stopwords: # Not index the stopwords
                        continue
                    
                    # If vocab is given AND
                    #    the word is not in the vocab
                    # then
                    #    don't index those words
                    if vocab and word not in vocab:
                        continue

                    idx_filename = os.path.join(output_dir, word)

                    # if a file for thw word `w' does NOT exist
                    if idx_filename not in idx_file_dict:
                        # create a file with name `w' (in output_dir)
                        idx_file_dict[ word ] = open(idx_filename,  'w')

                    ''' AS OF NOW, WE ARE NOT DOING THIS.
                    # if name(`f') NOT in file-w
                        # Put an entry of the file-f in file-w with sentence number
                    # Else:
                        # Update the entry with the sentence number
                    '''

                    # Put an entry with (file_id, line_no) in a index file.
                    idx_file_dict[ word ].write('%d\t%d\n' % (data_file_no, line_no))
    
                # WE ARE NOT DOING THIS AS OF NOW.
                # Check for noun+noun sequence
                    # If it is, store it with meaningfull information.
                    
    for key, val in idx_file_dict.iteritems():
        val.close()
        

def _prepare_index(filelist, output_dir='./index/', vocab=None, all_data_files=None, part=None):
    '''Prepare index (in concordance format) for the given corpus.'''
    
    if part:
        output_dir = os.path.join(output_dir, str(part))
        if not os.path.exists(output_dir):
            os.mkdir( output_dir )
    
    for ifilename in filelist:
        conc_dict = create_concordance(filename)
        for word in conc_dict:
            ofilename = os.path.join(output_dir, word)
            with codecs.open(ofilename, 'a', encoding='utf-8') as ofile:
                ofile.write( '%d\t' % all_data_files.index(ifilename) )
                ofile.write( '\t'.join(map(str, conc_dict[word])) )
                ofile.write( '\n' )



def prepare_index(base_dir='./raw_corpus/', output_dir='./index/', vocab=None):
    '''Prepare index (in concordance format) for the given corpus.'''
    
    filelist = get_filelist(base_dir)
    
    with open(os.path.join(output_dir, '___all_data_files___'), 'r') as ifile: # Write the list to a special file
        data_filelist = ifile.readlines()
        data_filelist = map(lambda x: x.strip(), data_filelist)
    
    # Instead of preparing an index in one shot, split the filelist into k (say 20) partitions,
    # and call the following function on each partition in parallel
    
    #k = 20
    #p = Pool(k)
    #p.map(
    
    _prepare_index(filelist, output_dir, vocab, all_data_files=data_filelist)



def search_nc(w1, w2, index_dir='./index/'):
    '''Extract a sentences for a given noun compound (w1, w2) using the index 
    (stored in `index_dir').
    
    Followings are additional constaints on the search results:
        * ...
        * ...
    
    Parameters
    ----------
    w1:http://www.os.walk/
    
    w2:
    
    
    Returns
    -------
    list: A list of sentences with w1 and w2 with the predefined pattern.
    '''
    
    # Extract sentences with `w1' => set_w1
    # Extract sentences with `w1' => set_w2
    
    # Take intersection of set_w1 and set_w2 => set_w
    
    # For each sentence in set_w
        # apply necessory constains
        # ..and create a result set => `sents'
        
    # return `sents'
    
    pass


if __name__ == '__main__':


    prepare_corpus('../../Downloads/out/AA')
    #prepare_corpus('./raw_corpus_')
    
    if False:
        V = prepare_vocab()
        extV = extend_vocab(V)

        output_dir = './index/'

        with open(os.path.join(output_dir, '___vocab___'), 'w') as ofile: # Write the vocab to a special file
            V_ = list(V)
            V_.sort()
            ofile.write( '\n'.join(V_) )
            
        with open(os.path.join(output_dir, '___extended_vocab___'), 'w') as ofile: # Write the extended vocab to a special file
            extV_ = list(extV)
            extV_.sort()
            ofile.write( '\n'.join(extV_) )

    
    #prepare_index()
