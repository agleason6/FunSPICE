
#Copyright 2019 Adam Gleason, A2P Design Services LLC

#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy
from sympy import *
from Stamps import *

class FunSPICE:
  single = ['V', 'E', 'F', 'O']
  double = ['H']

  def __init__(self, netlist):
    self.nl = netlist

    # Compile netlist into list of stamp objects
    self.compile_stamps()
    
    # Initialize the circuit matrix and solution vectors
    self.init_matrix()

    # Assign l indicies to netlist elements that require it (O, V, etc)
    self.assign_l_indices()

    # apply stamps to matrix
    self.cir_mat = apply_stamps(self.stamps, self.cir_mat)

    # Convert list of lists to actual SymPy Matrix
    self.cir_mat = Matrix(self.cir_mat)

    # Put it in RREF (solve it)
    
    self.cir_rref = self.cir_mat.rref()
    self.cir_mat = self.cir_rref[0]


    # Collect Results
    self.collect_results()


  def get_cir_mat(self):
    return self.cir_mat

  def init_matrix(self):
    if self.nl is not None:

      self.ncurrents = 0 
      # loop through stamps and count nodes and currents
      self.u_nodes = []
      for stamp in self.stamps:
        nodes = stamp.get_nodes()
        # check if it has unique nodes
        for node in nodes:
            # if the node is not already on the list
            if (nodes[node] not in self.u_nodes):
                # then add it to the list
                self.u_nodes.append(nodes[node])
        self.ncurrents = self.ncurrents + stamp.get_ncurrents()            

      self.nnodes = len(self.u_nodes)

      # compute circuit matrix dimensions
      self.N = self.nnodes + self.ncurrents
      self.M = self.N + 1
      
      # create blank circuit matrix (to be stamped later)
      self.cir_mat = numpy.zeros((self.N,self.M), dtype=numpy.int)
      self.cir_mat = list(self.cir_mat)
      for i in range(self.N):
        self.cir_mat[i] = list(self.cir_mat[i])
    
      # solution index vectors (l's to be assigned to stamps later)
      self.v_ind = list(numpy.arange(0,self.nnodes))
      self.l_ind = []
      if (self.ncurrents > 0):
        if (self.ncurrents == 1):
          self.l_ind = [self.nnodes]
        else:
          self.l_ind = list(numpy.arange(self.nnodes, self.N))


  def assign_l_indices(self): 
    l_ind_copy = self.l_ind.copy()
    for stamp in self.stamps:
        ni = stamp.get_ncurrents()
        if (ni == 1):
          stamp.set_l(l_ind_copy[0])
          l_ind_copy.pop(0)
        elif (ni == 2):
          stamp.set_l([l_ind_copy[0], l_ind_copy[1]])
          l_ind_copy.pop(0)
          l_ind_copy.pop(0)
        elif (ni == 3):
          stamp.set_l([l_ind_copy[0], l_ind_copy[1], l_ind_copy[2]])
          l_ind_copy.pop(0)
          l_ind_copy.pop(0)
          l_ind_copy.pop(0)

  def compile_stamps(self):
    self.stamps = []
    for elem in self.nl:
      self.stamps.append(stamp_lu[elem['type']](elem))

  def collect_results(self):
    self.results = {}
    self.result_keys = []
    for vi in self.v_ind:
      key = 'v' + str(vi+1)
      val = self.cir_mat[vi,-1]
      val = S(str(val))
      val = simplify(val)
      self.results[key] = val
      self.result_keys.append(key)
    ic = 1
    for li in self.l_ind:
      key = 'i' + str(ic)
      ic = ic + 1
      val = self.cir_mat[li,-1]
      val = S(str(val))
      val = simplify(val)
      self.results[key] = val
      self.result_keys.append(key)

  def print_results(self):
    print('****************************************')
    print('******        RESULTS          *********')
    print('****************************************')
    for key in self.result_keys:
        print(key + ' = ')
        print(pretty(self.results[key]))
        print('****************************************')


def sens(function, var):
    ret = (var/function)*diff(function,var)
    ret = simplify(ret)
    return ret 

def poleszeros(tf):
    s = Symbol("s")
    zeros, poles = fraction(tf)
    pole_freqs = simplify(solve(poles, s))
    zero_freqs = simplify(solve(zeros, s))
    return zero_freqs, pole_freqs

def abeta(tf_cl):
    num, den = fraction(tf_cl)
    beta = (den-1)/num
    a = (den-1)/beta
    return a, beta
