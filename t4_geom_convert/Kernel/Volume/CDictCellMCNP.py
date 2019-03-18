# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 February 2019
:file : CDictCellMCNP.py
'''
from _collections_abc import MutableMapping
from ..FileHanlders.Parser.CParseMCNPCell import CParseMCNPCell


class CDictCellMCNP(MutableMapping):
    '''
    :brief: Class inheriting of abstract class MutableMapping and listing
    cell from MCNP
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.d_cellMCNP = dict()
        self.d_cellMCNP = CParseMCNPCell().m_parsingCell()

    def __getitem__(self, key):
        return self.d_cellMCNP[key]

    def __setitem__(self, key, value):
        self.d_cellMCNP[key] = value

    def __delitem__(self, key):
        del self.d_cellMCNP[key]

    def __iter__(self):
        return iter(self.d_cellMCNP)

    def __len__(self):
        return len(self.d_cellMCNP)

    def __repr__(self):
        return self.d_cellMCNP.__repr__()

# for key,val in CDictCellMCNP().d_cellMCNP.items() :
#     l = val.m_evaluateASTMCNP().split(')')
#     #l = l[0].split('(')
#     print(key, re.findall('\d+','(((((-1 * -2'))

    def __repr__(self):
        return self.d_cellMCNP.__repr__()
    
    
# for key,val in CDictCellMCNP().d_cellMCNP.items() :
#     l = val.m_evaluateASTMCNP().split(')')
#     #l = l[0].split('(')
#     print(key, re.findall('\d+','(((((-1 * -2'))
    
    