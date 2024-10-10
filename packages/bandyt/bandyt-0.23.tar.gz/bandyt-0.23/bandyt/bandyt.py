#//=============================================================
#//(c) 2011 Distributed under MIT-style license. 
#//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
#//=============================================================


import numpy as np
import random
import csv
import os
import time
from itertools import product
import matplotlib.pyplot as plt
import itertools as itools
import textwrap as tw
from copy import deepcopy
import multiprocessing as mp
from functools import reduce
from functools import partial
import multiprocessing
import pandas as pd
import pydot
import igraph as ig
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.patches import Wedge
from matplotlib.patches import Arc

__all__ = ['search', 'bnet', 'cext', 'dataset', 'bdm', 'bnetload', 'check_type', 'cond_normal', 'conditional_sampl', 'continuous_sampler','conv','conv_col','conv_row','cpt',
           'downstream_sampler', 'downstream_sampler1', 'factor_indx', 'factor_str', 'joint_prob', 'loader', 'make_A', 'mdl', 'mu', 'random_adjmat', 'random_dist',
           'test','upstream_sampler', 'read_input_file','getContact2discret', 'runParallel', 'datawrite', 'read_tsv', 'Residue', 
           'transformRes', 'get_unique_pair', 'get_trj_s', 'get_traj_p', 'remove_Neighbors',  'getGraphProp', 'load_graph',
           'is_valid_node', 'create_adjacency_matrix', 'calculate_hamming_distance_between_graphs', 'calculate_hamming_distances_per_node',
           'convert_bn_to_igraph', 'plot_hamming_distances']

def bnetload(structure):
    """ structure can be a csv file or and adjacency matrix """
    if type(structure)==np.ndarray:
        bn=bnet(np.arange(structure.shape[1]))
        pnodes=[np.where(p>0)[0].tolist() for p in structure]
    else:
        lst=[row for row in csv.reader(open(structure,'r'))]
        bn=bnet([row[0] for row in lst])
        pnodes=[[int(i) for i in row[1:]] if len(row)>1 else [] for row in lst]
    for c,pset in enumerate(pnodes):
        for p in pset:
            bn.add_edge(c,p)
    return bn


