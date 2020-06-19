#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  features.py
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


def nc_feature_extraction(arg1 , arg2):
    """Extract the feature-set from noun compound for representing in vector 
    form in later phase and to use it in learning phase.
    
    Parameters
    ----------
    arg1 : str
        Head Noun String
    arg2 : str
        Modifier Noun String
        
    Returns
    -------
    vector : list
        feature-set vector of Noun Compound.
    """
    
    # 2.1.1 Word embedding of w1 and w2 
    
    
    # 2.1.2 Candidate preposition for prepositional paraphrasing : finding appropriate preposition for noun compound using Netspeak.
    
    
    # 2.1.3 Candidate verb for verb+prep paraphrasing
    
    
    pass



def sent_feature_extraction(w1, w2, sentences):
    '''Extract the feature-set from noun compound & given sentence for 
    representing in vector form in later phase for learning. 
    
    Parameters
    ----------
    
    arg1: str
        Head Noun String
    arg2 : str
        Modifier Noun String
    arg3 : vector<str>       
        sentences extracted from large corpus.
           
    Returns
    -------
    vector
        feature-set from given sentences.
    
    '''
    
    for sentence in sentences:
    
        # Get dependecy parsing, POS tagging, and parsing from CoreNLP
        
        # Get SRL from SENNA : semantic role labeling
        
        # 2.2.1  Find common ancestor: getting common ancestor of modifier and head noun from parsing tree.
        # dep(w_c, w_1) : dependancy between common ancestor and modifier
        # dep(w_c, w_2) : dependancy between common ancestor and head
        
        # 2.2.2 Get list of all verbs
        
        
        # 2.2.3 POS tags: w1, w2, ...
        
        
        # 2.2.4 SRL for w1 and w2 (w.r.t. the w_c)
        
        
        # 2.2.5 Other features
        # 
        #
        
        pass
    
    pass
    
    
def feature_extraction( nc ):
    '''
        Base function for extracting feature from noun compound and sentences.
        
        Parameters
        ----------
        
        arg1 : str
               Head Noun String
        arg2 : str
               Modifier Noun String
               
        
        Returns
        -------
        
        vector 
              feature-set vector of Noun Compound & sentences extracted.
        
    '''
    
    # 2.1 Extract NC level features : call_nc_feature_extraction( nc )
    
    
    # 2.2 Extract sentence level features : call_sent_feature_extraction(w1, w2, sentences)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