class bnet:
    def __init__( self, node_names ):
        """ Initialize an empty network 
        """
        self.node_names = node_names
        self.bsize = len(node_names)

        self.node_index = np.arange(self.bsize)
        self.global_index = np.arange(self.bsize)
        self.pnodes = [[] for i in node_names]
        self.cnodes = [[] for i in node_names]
        #self.p_candidates=[set([i for i in self.node_index if i!=j]) for j in self.node_index]
        self.pcandidates=set(self.node_index)
        self.pconstraints=[set([i]) for i in self.node_index]
        
        self.pmax=self.bsize
        self.required_edges=[]
        self.forbidden_edges=[]

        self.unconditional_p=False
        self.conditional_p=False
        self.basis=False
        self.adj_mat=False
        self.adj_ind=False

    def __and__(self,net_b):
        intersection=bnet(self.node_names)
        
        for i,name in enumerate(intersection.node_names):
            [intersection.add_edge1(i,j) for j in\
            set(self.pnodes[self.node_names.index(name)])&\
            set(net_b.pnodes[net_b.node_names.index(name)])]

        return intersection

    def __sub__(self,net_b):
        delta=bnet(self.node_names)
        for i,name in enumerate(delta.node_names):
            [delta.add_edge(i,j) for j in\
            set(self.pnodes[self.node_names.index(name)])-\
            set(net_b.pnodes[net_b.node_names.index(name)])]

        return delta
    
    def adjacency_matrix(self):
        """ Populates lower triangular adjacency matrix adj_mat
            and a permutation index adj_ind. 
        """
        a_mat = np.zeros((self.bsize,self.bsize),dtype=int)
        for k in range(self.bsize): a_mat[k,self.pnodes[k]] = 1
        ind = np.argsort([len(self.find_ancestors(i)) for i in self.node_index])
        self.adj_mat = a_mat[ind][:,ind]
        self.adj_ind = ind

    def factor_indx( self ):
        """ Returns an array of [node, ancestors] lists from the adjacency
        matrix if it was populated.
        """
        if type(self.adj_mat) is np.ndarray: adj_mat = self.adj_mat
        else: self.adjacency_matrix()
        out=[]
        for node in range( adj_mat.shape[0] ):
            sources = adj_mat[ node ] > 0
            if np.sum( sources ) == 0: out += [[ node ]]
            else: out += [[node] + np.where( sources )[0].tolist()]
        return np.array(out)

    def joint_prob(self,states):
        """ Returns the joint probability for the joint state if populate_prob() was run
        """
        if (type(self.unconditional_p) is np.ndarray) and\
            (type(self.conditional_p) is np.ndarray):
            tmp=1
            for i,j in enumerate(states):
                indx=np.dot(states[self.pnodes[i]],self.basis[i][1:])
                tmp*=self.conditional_p[i][states[i],indx]
        return tmp


    def get_cp(self,node, data, arity):
        """ helper
        """
        subset = [node] + self.pnodes[node]
        Nijk,Nij,pstates,basis,H,C = cpt( data[:, subset], arity[subset] )
        unconditional=np.sum(Nijk,axis=0)
        vec=np.zeros(Nij.size)
        vec[Nij.nonzero()]=1/Nij[Nij.nonzero()]
        vec=np.diag(vec)
        return unconditional/np.sum(unconditional),np.dot( Nijk.T, vec),basis

    def intrinsic_factorization(self):
        """ Algebraic charachterization of an equivalence class of structures
            as described by Wong and Wu.       
        """
        numerator = ['.'.join(np.sort([i]+j).astype(str)) for i,j in enumerate(self.pnodes)]
        denominator = ['.'.join(np.sort(j).astype(str)) for i,j in enumerate(self.pnodes) if len(j)>0]
        common=np.intersect1d(numerator,denominator)
        for i in common: 
            numerator.remove(i)
            denominator.remove(i)
        return (set(np.sort(numerator)),set(np.sort(denominator)))

    def intrinsic_distance(self,other):
        """ Attempt to establish a distance between two structures
        """
        this=self.intrinsic_factorization()
        distance = lambda x,y: len(x.union(y) - x.intersection(y))
        return distance(this[0],other[0]) + distance(this[1],other[1])
        

    def p_candidates( self, cnode ):
        """ Returns possible ancestor candidates for a node
        """
        return self.pcandidates-self.pconstraints[cnode]

    def c_candidates( self, node ):
        """ Retruns possible descendent candidates for a node
        """
        return self.pcandidates-self.find_ancestors(node)

    def insert_node(self, node_id):
        """ Adds a new node to the existing network object
        """
        self.node_names.append(node_id)
        self.bsize+=1
        self.node_index=np.arange(self.bsize)
        self.pnodes.append([])
        self.cnodes.append([])
        self.pconstraints.append(set([self.node_index[-1]]))

    def remove_node( self, node_id = None ):
        """ Removes the specified node from the existing network object
            node_id - a string ID, or an integer index of the node
        """

        if node_id in self.node_names:
            indx = self.node_names.index( node_id )
        elif node_id in self.node_index:
            indx = node_id
        else:
            raise ValueError("Node not found")

        for ancestor in self.pnodes[ indx ]:
            self.remove_edge( indx, ancestor )

        for descendent in self.cnodes[ indx ]:
            self.remove_edge( descendent, indx )

 
        self.bsize-=1
        self.node_index = np.arange( self.bsize )
        self.pnodes.pop( indx )
        self.cnodes.pop( indx )
        self.pconstraints.pop( indx )
        self.pcandidates = set( self.node_index )
        self.node_names.pop( indx )
                



    def find_ancestors(self,node):
        """ Returns the set of all ancestors of a node
        """
        ancestors=set()
        def g(node,ancestors):
            if node not in ancestors:
                ancestors|=set([node])
                for p in self.pnodes[node]:
                    g(p,ancestors)
        g(node,ancestors)
        return ancestors

    def find_descendents(self,node):
        """ Returns the set of all descendents of a node
        """
        d_set=set()
        def g(node,d_set):
            if node not in d_set:
                d_set|=set([node])
                for c in self.cnodes[node]:
                    g(c,d_set)
        g(node,d_set)
        return d_set
    
    def add_edge(self,cnode,pnode):
        """ Inserts an edge given by (cnode,pnode)
        """
        self.pconstraints[cnode].add(pnode)
        self.pconstraints[pnode].add(cnode)
        self.cnodes[pnode].append(cnode)
        self.pnodes[cnode].append(pnode)
        d_set=self.find_descendents(cnode)
        a_set=self.find_ancestors(pnode)
        for i in a_set:
            self.pconstraints[i]|=d_set

    def add_edge1(self,cnode,pnode):
        """ Inserts the edge given by (cnode,pnode)
        """
        self.pconstraints[cnode].add(pnode)
        self.cnodes[pnode].append(cnode)
        self.pnodes[cnode].append(pnode)
        d_set=self.find_descendents(cnode)
        a_set=self.find_ancestors(pnode)
        for i in a_set:
            self.pconstraints[i]|=d_set


    def add_random_edge(self,add_function=None):
        """ Insert a random edge
        """
        if add_function: add_edge=add_function
        else: add_edge=self.add_edge
        #candidates=(np.array([len(i) for i in self.pnodes])<self.pmax)*\
        #   (np.array([len(j) for j in self.pconstraints])<self.bsize)
        candidates=np.array([len(self.p_candidates(i)) for i in self.node_index])
        if np.sum(candidates)>0:
            cnode=np.random.choice(np.where(candidates>0)[0])
            pnode=np.random.choice([i for i in self.p_candidates(cnode)])
            self.add_edge(cnode,pnode)
            print('add %s->%s' %(pnode,cnode))
        else:
            raise ValueError

    def remove_edge(self,cnode,pnode):
        """ Removes the edge given by (cnode,pnode)
        """
        d_set=self.find_descendents(cnode)
        a_set=self.find_ancestors(pnode)
        self.pnodes[cnode].remove(pnode)
        self.cnodes[pnode].remove(cnode)
        self.pconstraints[cnode]-=set([pnode])
        for i in a_set:
            self.pconstraints[i]=self.find_descendents(i)|\
                                set([i])|set(self.pnodes[i])



    def remove_random_edge(self,remove_function=None):
        """ Remove a random edge
        """
        ind=np.where(np.array([len(i) for i in self.pnodes])>0)[0]
        if ind.size>0:
            cnode=np.random.choice(ind)
            pnode=np.random.choice(self.pnodes[cnode])
            #print('removing %d -> %d' %(pnode,cnode))
            if remove_function:
                remove_function(cnode,pnode)
            else: 
                self.remove_edge(cnode,pnode)
        else: 
            raise ValueError
    
    def perturb_net_old(self,alpha=0.5):
        """ Stochastically perturbs the existing structure
            alpha: the degree of perturbation between 0 and 1, the smaller
            values narrow the window of perturbation speeding up the search for
            large networks.

        """
        n=self.bsize

        #max_add=n*(n-1)*0.5 - np.sum([len(aset) for aset in self.pnodes])

        #start=time.time()
        def get_add_edges():
            add_candidates = []
            for cnode in self.node_index:
                for pnode in self.p_candidates(cnode):
                    add_candidates.append((cnode,pnode))
            return add_candidates

        drop_candidates = []
        for cnode in self.node_index:
            for pnode in self.pnodes[cnode]:
                drop_candidates.append((cnode,pnode))
        
        add_candidates = get_add_edges()
        add_size = len(add_candidates)
        drop_size = len(drop_candidates)
        if add_size>1 : count = np.random.randint(np.log(add_size)+1)
        else: count=0
        s = 0
        while (add_size > 0) and (s < count):
            ind = np.random.randint(add_size)
            cnode,pnode = add_candidates[ind]
            self.add_edge(cnode,pnode)
            #print('add %s->%s' %(pnode,cnode))
            add_candidates=get_add_edges()
            add_size = len(add_candidates)
            #self.intrinsic_factorization()
            s+=1
        #print('add %s' %s)

        if drop_size * alpha >  1:
            ind = np.arange(drop_size)
            np.random.shuffle(ind)
            count = np.random.randint(1,int(drop_size*alpha)+1)
            for i in ind[: count]:
                cnode,pnode = drop_candidates[i]
                self.remove_edge(cnode,pnode)
                #print('drop %s->%s' %(pnode,cnode))
            #print('drop %s' %count)
        #print(time.time()-start)



    def perturb_net(self,alpha=0.5):
        """ Stochastically perturbs the existing structure
            alpha: the degree of perturbation between 0 and 1, the smaller
            values narrow the window of perturbation speeding up the search for
            large networks.

        """
        n=self.bsize

        #max_add=n*(n-1)*0.5 - np.sum([len(aset) for aset in self.pnodes])

        #start=time.time()
        def get_add_edges():
            add_candidates = []
            for cnode in self.node_index:
                for pnode in self.p_candidates(cnode):
                    add_candidates.append((cnode,pnode))
            return add_candidates

        drop_candidates = []
        for cnode in self.node_index:
            for pnode in self.pnodes[cnode]:
                drop_candidates.append((cnode,pnode))
        
        drop_size = len(drop_candidates)
        if drop_size * alpha >  1:
            ind = np.arange(drop_size)
            np.random.shuffle(ind)
            count = np.random.randint(1,int(drop_size*alpha)+1)
            for i in ind[: count]:
                cnode,pnode = drop_candidates[i]
                self.remove_edge(cnode,pnode)

        add_candidates = get_add_edges()
        add_size = len(add_candidates)

        if add_size>1 : count = np.random.randint(np.log(add_size)+1)
        else: count=0
        s = 0
        while (add_size > 0) and (s < count):
            ind = np.random.randint(add_size)
            cnode,pnode = add_candidates[ind]
            self.add_edge(cnode,pnode)
            #print('add %s->%s' %(pnode,cnode))
            add_candidates=get_add_edges()
            add_size = len(add_candidates)
            #self.intrinsic_factorization()
            s+=1
        #print('add %s' %s)


    def random_relaxation(self,nodes, remove_function=None):
        """ relaxation of structure within Markov Cover of a randomly selected node 
        """
        if remove_function:
            rm_edge=remove_function
        else:
            rm_edge=self.remove_edge
        for node in nodes:
            pnodes=np.random.choice(self.pnodes[node],size=np.random.randint(1,len(self.pnodes[node])+1),replace=0)
            for pnode in pnodes:
                rm_edge(node,pnode)

    def mc_relaxation(self,node, remove_function=None):
        """ relaxation of structure within Markov Cover of a randomly selected node 
        """
        if remove_function:
            rm_edge=remove_function
        else:
            rm_edge=self.remove_edge
        mc = [node] + [q for q,k in enumerate(self.pnodes) if node in k]
        np.random.shuffle(mc)
        for i in mc[:np.random.randint(1,len(mc)+1)]:
            if self.pnodes[i]:
                j=np.random.choice(self.pnodes[i])
                print(i,j)
                rm_edge(i,j)


    def make_random_net(self):
        """ Generate a random structure
        """
        adj_mat=np.tril(np.random.randint(0,2,size=(self.bsize,self.bsize)),-1)
        self.pnodes=[i.nonzero()[0].tolist() for i in adj_mat]
        self.cnodes=[i.nonzero()[0].tolist() for i in adj_mat.T]
        self.pconstraints=[set(np.arange(i,self.bsize)) for i in range(self.bsize)]
        

    def markov_cover(self,node):
        """ Returns a network object that corresponds to the Markov Cover of the
        provided node.
        """
        mnodes=[node]+self.pnodes[node]+self.cnodes[node]
        for i in self.cnodes[node]:
            mnodes+=self.pnodes[i]
        mnodes=np.unique(mnodes).tolist()
        markov=bnet([self.node_names[i] for i in mnodes])
        markov.global_index = np.array(mnodes)
        for i,name in enumerate(mnodes):
            for j in set(self.pnodes[name])&set(mnodes):
                markov.add_edge(i,mnodes.index(j))
        return markov

    def subnet_of_radius(self,node,radius=1):
        """ Returns a network object that corresponds to a subnetwork of the
        given radius around the provided node.
        """
        Mn=self.markov_cover(node)
        print( Mn.node_names)
        mnodes=[self.node_names.index(name) for name in Mn.node_names]
        print (mnodes)
        subnet_nodes=[]
        for r in range(radius):
            for i in mnodes:
                Mn=self.markov_cover(i)
                subnet_nodes+=[self.node_names.index(name) for name in Mn.node_names]
                print (Mn.node_names)
            subnet_nodes=np.unique(subnet_nodes).tolist()
            mnodes=[i for i in subnet_nodes]

        subnet_r=bnet([self.node_names[i] for i in subnet_nodes])
        for i,name in enumerate(subnet_nodes):
            for j in set(self.pnodes[name])&set(subnet_nodes):
                subnet_r.add_edge(i,subnet_nodes.index(j))

        return subnet_r

    def dot(self,filename='rendering',header=None):
        """ Render the existing structure into a file output.pdf
        """
        s='digraph G{\n concentrate=true;\n ratio=fill;\n'
        if header:
            s += header + ';\n'
        for child in self.node_index:
            s+='"%s";\n' %self.node_names[child]
            for parent in self.pnodes[child]:
                s+='"%s" -> "%s";\n' %(self.node_names[parent],self.node_names[child])
        s+='}'
        dotfile=open(filename+'.dot','w')
        dotfile.write(s)
        dotfile.close()
        os.system("dot -Tpdf "+filename+".dot -o "+filename+".pdf")


    def bnetsave(self,filename='bnstruct.csv'):
        """ Save the existing structure into a CSV file.
        """
        fout=open(filename,'w')
        csvwr=csv.writer(fout)
        for i,name in enumerate(self.node_names):
            csvwr.writerow([name]+self.pnodes[i])
        fout.close()

def runParallel(foo,iter,ncore):
    pool=multiprocessing.Pool(processes=ncore)
    try:
        out=(pool.map_async( foo,iter )).get()  
    except KeyboardInterrupt:
        print ("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()
    else:
        #print ("Quitting normally core used ",ncore)
        pool.close()
        pool.join()
    try:
        return out
    except Exception:
        return out

def datawrite(output,data,labels=None):
    with open(output, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if labels is not None:
            csv_writer.writerow(labels)
        for row in data:
            csv_writer.writerow(row)

def read_tsv(fin):
    f=open(fin)
    f.readline()
    h=f.readline().strip().split('\t')
    data=np.array([r.strip().split('\t') for r in f.readlines()])
    return h,data 

class Residue():
    def __init__(self):
        self.d={'CYS': 'C', 'CYX': 'C', 'ASP': 'D', 'ASH': 'D', 'SER': 'S', 
                'GLN': 'Q', 'LYS': 'K', 'ILE': 'I', 'PRO': 'P', 'THR': 'T', 
                'PHE': 'F', 'ASN': 'N', 'GLY': 'G', 'HIS': 'H', 'HSD': 'H',
                'HID': 'H', 'HIE': 'H', 'HIP': 'H', 'LEU': 'L', 'ARG': 'R', 
                'TRP': 'W', 'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'GLH': 'E', 
                'TYR': 'Y', 'MET': 'M', 'ZD7': 'Z', 'NMA': 'X', 'LIG': 'LIG' }

    def shRes(self,x):
        #print(self.d.keys())
        if len(x) % 3 != 0: 
            raise ValueError('Input length should be a multiple of three')
        y = ''
        for i in range(len(x) // 3):
            y += self.d[x[3 * i : 3 * i + 3]]
        return y


def transformRes(pair):
    R=Residue()
    res1=R.shRes(pair.split('_')[0][:3])+pair.split('_')[0][3:]
    res2=R.shRes(pair.split('_')[1][:3])+pair.split('_')[1][3:]
    return res1+'_'+res2

def get_unique_pair(data):
    P=np.array([a.split(':')[1:3][0]+a.split(':')[1:3][1][:]+'_'+b.split(':')[1:3][0]+b.split(':')[1:3][1][:] for a,b in data[:,2:]])
    Pt=np.array([transformRes(p) for p in P])
    u,pair_indx=np.unique(Pt,return_inverse=True)
    return Pt,u,pair_indx

def get_trj_s(pair_indx,T,ui):
    tmax=T[-1]
    traj=np.zeros(tmax+1)
    traj[np.unique(T[pair_indx==ui])]=1
    return traj

def get_traj_p(T,pair_indx,nproc): #u also
    tmax=T[-1]
    u=np.unique(pair_indx)
    traj=np.zeros((tmax+1,u.size))
    make_v=partial(get_trj_s,pair_indx,T)
    trj=runParallel(make_v,u,nproc)
    return trj

def remove_Neighbors(contacts,N):
    iplus=np.array([i for i,p in enumerate(contacts) if int(p.split('_')[0][1:])+N != int(p.split('_')[1][1:])])
    imin=np.array([i for i,p in enumerate(contacts) if int(p.split('_')[0][1:])-N != int(p.split('_')[1][1:])])
    return np.intersect1d(iplus,imin)


#Main Function below

def getContact2discret(tsvfile='input.tsv',neighbors=1,csv_out='pairwise_residue_contacts.csv',nproc=28):
    
    # Bulk of this function is this step which is reading tsv and converting to contact matrix
    h,tsv_data=read_tsv(tsvfile)
    pair,unqpair,pair_indx=get_unique_pair(tsv_data)
    T=tsv_data[:,0].astype(int)
    traj=np.array(get_traj_p(T,pair_indx,nproc))

    # Remove neighbors (default is 1)
    I=remove_Neighbors(unqpair,neighbors)
    variables=unqpair[I]
    data=traj[I].T.astype(int)
   
    # If csv file given then save to csv file (Default is to save to trajectory.csv, Set csv_out to None to skip) 
    if csv_out is not None:
        datawrite(csv_out,data,labels=variables)
        return np.vstack((variables,data)) 
    
    # Return dataset with first row as variable names then trajectory data with shape (frames,variables)
    return np.vstack((variables,data))

def read_input_file(f):
    if f[-3:]=='tsv':
        discreteData=getContact2discret(f)
        dt=loader(discreteData)
    else:
        dt=loader(f)
        if np.any(np.array([np.unique(x).size/len(x) for  x in dt.data.T])>0.95):
            dt.quantize_all(bins=8)
    return dt

def loader(data,sep=',',skip_header=0, rowskip=[], colskip=[], axis=1, names=1, fromstring=0):
    """ Loads a data and returns a dataset instance.
        
        data: a filename, string of data, or an array of data;

        The file should contain variable names on the first row,
        or the first column. 
        The rest should be numerical sample values and nothing else!!!

        skip_header: number of lines to skip;

        rowkip: a list of row indecies to skip;;

        colskip: a list of column indecies to skip

        names: should be set to 0 if the variable names are missing or are 
        too cumbersome to be replaced by the variable indecies instead;
        
        axis: 0 for row-wise orientation of the data in the file, or 1 for
        column-wise orientation.

        
    """

    if (type(data)==str) and (fromstring==1):
        iterable=data.strip('\n').split('\n')
        content=np.array([i for i in csv.reader(iterable,delimiter=sep)])
    elif type(data)==np.ndarray:
        content=data
    else:
        csv_reader=csv.reader(open(data,'r'),delimiter=sep)
        for k in range(skip_header):
            next(csv_reader,None)
        content=np.array([i for i in csv_reader])
        #content=np.genfromtxt(filename,delimiter=sep,dtype=str)

    if rowskip:
        content=np.delete(content,rowskip,0)

    if colskip:
        content=np.delete(content,colskip,1)

    if axis==0: # if the file oriented column-wise
        content=content.T

    if names==0:
        variables=np.arange(content.shape[1]).tolist()
        offset=0
    else:
        variables=content[0].tolist()
        offset=1

    try:
        #if type(data)!=np.ndarray:
        content=np.array([conv_col(col) for col in
        content[offset:].T],dtype='object').T
        arity=np.array([np.unique(i).size for i in content.T])
        return dataset(variables,content,arity)
    except ValueError: 
        print( 'Data could not be loaded, failed converting to float.')
        return content



def check_type(col):
    """ helper for conv_col() 
    """
    return any(np.array([\
        isinstance(i,float) for i in col]))


def conv_col(col):
    """ Attempt to convert column from raw to integer data
    """
    try:
        if not check_type(col): 
            out=col.astype(int)
            unq=np.unique(out)
            if np.max(unq)!=unq.size-1:
                #print('index correction')
                out=np.searchsorted(unq,out)
        else: raise ValueError
    except ValueError:
        #print('Not an int')
        try: 
            out=col.astype(float)
        except ValueError:
            print('Falling back to searchsorted for conversion')
            out=np.searchsorted(np.unique(col),col)
    return out

def conv_row(row):
    """ row converter
    """
    out=[]
    for val in row:
        if type(val)==str:
            val=conv(val)
        if type(val)==str:
            print('Falling back to searchsorted method %s' %type(val))
            out=np.searchsorted(np.unique(row),row)
            break
        out.append(val)
    return out

def conv(val):
    try:
        if '.' in val: return float(val)
        else: return int(val)
    except ValueError:
        print ('Data could not be converted: %s' %val)
        return val    
    



class dataset:
    """ Basic methods for preprocessing data """

    def __init__(self,variables,data,arity):
        self.variables=variables
        self.data=data
        self.arity=arity

    def bin_quantize(self, variables=[], bins=3):
        """ Attempt max entropy binning quantization 

            variables:  a list or an array as in variables=[1,3,5]
            bins: the number of categories in the quantization
            min_const_samples_bin_size: determines the min count of
            constant samples that should be given a category of its own
        """
        min_const_samples_bin_size=1.0/bins
        self.edges=np.zeros((self.arity.size,bins+1))
        for i in variables:
            un_cnt=np.unique(self.data[:,i],return_counts=True)
            constvals=un_cnt[0][un_cnt[1]>self.data.shape[0]*min_const_samples_bin_size]
            mask=np.ones(self.data.shape[0],dtype=bool)
            cv_edges=[]
            if constvals.size>0:
                for j,cv in enumerate(constvals):
                    mask*=(self.data[:,i]!=cv)
                    cv_edges+=[np.min(self.data[self.data[:,i]==cv,i])]
                    self.data[self.data[:,i]==cv,i]=j

            size=np.sum(mask)/(bins-constvals.size)
            sorted_i=np.argsort(self.data[mask,i])
            edges=[ self.data[mask,i][sorted_i[int(size*num)-1]] \
                for num in range(1,bins-constvals.size) ]
            #print(edges,constvals.size)
            self.edges[i]=cv_edges+[self.data[mask,i][sorted_i[0]]]+edges+[self.data[mask,i][sorted_i[-1]]]
            self.data[mask,i]=np.searchsorted(edges,self.data[mask,i])+constvals.size
            arity=len(edges)+1+constvals.size
            if arity==np.unique(self.data[:,i]).size : self.arity[i] = arity
            else : self.arity[i] = -1


    def range_quantize(self,variables=[],bins=3):
        """ Uniform range quantization
            
            variables: list of indecies of nodes to quantize
            bins: the number of categories in the quantization
        """
        self.edges=np.zeros((self.arity.size,bins-1))
        for i in variables:
            edges=np.linspace(min(self.data[:,i]),max(self.data[:,i]),bins+1)[1:-1]

            #print(edges)
            self.edges[i]=np.unique(edges)
            self.data[:,i]=np.searchsorted(self.edges[i],self.data[:,i])
            self.arity[i]=np.unique(self.data[:,i]).size

        
    def requantize(self,variables=[]):
        """ Replaces the sample values with their index,
            useful if the data has inconsistencies.

            variables: list of indecies of troublesome nodes
        """

        for i in variables:
            un=np.unique(self.data[:,i]).tolist()
            for j in un:
                inds=np.where(self.data[:,i]==j)[0]
                self.data[inds,i]=un.index(j)
                

    def quantize_all(self, cond = 5, bins=8):
        """ Discretize everything with arity>5 without thinking. 
        """
        self.requantize(np.where(self.arity<=cond)[0])
        self.bin_quantize(np.where(self.arity>cond)[0],bins)
        self.data=self.data.astype(int)
        
class cext:
    def __init__(self):
        """ ctypes interface for C++ objective function implementation
        """
        _path=os.path.dirname(os.path.realpath(__file__))
        self.lib = np.ctypeslib.load_library('ofext',_path)

        #self.lib.mdl.restype=np.ctypeslib.ctypes.c_double
        type_data=np.ctypeslib.ndpointer(dtype=np.int32,ndim=2,flags='C_CONTIGUOUS')
        type_arity=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
        type_out=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
        self.lib.mdl.argtypes=\
            [type_data,\
            np.ctypeslib.ctypes.c_int,\
            type_arity,\
            np.ctypeslib.ctypes.c_int,\
            np.ctypeslib.ctypes.c_int,\
            type_out]

        #self.lib.mu.restype=np.ctypeslib.
        type_data=np.ctypeslib.ndpointer(dtype=np.int32,ndim=2,flags='C_CONTIGUOUS')
        type_arity=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
        type_out=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
        self.lib.mu.argtypes=\
            [type_data,\
            np.ctypeslib.ctypes.c_int,\
            type_arity,\
            np.ctypeslib.ctypes.c_int,\
            type_out]

        

    def mu( self, data, arity ):
        m,n = data.shape
        data = np.require(data, np.int32, 'C')
        arity = np.require(arity ,np.int32, 'C')
        out = np.zeros(2)
        self.lib.mu(data, m, arity, n, out)
        return out


    def mdl(self,data,arity,complexity=1):
        """ cpp mdl objective function
            complexity can be 0 for AIC or 1 for BIC"""
        m,n=data.shape
        data=np.require(data,np.int32,'C')
        arity=np.require(arity,np.int32,'C')
        out = np.zeros(2)
        self.lib.mdl(data,m,arity,n,complexity,out)
        return out
        
def mdl(data,arity,a=1):
    """ Minimum Description Length metric as described by Decampos \
        a=1 constitutes standard mdl (BIC) score
        a=0 constitutes AIC score
    """

    ri = arity[0]
    sink = data[:,0]
    N = sink.size
    penalty = 0.0

    if data.shape[1]==1:
        abasis = np.array([0])
        delta_complexity = 0.0
    else:
        arity[0] = 1
        abasis = np.concatenate(( [0], np.multiply.accumulate(arity[:-1]) ))
        arity[0] = ri
        penalty = (ri-1)*np.multiply.reduce(arity[1:])*np.log(N)*.5*a

    drepr = np.dot( data, abasis )
    un=np.unique( drepr )
    
    #Nijk = np.zeros( ( un.size, ri ), dtype=int )
    #for k,v in enumerate( un ):
    #    Nijk[ k, : ] = np.bincount( sink[ drepr == v ].astype( int ), minlength=ri ) 

    Nijk=np.array([np.bincount(sink[drepr==v].astype(int),minlength=ri) for v in un])


    Nij = np.sum(Nijk,axis=1)
    I = Nij>0
    Nijk = Nijk[I,:]
    pijk = Nijk/Nij[I].reshape(Nij.size,1)
    LL = sum(Nijk[pijk>0]*np.log(pijk[pijk>0]))

    #LL = -H/N
    #H(X|Y) = H(X,Y) - H(Y)
    #MI(X,Y) = H(X) - H(X|Y) = H(X) + H(Y) - H(X,Y) 
    
    return -(LL-penalty)/N, 0


def cpt(data,arity):
    """ Get conditional probability counts, state configurations, 
        encoding basis, relative entropy and complexity values
    """

    ri=arity[0]
    cnode=data[:,0]

    if data.shape[1]==1:
        abasis=np.array([0])
        cartesian = np.array([])
        un=np.array([0])
    else:
        arity[0]=1
        abasis=np.concatenate(([0],np.multiply.accumulate(arity[:-1])))
        arity[0]=ri
        states = [np.arange(r,dtype=np.int8) for r in arity[1:]]
        cartesian = np.array([i for i in product(*states)])
        un=np.sort(np.dot(cartesian,abasis[1:]))

    drepr=np.dot(data,abasis)
    #un1=np.dot(cartesian,abasis[1:])
    #un=np.unique(drepr)
    w_ij=dict([(val,ind) for ind,val in enumerate(un)])
    v_ik=np.unique(cnode)
    Nijk=np.zeros((un.size,ri),dtype=int)
    for k,v in enumerate(un):
       Nijk[k,:]=np.bincount(cnode[drepr==v].astype(int),minlength=ri)

    Nij=np.sum(Nijk,axis=1)
    N_ij=Nij[Nij!=0]
    N_ijk=Nijk[Nijk!=0]
    H=np.dot(N_ijk,np.log(N_ijk))\
        -np.dot(N_ij[N_ij.nonzero()],np.log(N_ij[N_ij.nonzero()]))
    C=(ri-1)*np.multiply.reduce(arity[1:])*np.log(cnode.size)*.5

    #pstates=[data[np.where(drepr==q)[0][0],1:] for q in un]

    return Nijk,Nij,cartesian, abasis, H, C

def bdm(data,arity,new_ancestor_arity=0):
    """ Bayesian Dirichlet metric as described by Cooper&Herskovits """
    N=data.shape[0]
    csize=data.shape[0]+max(arity)
    lgcache=np.arange(0,csize)
    lgcache[0]=1
    lgcache=np.log(lgcache)
    lgcache[0]=0.0
    lgcache=np.add.accumulate(lgcache)
    ri=arity[0]
    cnode=data[:,0]

    if data.shape[1]==1:
        abasis=np.array([0])
    else:
        arity[0]=1
        abasis=np.concatenate(([0],np.multiply.accumulate(arity[:-1])))
        arity[0]=ri

    drepr=np.dot(data,abasis)
    un=np.unique(drepr)
    Nijk=np.zeros((un.size,ri),dtype=int)
    for k,v in enumerate(un):
        Nijk[k,:]=np.bincount(cnode[drepr==v].astype(int),minlength=ri)

    N_ij=np.sum(Nijk,axis=1)
    BD=-np.sum(lgcache[ri-1]+np.sum(lgcache[Nijk],axis=1)-lgcache[N_ij+ri-1])
    return BD/N, 0.0


def mu(data,arity,new_ancestor_arity=0):
    """ Minimum Uncertainty (Mutual Information with sampling uncertainty control)"""

    ri=arity[0]
    sink=data[:,0]

    if data.shape[1]==1:
        abasis=np.array([0])
    else:
        arity[0]=1
        abasis=np.concatenate(([0],np.multiply.accumulate(arity[:-1])))
        arity[0]=ri

    drepr=np.dot(data,abasis)
    un=np.unique(drepr)

    #Nijk=np.zeros((un.size,ri),dtype=int)
    #for k,v in enumerate(un):
    #    Nijk[k,:]=np.bincount(cnode[drepr==v].astype(int),minlength=ri)

    Nijk=np.array([np.bincount(sink[drepr==v].astype(int),minlength=ri) for v in un])

    Nij = np.sum(Nijk,axis=1)
    I = Nij>0
    Nijk = Nijk[I,:]
    pijk = Nijk/Nij[I].reshape(Nij.size,1)
    LL = sum(Nijk[pijk>0]*np.log(pijk[pijk>0]))

    XI = 2 + np.pi**2/24
    mu = sum(np.log(Nij)+XI)
    N=sink.size

    #LL = -H/N
    #H(X|Y) = H(X,Y) - H(Y)
    #MI(X,Y) = H(X) - H(X|Y) = H(X) + H(Y) - H(X,Y) 

    return -LL/N , mu/N

def random_adjmat(var_size , density = None , source_max = None):
    if density is None: density = np.random.randint( 1 , np.int(var_size*(var_size-1)/2) )
    if density>0 and density<1: density = np.int(density * var_size*(var_size - 1)*.5)
    tmp_vec = np.zeros( np.int(var_size*(var_size-1)/2) , dtype = np.int ) 
    tmp_vec[ 0 : density ] = 1
    np.random.shuffle( tmp_vec )
    adj_mat = np.zeros( (var_size,var_size) , dtype=np.int )
    for ind in range( var_size-1 ):
        adj_mat[ ind+1 , 0:ind+1 ] = tmp_vec[ np.int(ind*(ind+1)/2) : np.int((ind+1)*(ind+2)/2) ]
        if not(source_max is None):
            adj_mat[ ind+1 , np.where(adj_mat[ ind+1 , 0:ind+1 ] > 0)[0][source_max:] ] = 0
    return adj_mat


def factor_str( adj_mat ):
    out=''
    for node in range( adj_mat.shape[0] ):
        sources = adj_mat[ node ] > 0
        if np.sum( sources ) == 0: out+='{%s} ' %( node )
        else: out += '{%s%s} ' %( node , np.str(np.where(sources)[0]) )
    return out


def factor_indx( adj_mat ):
    out=[]
    for node in range( adj_mat.shape[0] ):
        sources = adj_mat[ node ] > 0
        if np.sum( sources ) == 0: out += [[ node ]]
        else: out += [[node] + np.where( sources )[0].tolist()]
    return np.array(out)


def joint_prob( node_prob , cond_prob , arity , adj_mat, return_states=False ):
    """ utility for random_dist function, returns an array of joint probabilities constructed for a
    given bundle of nodes """

    prod = np.zeros( adj_mat.shape[0] , dtype=np.object )
    factor = factor_indx( adj_mat ) 
    states = [np.arange(r) for r in arity]
    cartesian = np.stack(np.meshgrid(*states,indexing='ij'),-1).reshape(-1,len(states))
    dimension = np.array([len(factor[node]) for node in range(adj_mat.shape[0]) ])
    terms = node_prob[ dimension == 1].tolist() + cond_prob[ dimension > 1 ].tolist()
    out = np.zeros(len(cartesian))

    for k,indx in enumerate(cartesian):
        tmp=1
        s=''
        for i in range(adj_mat.shape[0]): 
            if dimension[i]>1:
                tmp_arity = np.concatenate(([1],arity[ factor[i][1:] ][:-1]))
                #tmp_arity[0]=1
                basis = np.multiply.accumulate(tmp_arity )
                #if i==6: print(factor[i],indx, indx[i],indx[ factor[i][1:]],\
                #    np.dot(indx[factor[i][1:] ],basis),basis,cond_prob[i].shape )
                #print(k,i,cond_prob[i].shape, arity[factor[i][1:]][:-1], ddd,indx[factor[i][1:]], basis)
                tmp *= cond_prob[i][ indx[i], np.dot(indx[ factor[i][1:] ], basis ) ]
                #s += str(cond_prob[i][ indx[i], np.dot(indx[ factor[i][1:] ], basis ) ])+' '

            else:
                tmp *= node_prob[i][ indx[i] ]
        out[k] = tmp
    if return_states is True:
        return out,cartesian
    else:
        return out


def random_dist( arity , adj_mat , a = 0, bb = 1, cc = 100):
    """ arity - array of node arities;
        adj_mat - adjacency matrix corresponding to the network structure;
        alpha - concentration parameter in the source dirichlet distribution;
        """

    node_prob = np.zeros( arity.size , dtype = np.object )
    cond_prob = np.zeros( arity.size,dtype = np.object )
    source_joint=np.zeros( arity.size,dtype = np.object )
    for node in range( 0 , len( arity ) ):
        sources = adj_mat[ node ] > 0
        if np.sum( sources ) == 0:
            node_prob[ node ] = np.random.dirichlet( [1]*arity[node] )
            #np.random.shuffle(node_prob[ node ])
        else:
            ancestor_arity=np.prod(arity[sources])
            if a: alpha= np.random.gamma(bb,cc,size=arity[node])
            else: alpha=np.ones(arity[node])
            cond_prob[node] = np.random.dirichlet(alpha,size=ancestor_arity).T
            #np.random.dirichlet(np.random.uniform(0,100,size=arity[node]),size=ancestor_arity).T
            #for i in range(arity[node]): np.random.shuffle(cond_prob[node][:,i])
            #E=np.eye(arity[node],ancestor_arity)
            #cond_prob[node] = (cond_prob[node])/np.sum(cond_prob[node],axis=0)
            source_joint[node] = joint_prob(\
                node_prob[sources],cond_prob[sources],\
                arity[sources], adj_mat[sources][:,sources]\
                )
            #print(factor_str(adj_mat[sources][:,sources]))
            node_prob[node]=np.dot(cond_prob[node],source_joint[node])
            #print('node\n %s\n' %np.sum(node_prob[node]))
    return [node_prob,cond_prob,source_joint]


def downstream_sampler( node_prob , cond_prob , arity , adj_mat , sample_size=100 ):
    samples = np.zeros( adj_mat.shape[0] , dtype = np.int )
    out=np.zeros((sample_size,adj_mat.shape[0]), dtype = np.int)
    for k in range(sample_size): 
        seed=np.random.uniform( size=arity.size )
        for node,row in enumerate(adj_mat):
            if np.sum(row) == 0:
                samples[node] = np.searchsorted( 
                np.add.accumulate(node_prob[node]) , seed[node] 
                )
                #print(node_prob[I[node]])
                #print(samples[I[node]])
            else:
                basis = np.multiply.accumulate( [1] + arity[row>0][:-1].tolist() )
                samples[node] = np.searchsorted(\
                     np.add.accumulate( cond_prob[ node ][ : , np.dot(samples[row>0],basis) ] ) ,\
                     seed[node]
                     )
                #print(cond_prob[I[node]][:,np.dot(samples[row>0],basis)] )
                #print(samples[I[node]])
        out[k]=samples
    return out

def downstream_sampler1( node_prob , cond_prob , arity , adj_mat , sample_size=100 ):
    #samples = np.zeros( adj_mat.shape[0] , dtype = np.int )
    samples=np.zeros((sample_size,adj_mat.shape[0]), dtype = np.int)
    #for k in range(sample_size): 
        #seed=np.random.rand( arity.size )
        #np.random.shuffle(seed)
    for node,row in enumerate(adj_mat):
        if np.sum(row) == 0:
            samples[:,node] = np.searchsorted( \
            np.add.accumulate(node_prob[node]) , np.random.rand(sample_size)
            )
            #print(node_prob[I[node]])
            #print(samples[I[node]])
        else:
            basis = np.multiply.accumulate( [1] + arity[row>0][:-1].tolist() )
            ancestors = np.dot(samples[:,row>0], basis)
            for state in np.unique(ancestors):
                samples[ ancestors == state , node ] = np.searchsorted(\
                    np.add.accumulate( cond_prob[ node ][ : , state ] ) ,\
                    np.random.rand(sum(ancestors == state))\
                 )
            #samples[node] = arange(arity[node])[np.random.multionmial(1,\
            #cond_prob[node][:,np.dot(samples[row>0],basis)])>0][0]
            #print(cond_prob[I[node]][:,np.dot(samples[row>0],basis)] )
            #print(samples[I[node]])
    return samples


def upstream_sampler( node_prob , cond_prob , arity , adj_mat , sample_size=100 ):
    samples = np.zeros( adj_mat.shape[0] , dtype = np.int )
    
    I = np.argsort( np.sum( adj_mat , axis = 0 ) ) # sort by number of sinks
    seed=np.random.rand( arity.size )
    for node,row in enumerate(adj_mat.T[I]):
        if np.sum(row) == 0:
            samples[I[node]] = np.searchsorted( 
            np.add.accumulate(node_prob[I[node]]) , seed[node] 
            )
            #print(node_prob[I[node]])
            #print(samples[I[node]])
        else:
            basis = np.multiply.accumulate( [1] + arity[row>0][1:].tolist() )
            samples[I[node]] = np.searchsorted(\
                 np.add.accumulate( cond_prob[ I[node] ][ : , np.dot(samples[row>0],basis) ] ) ,\
                 seed[node]
                 )
            #print(cond_prob[I[node]][:,np.dot(samples[row>0],basis)] )
            #print(samples[I[node]])
    return samples

# Continuous variables 

def conditional_sampl(x,mu,A):
    given1 = np.random.normal()
    given2 = np.linalg.solve( A[1:,1:] , x - mu[1:] - A[1:,0]*given1 )
    given2 = given2.tolist()
    given2.insert(0,given1)
    return mu[0] + np.dot(A[0,:],given2)

def make_A(sigmas,mat):
    Cov = np.outer(sigmas,sigmas.T)
    print(Cov)
    rho=0.4*(mat+mat.T)+np.diag(np.ones(sigmas.size))
    #rho=0.5*np.ones((sigmas.size,sigmas.size))+np.diag(np.ones(sigmas.size)*0.5)
    Cov = Cov*rho
    Cov = np.linalg.cholesky(Cov)
    #print(np.linalg.cholesky(Cov))
    print(Cov)
    return Cov

def cond_normal(mu,S,x,size=None):
    
    b=mu[-1]+np.dot(S[:-1,-1].T,np.dot(np.linalg.inv(S[:-1,:-1]),(x-mu[:-1])))
    print(b)
    A=S[-1,-1] - np.dot(S[:-1,-1].T,np.dot(np.linalg.inv(S[:-1,:-1]),S[:-1,-1]))
    print(A)
    return np.random.normal([b],[A],size)



def continuous_sampler(adj_mat, size):
    samples = np.zeros( adj_mat.shape[0] )
    #mu_node = np.random.randint(-1,1,size=adj_mat.shape[0])
    mu_node = np.random.normal(size=adj_mat.shape[0])
    print(mu_node)
    sigma_node = np.random.uniform(1,6,size=adj_mat.shape[0])
    ind = [[node]+np.where(row>0)[0].tolist() if sum(row)>0 else []
        for node,row in enumerate(adj_mat)]
    A = [ make_A(sigma_node[ii],adj_mat[ii,:][:,ii]) \
        if ii else [] for ii in ind]
    out=[]
    for n in range(size):
        for node,row in enumerate( adj_mat ):
            if np.sum(row) == 0:
                samples[node] =\
                np.random.normal(mu_node[node],scale=sigma_node[node])
            else:
                mu = mu_node[np.array([node]+np.where(row>0)[0].tolist())]
                samples[node] = conditional_sampl(samples[row>0],mu,A[node])
        out.append(samples)
        samples=np.zeros( samples.size)
    return np.array(out)


#Scatter plot distribution of random networks as a function 
def test(arity=np.array([3]*8), samples=10000, alpha=0):
    def tt(arity,a):
        A=random_adjmat(arity.size)
        rd=random_dist(arity,A,alpha)
        return rd[0][-1]

    z=np.array([tt(arity,1).tolist() for i in range(samples)])


#baricentric coordinate to cartesian conversion
    b=np.array([[0,np.sqrt(2)/2,np.sqrt(2)],[0,1,0]])
    zz=np.dot(b,z.T)

    plt.triplot(b[0,:],b[1,:])
    plt.scatter(zz[0,:],zz[1,:],s=.1)
    
#try:
#    cmdl=oflib.cext().mdl
#    cmu=oflib.cext().mu
#except OSError: 
    #print("Try running make")
    #pass

def getGraphProp(filename, fileout):
    g = pd.read_pickle(filename)
    name=g.vs["label"]
    weighted_degree=g.strength(weights=g.es["weight"])
    degree=g.degree()
    percentiles = np.percentile(weighted_degree, np.arange(0, 101, 1))  # Get percentiles from 0 to 100
    percentile_ranks = np.digitize(weighted_degree, percentiles, right=True)
    graph_properties=['Degree', 'Weighted Degree', 'WD Percentile Rank']
    graph_properties_values = [degree,weighted_degree,percentile_ranks]
    for prop_name, prop_values in zip(graph_properties, graph_properties_values):
        g.vs[prop_name] = prop_values
    g.write_graphml(f'{fileout}.graphml')
    file=open(f'{fileout}.csv', 'w')
    file.write("Node name,Degree,Weighted Degree,WD Percentile Rank\n")
    [print("%s,%f,%f,%f"%(a,x,y,z), file=file) for a,x,y,z in zip(name,degree,weighted_degree,percentile_ranks )] 
    file.close()
    
class search:
    """ Methods for BN structure learning """

    def __init__(self, dt, ofunc=None, pscore=None, cache_size=None, target_nodes=None):
        """
        dt: dataset instance of dutils.dataset
        ofunc: objective function can be selected between MU, MDL or BDM. The defalut is MDL.
        If C extension is properly compiled fast MU and MDL options may also be availabe.
        For example, assuming that
        >> import bnomics as bn
        >> data = bn.dutils.loader("test_data")
        was already done, to select fast MDL scoring one should do
        >> out = bn.search(data, ofunc=bn.cmdl)
        the scoring method can be selected between bn.mu, bn.cmu, bn.mdl, bn.cmdl, bn.bdm.              
        """

        # default objective function
        if ofunc: self.objfunc = ofunc
        else: self.objfunc = mdl
        self.sensitivity=1
        
        # set some class variables
        self.data=dt.data
        self.arity=dt.arity
        self.variables=dt.variables
        self.target_nodes=target_nodes

        # make an empty network
        self.BN=bnet(self.variables)

        self.node_index=np.asarray([i for i,j in enumerate(self.variables)])

        # evaluate unconditional scores
        self.scores=np.array([self.objfunc(self.data[:,[i]],self.arity[[i]]) for i in self.node_index])
        self.net_score=np.sum(self.scores)

        # for score caching
        self.cache_size=self.arity.size
        if cache_size:
            self.cache_size=cache_size


        self.delta_cache=np.zeros((self.node_index.size,self.cache_size))
        self.delta_index=np.zeros((self.node_index.size,self.cache_size),dtype=int)
        self.delta_tmp=np.zeros(self.node_index.size)
        
        # primary score tracking arrays
        self.add_deltas=np.zeros(self.node_index.size)
        self.tmp_add = np.zeros(self.scores.shape)
        self.add_candidates=[[] for i in self.node_index]

        self.remove_deltas=np.zeros(self.node_index.size)
        self.remove_candidates=[[] for i in self.node_index]
        self.tmp_remove = np.zeros(self.scores.shape)

        self.edge_scores = [[] for i in self.node_index]

        # targeted or untargeted reconstruction
        if target_nodes:
            for target_node in target_nodes:
                self.add_score(target_node)
        else:
            for i in self.node_index:
                self.add_score(i)




    def d_score_serial(self,node):
        """ Score ancestor candidates as descendents 
        """
        a_set = self.BN.find_ancestors(node)
        for i in sefl.BN.pcandidates-a_set:
            new_score = self.objfunc(self.data[:,[i,node]] , self.arity[[i,node]])
            delta_tmp[i] = new_score - self.scores[cnode]
        self.delta_tmp[delta_tmp<0.0] = 0.0
        self.delta_cache[:,node] = delta_tmp
        delta_tmp[:] = 0.0

    def add_score(self,cnode):
        """ Simple first order search of an edge to add 
        """

        start=time.time()
        family=self.BN.pnodes[cnode]
        score=self.scores[cnode]
        old_score=score[0]
        delta_tmp=self.delta_tmp
        parent=[]
        dd = 0
        ss=0
        for i in self.BN.p_candidates(cnode):
            subset=[cnode]+family+[i]#np.sort(family+[i]).tolist()
            new_score=self.objfunc(self.data[:,subset],self.arity[subset])

            d = score[0] - new_score[0] - new_score[1]*self.sensitivity
            if d  > dd: 
                dd = d 
                #ss = new_score[1]
                parent=[i] 
                self.tmp_add[cnode] = new_score
                #cond = False
                
        self.add_deltas[cnode] = dd
        self.add_candidates[cnode]=parent
        #print(time.time()-start)

    def remove_score(self,cnode):
        """ Simple reverse search for an edge to remove 
        """
        family=self.BN.pnodes[cnode]
        score=self.scores[cnode]
        old_score=score[0]
        epsilon = 0.0
        dd=0.0
        ss=0.0 
        parent=[]
        for i in self.BN.pnodes[cnode]:
            indx = family.index(i)
            family.remove(i)
            subset = [cnode]+family
            drop_score = self.objfunc(self.data[:,subset],self.arity[subset])
            family.insert(indx,i)

            d = drop_score[0] - score[0] - score[1]*self.sensitivity
            if d <= dd : 
                dd = d
                ss=score[1]; epsilon=1.0; parent = [i]; 
                self.tmp_remove[cnode] = drop_score

        self.remove_candidates[cnode] = parent
        self.remove_deltas[cnode] = -dd+epsilon


    def add_score_old(self,cnode):
        """ Simple first order search of an edge to add 
        """

        start=time.time()
        family=self.BN.pnodes[cnode]
        score=self.scores[cnode]
        old_score=score
        delta_tmp=self.delta_tmp
        parent=[]
        for i in self.BN.p_candidates(cnode):
            subset=[cnode]+np.sort(family+[i]).tolist()
            new_score=self.objfunc(self.data[:,subset],self.arity[subset])
            if score<new_score: 
                score=new_score; parent=[i]; self.tmp_add[cnode] = new_score
        self.add_deltas[cnode]=score-old_score
        self.add_candidates[cnode]=parent
        #print(time.time()-start)



    def add_score_old(self,cnode):
        """ Simple first order search of an edge to add"""

        family=[cnode]+self.BN.pnodes[cnode]
        score=self.scores[cnode]
        delta_tmp=self.delta_tmp
        for i in self.BN.p_candidates(cnode):
            subset=family+[i]
            new_score=self.objfunc(self.data[:,subset],self.arity[subset])
            delta_tmp[i]=new_score-score
        self.delta_tmp[delta_tmp<0.0]=0.0
        self.delta_index[cnode,:]=np.argsort(delta_tmp)[-self.cache_size:]
        self.delta_cache[cnode,:]=delta_tmp[self.delta_index[cnode,:]]
        delta_tmp[delta_tmp>0]=0.0




    def remove_score_old(self,cnode):
        """ Simple reverse search for an edge to remove 
        """
        family=self.BN.pnodes[cnode]
        score=self.scores[cnode]
        old_score=score
        delta = 0
        parent=[]
        for i in self.BN.pnodes[cnode]:
            indx = family.index(i)
            family.remove(i)
            subset=[cnode]+family
            new_score=self.objfunc(self.data[:,subset],self.arity[subset])
            family.insert(indx,i)
            if new_score >= score: 
                score=new_score
                parent=[i]
                delta=1
                self.tmp_remove[cnode]=new_score
        self.remove_candidates[cnode]=parent
        self.remove_deltas[cnode]=score-old_score+delta


    def ancestor_pair(self,node):
        """ Find the best pair of ancestors for node.
        """
        ancestors=self.BN.pnodes[node]
        score=self.scores[node]
        tmp=0.0
        pair=[]
        for i in self.BN.p_candidates(node):
            for j in self.BN.p_candidates(node):
                if j>i:
                    subset=[node]+np.sort([i,j]+ancestors).tolist()
                    new_score=self.objfunc(self.data[:,subset],self.arity[subset])
                    delta=new_score-score
                    if delta>tmp:
                        tmp=delta*0.5
                        pair=[i,j]
            
        return pair,tmp
    
        

    def add_edge_and_sync(self,cnode,pnode):
        """ Add the edge to DAG, apply the induced constraints and update scores """

        #print('adding %s->%s' %(pnode,cnode))

        #self.scores[cnode]+=self.add_deltas[cnode]
        self.scores[cnode] = self.tmp_add[cnode]  #mods for mu


        self.BN.pconstraints[cnode].add(pnode)
        self.BN.pconstraints[pnode].add(cnode)
        self.BN.cnodes[pnode].append(cnode)
        self.BN.cnodes[pnode].sort()
        self.BN.pnodes[cnode].append(pnode)
        self.BN.pnodes[cnode].sort()
        self.add_score(cnode)

        # get ancestor and descendent sets and propagate necessary changes
        # through scores and constraints
        d_set=self.BN.find_descendents(cnode)
        a_set=self.BN.find_ancestors(pnode)
        for i in a_set:

            if d_set-self.BN.pconstraints[i]:
                self.BN.pconstraints[i]|=d_set
            self.add_score(i)





    def remove_edge_and_sync(self,cnode,pnode):
        """ Remove the edge from DAG, relax constraints and update the scores """

        #print('removing %s -> %s' %(pnode,cnode))

        # get ancestor and descendent sets
        d_set=self.BN.find_descendents(cnode)
        a_set=self.BN.find_ancestors(pnode)

        # modify the locality of the edge and update scores
        self.BN.pnodes[cnode].remove(pnode)
        self.BN.cnodes[pnode].remove(cnode)
        self.BN.pconstraints[cnode]-=set([pnode])
        family=[cnode]+self.BN.pnodes[cnode]
        self.scores[cnode]=self.tmp_remove[cnode] #self.objfunc(self.data[:,family],self.arity[family])
        self.add_score(cnode)
        self.remove_score(cnode)

        # propagate changes through constraints and scores
        for i in self.BN.pnodes[cnode]:
            a_set-=self.BN.find_ancestors(i)

        for i in a_set:
            update_constraints=self.BN.find_descendents(i)|set([i])|set(self.BN.pnodes[i])
            if self.BN.pconstraints[i]-update_constraints:
                self.BN.pconstraints[i] = update_constraints
            self.add_score(i)
  
            
    def ascent(self, max_iter=None):
        """ Data driven structure learning ascent.
            max_iter: the upper bound on the number of added to the BN edges
        """
        N = self.node_index.size
        if max_iter is None: max_iter=N*np.log(N)
        

        #best_deltas=np.amax(self.delta_cache,axis=1)
        #max_delta = np.max(best_deltas)

        # Initialize 
        #max_add = np.min(self.tmp_add[:,1])
        max_add = np.max(self.add_deltas)
        max_remove = np.max(self.remove_deltas)
        #max_remove = np.max(self.tmp_remove[:,1])

        #cnode=np.argmax(best_deltas)
        #pnode=np.argmax(self.delta_cache[cnode,:])


        cur_iter=0
        # iteratre until tolerances or max_iter is hit
        while (max_add>0.0 or max_remove>0.0) and (cur_iter<max_iter):

            # add an edge first and update conditionals
            if max_add>0.0:#max_remove:
                cnode = np.argmax(self.add_deltas)
                pnode = self.add_candidates[cnode][0]


                # check that the pair (cnode,pnode) doesn't create a cycle
                if pnode in self.BN.cnodes[cnode]:
                    print('cycle: %s->%s' %(pnode,cnode))
                    raise ValueError

                # add the egde and update the removal scores
                self.add_edge_and_sync(cnode,pnode)
                self.remove_score(cnode)

                # update conditionals 
                max_add = np.max(self.add_deltas)
                max_remove = np.max(self.remove_deltas)
    
            # remove an edge and update conditionals
            if max_remove>0.0:
                cnode=np.argmax(self.remove_deltas)
                pnode=self.remove_candidates[cnode][0]
                self.remove_edge_and_sync(cnode,pnode)

                # update conditionals after sync
                max_add = np.max(self.add_deltas)
                max_remove = np.max(self.remove_deltas)

                                                   
            cur_iter+=1

        return self.net_score,np.sum(self.scores)  



    def restarts(self, nrestarts=10, criterion=False, alpha=0.5):
        """ Ascent with stochastically perturbed restarts.

        nrestarts: integer number of restarts to perform;
        criterion: when provided the result of intrinsic_factorization() serves
        as a stoping criterion when searching for a predefined network;
        alpha: float in (0,1), the degree of perturbation, when small it aids in speeding up
        the search in large spaces by controlling/narrowing the perturbation
        window; """


        bn_search=self.ascent

        bn_search()
        tmpBN=deepcopy(self.BN)
        tmpscore=np.sum(self.scores) #MIR mod

        if criterion:
            res=[[1,tmpscore,tmpBN.intrinsic_factorization()==criterion]]
        else:
            res=[[1,tmpscore]]

        visited_BN=[]
        for restart in range(2,nrestarts+1):
            print("iteration %d" %restart)

            # Perturb the structure, check if this equivalence class was
            # visited before, and update scores.
            self.BN.perturb_net(alpha)
            ifac = self.BN.intrinsic_factorization()
            if ifac not in visited_BN: 
                visited_BN.append(ifac)
            self.score_net()
            for node in self.BN.node_index:
                self.add_score(node)
                self.remove_score(node)
            bn_search()
            current_score=np.sum(self.scores) #MIR mod

            # Check for improvement and, if criterion was set, check whether
            # equivalence class was reached.
            if current_score<tmpscore: #MIR mod
                print('found', current_score)
                self.dot(filename=f'{restart}')
                tmpBN=deepcopy(self.BN)
                tmpscore=current_score
                if criterion:
                    equivalence = tmpBN.intrinsic_factorization()==criterion 
                    res.append([restart,tmpscore,equivalence]) 
                    if equivalence: break
                else:
                    res.append([restart,tmpscore])


        #print("%s visited classes" %len(visited_BN))
        self.BN=deepcopy(tmpBN)
        self.score_net()
        return res




    def simple_search(self, max_edges=None, tol=10**-6):
        """ Simple data driven structure learning search.

            max_edges is the upper bound on the number of edges added to the BN.
        """

        # If max_edges is not provided try to add up to twice as many edges as
        # there are nodes 
        if max_edges is None: max_edges=2*self.node_index.size

        for i in self.node_index:
            self.add_score(i)
        best_deltas=np.amax(self.delta_cache,axis=1)
        cnode=np.argmax(best_deltas)
        pnode=np.argmax(self.delta_cache[cnode,:])
        cur_iter=0
        while np.max(best_deltas)>tol and cur_iter<max_edges:
            print( 'iteration %s' %cur_iter)
            print(best_deltas[cnode],cnode,self.delta_index[cnode,pnode])
            self.add_edge_and_sync(cnode,pnode)

            best_deltas=np.amax(self.delta_cache,axis=1)
            cnode=np.argmax(best_deltas)
            pnode=np.argmax(self.delta_cache[cnode,:])
            cur_iter+=1
        return self.net_score,np.sum(np.diag(self.scores))


    def score_net(self):
        """ Score the constructed BN """

        score=0
        for child in self.node_index:
            subset=[child]+self.BN.pnodes[child]
            self.scores[child]=self.objfunc(self.data[:,subset],self.arity[subset])
        self.net_score=np.sum(self.scores, axis=0)#[:,-1]) #MIR mod
        return self.net_score
    

    def score_edge(self, cnode, pnode):
        """ Score the edge given by (cnode,pnode) """
        bundle=[cnode]+self.BN.pnodes[cnode]
        
        score=self.scores[cnode]
        #score=self.objfunc(self.data[:,bundle],self.arity[bundle])
        try:
            bundle.remove(pnode)
        except ValueError:
            print(cnode,pnode)
        drop_score=self.objfunc(self.data[:,bundle],self.arity[bundle])

        return drop_score[0]-score[0]-score[1]*self.sensitivity

    def score_edges(self):
        self.edge_scores = [[self.score_edge(cnode,pnode) for pnode in self.BN.pnodes[cnode]] for cnode in self.BN.node_index]


    def get_cpt(self,subset):
        """ Helper for populate_prob function """

        Nijk,Nij,pstates,basis,H,C = cpt( self.data[:, subset], self.arity[subset] )
        unconditional=np.sum(Nijk,axis=0)
        vec=np.zeros(Nij.size)
        vec[Nij.nonzero()]=1/Nij[Nij.nonzero()]
        vec=np.diag(vec)
        return unconditional/np.sum(unconditional),np.dot( Nijk.T, vec),basis

    def populate_prob(self, node=None):
        """ Returns Markov Cover of a node with induced P(node : MC), 
            i.e. probability of node given its Markov Cover;

            node: integer index of the node in question; """
            
        if node is None: mc = self.BN
        else: mc=self.BN.markov_cover(node)
        mc.unconditional_p=np.zeros(mc.bsize,dtype=object)
        mc.conditional_p=np.zeros(mc.bsize,dtype=object)
        mc.basis=np.zeros(mc.bsize,dtype=object)
        print(mc.bsize) 
        for i in range(mc.bsize):

            subset = mc.global_index[[i] + mc.pnodes[i]]
            print(subset)
            mc.unconditional_p[i],mc.conditional_p[i],mc.basis[i]\
            = self.get_cpt(subset)
        if not(node is None): return mc
        
        


    def stats(self,node=None,filename='', return_Nijk=False):
        """ Print out P(node : ancestors) and some other useful data.

        node: integer index of the node of interest; 
        filename: string containing the name of the file to save to; 
        return_Nijk=False: if True the function will return the joint state
        counts Nijk for node_i and its ancestors where the column index k correspond to
        node states and row index j corresponds to ancestor joint states; """

        if node is None:
            nodes=self.BN.node_index
        else: nodes=[node]
        output=''
        for node in nodes:
            subset=[node]+self.BN.pnodes[node]
            Nijk,Nij,pstates,basis,H,C=cpt(self.data[:,subset],self.arity[subset])

            head='\t\t'.join(['%4s' %val  for val in np.unique(self.data[:,node])])
            output+='Node: '+str(self.BN.node_names[node])+':'+str(node)+'\n'
            tmp=''.join(['Ancestors: ',
                ' '.join(['('+str(self.BN.node_names[i])+':'+str(i)+')'
                for i in self.BN.pnodes[node]])])
            output+='\n'.join(tw.wrap(tmp))+'\n'
            tmp=''.join(['Descendants: ',
                    ' '.join(['('+str(self.BN.node_names[i])+':'+str(i)+')'
                for i in self.BN.cnodes[node]])])
            output+='\n'.join(tw.wrap(tmp))+'\n'
            output+='H=%f C=%f\n' %(H,C)
            output+='State\tCount\t'+head+'\n\n'
            for i,state in enumerate(pstates):
                output+=''.join([''.join(list(map(str,state))),\
                '\t%4s\t' %(Nij[i]),\
                '\t'.join(['%4s(%.2f)' %(val,val/Nij[i])\
                if Nij[i]>0 else '%4s(%.2f)' %(0,0.0) for val in Nijk[i,:] ]),'\n'])
            output+='\n\n'
        if filename:
            print(output,file=open(filename,'w'))
        else:
            print(output)
        if return_Nijk: return Nijk

    
        
        




    def dot(self, filename = "rendering", \
                    path = "", \
                    tol = 10**-16, \
                    cnode = None, \
                    radius = None,\
                    concentrate = False, \
                    edge_label = True, \
                    connected_only = True, \
                    logscale = False, \
                    return_scores=False):
        """ Create a dot file for the constructed BN.

            path:   optional string pointing to the location of the file to be created;
            tol:    minimum edge stregth required for the edge to be rendered;
            cnode:  optional node index to construct Markov neighborhood around;
            radius = None:          if int r is provided, constructs neighborhood of radius r around the node;
            edge_label = True:      if False, edge strengths labels are dropped;
            concentrate = False:    if True merges edges with common source together;
            logscale = False:       linear greyscale gradient, or logarithmic greyscale gradient to draw edges;
            connected_only = True:  render only the connected nodes, drop the rest;

        """

        BN=self.BN


        if not cnode is None:
            if radius is None:
                BN=self.BN.markov_cover(cnode)
                print( 'Markov neighborhood of %s' %self.BN.node_names[cnode])
            else:
                BN=self.BN.subnet_of_radius(cnode,radius)
                print("Subnet of radius %d around %s" \
                    %(radius,self.BN.node_names[cnode]) )
        
        # Index map for Markov Net scoring
        ind_map=[self.BN.node_names.index(i) for i in BN.node_names]

        edge_scores=[]
        edges=[]
        
        # Begin the dot string and set some global attributes 
        s='digraph G{\n ratio=fill;\n node [shape=box, style=rounded];\n\
            edge [penwidth=1];\n'
        if bool(concentrate):
            s+='concentrate=true;\n'

        
        if bool(connected_only):
            node_index=[i for i in BN.node_index if BN.pnodes[i]]
        else:
            node_index=BN.node_index
        

        #self.score_edges()
        for cnode in node_index:
            s+='"%s";\n' %BN.node_names[cnode]

            for pnode in BN.pnodes[cnode]:

                # In case BN is a Markov Neighborhood translate the edge
                # indices into their global equivalent and score. Otherwise the
                # map is an identity
                cnode_g=ind_map[cnode]
                pnode_g=ind_map[pnode] 

                edge_score = self.score_edge(cnode_g,pnode_g)

                #print(edge_score)
                if edge_score>tol:
                    edge_scores.append(edge_score)
                    edges.append((pnode_g,cnode_g))

        
        # Generate grayscale color gradient for all the edges
        edge_scores = np.array(edge_scores)
        color_grad = np.ones(len(edge_scores))
        pos_scores = edge_scores[edge_scores>0]


        if bool(logscale):
            log_score_range=np.log(np.max(pos_scores))-np.log(np.min(pos_scores)) 
            color_grad[edge_scores > 0] = 0.9-(np.log(pos_scores)-np.log(np.min(pos_scores)))/log_score_range
            #color_grad=(1-np.array(np.log(np.abs(edge_scores)))/np.log(np.max(edge_scores)))
        else:
            score_range = np.max(pos_scores)
            color_grad[edge_scores>0]=(.9-np.array(pos_scores)/score_range)

        indx=np.argsort(edge_scores)
        
        # Add edges and style to the dot string
        for i,j in enumerate(edge_scores):


            if bool(edge_label):
                if j>0: 
                    col = '0 .2 %s' %(color_grad[i])
                    stl='[color="%s", fontcolor="%s", style=bold, label="%.4f" ]' %(col,col,j)
                else: stl='[color="0 0 0", style="dotted", arrowhead="empty" ]' 
            else:
                if j>0: stl='[color="0 0.2 %s"]' %(color_grad[i])   #style=bold ]'
                else: stl = '[color = "0.0 1.0 1.0"]'



            s+='"%s" -> "%s" %s;\n' %(BN.node_names[edges[i][0]],BN.node_names[edges[i][1]],stl)

        s+='}'

        # Write the dot string to file
        filestring = path+filename
        foo=open(filestring+".dot","w")
        foo.write(s)
        foo.close()
        os.system("dot -Tpdf "+filestring+".dot -o "+filestring+".pdf")

        if bool(return_scores): 
            return np.hstack([edge_scores.reshape((edge_scores.size,1)).astype(object),edges])

def load_graph(dot_file_path):
    """Load a graph from a DOT file."""
    graphs = pydot.graph_from_dot_file(dot_file_path)
    return graphs[0]

def is_valid_node(node_name):
    """Check if a node name is valid and not a reserved word or empty."""
    excluded_nodes = {'edge', 'node', '\\n', ''}
    node_name = node_name.strip('"').strip()
    return node_name not in excluded_nodes and not node_name.isspace()

def create_adjacency_matrix(graph, nodes):
    """Create an adjacency matrix for a given graph and list of nodes."""
    matrix_size = len(nodes)
    adjacency_matrix = np.zeros((matrix_size, matrix_size), dtype=float)
    node_to_index = {node: idx for idx, node in enumerate(nodes)}

    for edge in graph.get_edges():
        source = edge.get_source().strip('"')
        target = edge.get_destination().strip('"')
        weight = edge.get_attributes().get('label', '1').strip('"')
        try:
            weight = float(weight)
        except ValueError:
            weight = 1.0
        if source in nodes and target in nodes:
            adjacency_matrix[node_to_index[source], node_to_index[target]] = weight

    return adjacency_matrix

def calculate_hamming_distance_between_graphs(dot_file_path_1, dot_file_path_2):
    """Calculate the Hamming distance between two matrices."""
    graph1=load_graph(dot_file_path_1)
    graph2=load_graph(dot_file_path_2)
    nodes = {node.get_name().strip().strip('"') for node in graph1.get_nodes() if is_valid_node(node.get_name().strip().strip('"'))}
    nodes.update({node.get_name().strip().strip('"') for node in graph2.get_nodes() if is_valid_node(node.get_name().strip().strip('"'))})
    matrix1=create_adjacency_matrix(graph1, nodes)
    matrix2=create_adjacency_matrix(graph2, nodes)    
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    hamming_distances = 0

    for node in nodes:
        node_index = node_to_index[node]
        distance = np.sum(np.abs(matrix1[node_index, :] - matrix2[node_index, :]))
        hamming_distances += distance
    print(f'Weighted Hamming distance between two graphs: {hamming_distances}')
    #return hamming_distances
    
def calculate_hamming_distances_per_node(dot_file_path_1, dot_file_path_2, output_filename):
    """Calculate the Hamming distance for each node between two matrices."""
    graph1 = load_graph(dot_file_path_1)
    graph2 = load_graph(dot_file_path_2)
    nodes = {node.get_name().strip().strip('"') for node in graph1.get_nodes() if is_valid_node(node.get_name().strip().strip('"'))}
    nodes.update({node.get_name().strip().strip('"') for node in graph2.get_nodes() if is_valid_node(node.get_name().strip().strip('"'))})
    
    matrix1 = create_adjacency_matrix(graph1, nodes)
    matrix2 = create_adjacency_matrix(graph2, nodes)
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    hamming_distances = {}

    for node in nodes:
        node_index = node_to_index[node]
        distance = np.sum(np.abs(matrix1[node_index, :] - matrix2[node_index, :]))
        hamming_distances[node] = distance
        
    df = pd.DataFrame(list(hamming_distances.items()), columns=['Node', 'Weighted Hamming Distance'])
    df.to_csv(output_filename, index=False)
    
    return hamming_distances

def convert_bn_to_igraph(srch,tol=0,directed=True,fout=False,format="pickle"):
    g = ig.Graph(directed=directed)
    bn=srch.BN
    g.add_vertices(bn.node_index.size)
    g.vs["label"]=bn.node_names
    ew=[]
    for child in bn.node_index:
        for parent in bn.pnodes[child]:
            edge_score=srch.score_edge(child,parent)
            if edge_score>tol:
                g.add_edge(parent,child)
                ew.append(edge_score)
    g.es["weight"]=ew
    if fout:
        g.save(fout,format=format)
    return g

def plot_hamming_distances(hamming_distances, value_filter=0, figsize=(25,25), fout=False):
    """Plot hamming distances in a circular graph representation, only for values greater than 0."""
    filtered_distances = {key: value for key, value in hamming_distances.items() if value > value_filter}
    sorted_data = sorted(filtered_distances.items(), key=lambda item: item[1])
    offset = np.pi / 2
    starting_radius = 0.5
    segment_width = 1
    arc_spacing = 0.1
    text_offset = 0.1
    colors = plt.cm.viridis(np.linspace(0, 1, len(filtered_distances)))
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    
    for i, (key, num) in enumerate(sorted_data):
        end_angle = (num / sum(hamming_distances.values())) * 2 * np.pi * 5
        end_angle = min(end_angle, 2 * np.pi)
        t = np.linspace(offset, end_angle + offset, 100)
        r = np.full_like(t, starting_radius + i * (segment_width + arc_spacing))
        ax.plot(t, r, lw=segment_width * 11, color='black', solid_capstyle='butt')
        ax.plot(t, r, lw=segment_width * 10, color=colors[i], solid_capstyle='butt')
        ax.text(offset, r[0], key, ha='left', va='center', fontsize=9, color='black')
    ax.set_frame_on(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    
    if fout:
        plt.savefig(fout, dpi=500)
    plt.show()
