#Copyright 2019 Adam Gleason, A2P Design Services LLC

#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

#3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ******************************
# Stamp Base Class
# ******************************
class Stamp_Base:
  def add_val(self, cur_val, new_val):
    if cur_val == 0:
      return new_val
    else:
      if type(cur_val) is str:
        return cur_val + ' + ' + str(new_val)
      else:
        if type(new_val) is str:
          return str(cur_val) + ' + ' + new_val
        else:
          return cur_val + new_val
    
  def parse_nodes(self, dev, nodes):
    nodes_copy = nodes.copy()
    for node in nodes:
      if dev[node] == 0:
        del nodes_copy[node]
      else:
        nodes_copy[node] = dev[node]
    self.nodes = nodes_copy
    self.nnodes = len(self.nodes)
  
  def get_nodes(self):
    return self.nodes

  def get_nnodes(self):
    return self.nnodes

  def get_ncurrents(self):
    return self.ncurrents

  def set_l(self, l):
    self.l = l

# ******************************
# Resistor Stamp
# ******************************
class R_Stamp(Stamp_Base):
  # example device
  #{'type':'R', 'k':1, 'j':0, 'val':'R1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 2
    self.nodes = {'k':0,'j':0}
    self.ncurrents = 0
    self.k = dev['k']
    self.j = dev['j']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)
    
  def stamp(self, mat):
    if type(self.val) is str:
      pos = '1/' + self.val
      neg = '-'  + pos
    else:
      pos = 1.0/self.val
      neg = -1*pos
    if self.k != 0:
      mat[self.k-1][self.k-1] = self.add_val(mat[self.k-1][self.k-1], pos)
      if self.j != 0:
        mat[self.k-1][self.j-1] = self.add_val(mat[self.k-1][self.j-1],neg)
    if self.j != 0:
      mat[self.j-1][self.j-1] = self.add_val(mat[self.j-1][self.j-1], pos)
      if self.k != 0:
        mat[self.j-1][self.k-1] = self.add_val(mat[self.j-1][self.k-1], neg)
    return mat

# ******************************
# Capacitor Stamp
# ******************************
class C_Stamp(Stamp_Base):
  # example device
  #{'type':'C', 'k':1, 'j':0, 'val':'C1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 2
    self.nodes = {'k':0,'j':0}
    self.ncurrents = 0
    self.k = dev['k']
    self.j = dev['j']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    pos = '(' + str(self.val) + '*s)'
    neg = '-'  + pos
    if self.k != 0:
      mat[self.k-1][self.k-1] = self.add_val(mat[self.k-1][self.k-1], pos)
      if self.j != 0:
        mat[self.k-1][self.j-1] = self.add_val(mat[self.k-1][self.j-1],neg)
    if self.j != 0:
      mat[self.j-1][self.j-1] = self.add_val(mat[self.j-1][self.j-1], pos)
      if self.k != 0:
        mat[self.j-1][self.k-1] = self.add_val(mat[self.j-1][self.k-1], neg)
    return mat

# ******************************
# Inductor Stamp
# ******************************
class L_Stamp(Stamp_Base):
  # example device
  #{'type':'L', 'k':1, 'j':0, 'val':'L1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 2
    self.nodes = {'k':0,'j':0}
    self.ncurrents = 0
    self.k = dev['k']
    self.j = dev['j']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)
  
  def stamp(self, mat):
    pos = '1/(' + str(self.val) + '*s)'
    neg = '-'  + pos
    if self.k != 0:
      mat[self.k-1][self.k-1] = self.add_val(mat[self.k-1][self.k-1], pos)
      if self.j != 0:
        mat[self.k-1][self.j-1] = self.add_val(mat[self.k-1][self.j-1],neg)
    if self.j != 0:
      mat[self.j-1][self.j-1] = self.add_val(mat[self.j-1][self.j-1], pos)
      if self.k != 0:
        mat[self.j-1][self.k-1] = self.add_val(mat[self.j-1][self.k-1], neg)

    return mat

# ******************************
# Current Source Stamp
# ******************************
class I_Stamp(Stamp_Base):
  # example device
  #{'type':'I', 'k':0, 'j':1, 'val':'I1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 2
    self.nodes = {'k':0,'j':0}
    self.ncurrents = 0
    self.k = dev['k']
    self.j = dev['j']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)
  
  def stamp(self, mat):
    if type(self.val) is str:
      pos = self.val
      neg = '-'  + pos
    else:
      pos = self.val
      neg = -1*pos
    if self.k != 0:
      mat[self.k-1][-1] = self.add_val(mat[self.k-1][-1], neg)

    if self.j != 0:
      mat[self.j-1][-1] = self.add_val(mat[self.j-1][-1], pos)

    return mat

# ******************************
# OP Amp Stamp
# ******************************
class O_Stamp(Stamp_Base):
  # example device
  #{'type':'O', 'p':1, 'n':2, 'o':3, 'val':'A1|inf'}
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 3
    self.nodes = {'p':0,'n':0, 'o':0}
    self.ncurrents = 1
    self.p = dev['p']
    self.n = dev['n']
    self.o = dev['o']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    if type(self.val) is str:
      pos = self.val
      neg = '-'  + pos
    else:
      pos = self.val
      neg = -1*pos
    if pos == 'inf':
      # Ideal Infinite Gain Op Amp
      if self.p != 0:
        mat[self.l][self.p-1] = self.add_val(mat[self.l][self.p-1], 1)
      if self.n != 0:
        mat[self.l][self.n-1] = self.add_val(mat[self.l][self.n-1], -1)
      mat[self.o-1][self.l] = self.add_val(mat[self.o-1][self.l], 1)
    else:
      # E Model with Finite Gain and j node grounded
      if self.o != 0:
        mat[self.l][self.o-1] = self.add_val(mat[self.l][self.o-1], 1)
        mat[self.o-1][self.l] = self.add_val(mat[self.o-1][self.l], 1)
      if self.p != 0:
        mat[self.l][self.p-1] = self.add_val(mat[self.l][self.p-1], neg)
      if self.n != 0:
        mat[self.l][self.n-1] = self.add_val(mat[self.l][self.n-1], pos)
    return mat

# ******************************
# Voltage Source Stamp
# ******************************
class V_Stamp(Stamp_Base):
  # example device
  #{'type':'V', 'k':0, 'j':1, 'val':'V1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 2
    self.nodes = {'k':0,'j':0}
    self.ncurrents = 1
    self.k = dev['k']
    self.j = dev['j']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    if self.k != 0:
      mat[self.l][self.k-1] = self.add_val(mat[self.l][self.k-1], 1)
      mat[self.k-1][self.l] = self.add_val(mat[self.k-1][self.l], 1)
    if self.j != 0:
      mat[self.l][self.j-1] = self.add_val(mat[self.l][self.j-1], -1)
      mat[self.j-1][self.l] = self.add_val(mat[self.j-1][self.l], -1)
    mat[self.l][-1] = self.add_val(mat[self.l][-1], self.val)
    return mat

# ******************************
# VCVS Stamp
# ******************************
class E_Stamp(Stamp_Base):
  # example device
  #{'type':'E', 'k':0, 'j':1, 'p':2, 'q':3, 'val':'mu1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 4
    self.nodes = {'k':0,'j':0, 'p':0, 'q':0}
    self.ncurrents = 1
    self.k = dev['k']
    self.j = dev['j']
    self.p = dev['p']
    self.q = dev['q']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    if type(self.val) is str:
      pos = self.val
      neg = '-'  + pos
    else:
      pos = self.val
      neg = -1*pos
    if self.k != 0:
      mat[self.l][self.k-1] = self.add_val(mat[self.l][self.k-1], 1)
      mat[self.k-1][self.l] = self.add_val(mat[self.k-1][self.l], 1)
    if self.j != 0:
      mat[self.l][self.j-1] = self.add_val(mat[self.l][self.j-1], -1)
      mat[self.j-1][self.l] = self.add_val(mat[self.j-1][self.l], -1)
    if self.p != 0:
      mat[self.l][self.p-1] = self.add_val(mat[self.l][self.p-1], neg)
    if self.q != 0:
      mat[self.l][self.q-1] = self.add_val(mat[self.l][self.q-1], pos)
    return mat
# ******************************
# CCVS Stamp
# ******************************
class H_Stamp(Stamp_Base):
  # example device
  #{'type':'H', 'k':0, 'j':1, 'p':2, 'q':3, 'val':'H1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 4
    self.nodes = {'k':0,'j':0, 'p':0, 'q':0}
    self.ncurrents = 2
    self.k = dev['k']
    self.j = dev['j']
    self.p = dev['p']
    self.q = dev['q']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    if type(self.val) is str:
      pos = self.val
      neg = '-'  + pos
    else:
      pos = self.val
      neg = -1*pos
    l1 = self.l[0]
    l2 = self.l[1]
    if self.k != 0:
      mat[l1][self.k-1] = self.add_val(mat[l1][self.k-1], 1)
      mat[self.k-1][l1] = self.add_val(mat[self.k-1][l1], 1)
    if self.j != 0:
      mat[l1][self.j-1] = self.add_val(mat[l1][self.j-1], -1)
      mat[self.j-1][l1] = self.add_val(mat[self.j-1][l1], -1)
    if self.p != 0:
      mat[self.p-1][l2] = self.add_val(mat[self.p-1][l2], 1)
      mat[l2][self.p-1] = self.add_val(mat[l2][self.p-1], 1)
    if self.q != 0:
      mat[self.q-1][l2] = self.add_val(mat[self.q-1][l2], -1)
      mat[l2][self.q-1] = self.add_val(mat[l2][self.q-1], -1)
    
    mat[l1][l2] = self.add_val(mat[l1][l2], neg)

    return mat
# ******************************
# Ideal Transformer Stamp
# ******************************
class X_Stamp(Stamp_Base):
  # example device
  #{'type':'X', 'p1':0, 'n1':1, 'p2':2, 'n2':3, 'val':'n'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 4
    self.nodes = {'p1':0,'n1':0, 'p2':0, 'n2':0}
    self.ncurrents = 3
    self.p1 = dev['p1']
    self.n1 = dev['n1']
    self.p2 = dev['p2']
    self.n2 = dev['n2']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    if type(self.val) is str:
      pos = self.val
      neg = '-'  + pos
    else:
      pos = self.val
      neg = -1*pos
    x1 = self.l[0]
    If = self.l[1]
    Ie = self.l[2]
    if self.p1 != 0:
      mat[self.p1-1][If] = self.add_val(mat[self.p1-1][If], neg)
      mat[Ie][self.p1-1] = self.add_val(mat[Ie][self.p1-1], neg)
    if self.n1 != 0:
      mat[self.n1-1][If] = self.add_val(mat[self.n1-1][If], pos)
      mat[Ie][self.n1-1] = self.add_val(mat[Ie][self.n1-1], pos)
    if self.p2 != 0:
      mat[self.p2-1][If] = self.add_val(mat[self.p2-1][If], 1)
      mat[If][self.p2-1] = self.add_val(mat[If][self.p2-1], 1)
    if self.n2 != 0:
      mat[self.n2-1][Ie] = self.add_val(mat[self.n2-1][Ie], -1)
      mat[Ie][self.n2-1] = self.add_val(mat[Ie][self.n2-1], -1)
    
    mat[x1][If] = self.add_val(mat[x1][If], -1)
    mat[x1][Ie] = self.add_val(mat[x1][Ie], 1)
    mat[If][x1] = self.add_val(mat[If][x1], -1)
    mat[Ie][x1] = self.add_val(mat[Ie][x1], 1)
    return mat
# ******************************
# CCCS Stamp
# ******************************
class F_Stamp(Stamp_Base):
  # example device
  #{'type':'F', 'k':0, 'j':1, 'p':2, 'q':3, 'val':'b1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 4
    self.nodes = {'k':0,'j':0, 'p':0, 'q':0}
    self.ncurrents = 1
    self.k = dev['k']
    self.j = dev['j']
    self.p = dev['p']
    self.q = dev['q']
    self.val = dev['val']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    if type(self.val) is str:
      pos = self.val
      neg = '-'  + pos
    else:
      pos = self.val
      neg = -1*pos
    if self.k != 0:
      mat[self.k-1][self.l] = self.add_val(mat[self.k-1][self.l], pos)

    if self.j != 0:
      mat[self.j-1][self.l] = self.add_val(mat[self.j-1][self.l], neg)

    if self.p != 0:
      mat[self.p-1][self.l] = self.add_val(mat[self.p-1][self.l], 1)
      mat[self.l][self.p-1] = self.add_val(mat[self.l][self.p-1], 1)

    if self.q != 0:
      mat[self.q-1][self.l] = self.add_val(mat[self.q-1][self.l], -1)
      mat[self.l][self.q-1] = self.add_val(mat[self.l][self.q-1], -1)

    return mat

# ******************************
# VCCS Stamp
# ******************************
class G_Stamp(Stamp_Base):
  # example device
  #{'type':'G', 'k':0, 'j':1, 'p':2, 'q':3, 'val':'g1'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 4
    self.nodes = {'k':0,'j':0, 'p':0, 'q':0}
    self.ncurrents = 0
    self.k = dev['k']
    self.j = dev['j']
    self.p = dev['p']
    self.q = dev['q']
    self.val = dev['val']    
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    if type(self.val) is str:
      pos = self.val
      neg = '-'  + pos
    else:
      pos = self.val
      neg = -1*pos
    if self.k != 0 and self.p != 0:
      mat[self.k-1][self.p-1] = self.add_val(mat[self.k-1][self.p-1], pos)
    if self.k != 0 and self.q != 0:
      mat[self.k-1][self.q-1] = self.add_val(mat[self.k-1][self.q-1], neg)
    if self.j != 0 and self.p != 0:
      mat[self.j-1][self.p-1] = self.add_val(mat[self.j-1][self.p-1], neg)
    if self.j != 0 and self.q != 0:
      mat[self.j-1][self.q-1] = self.add_val(mat[self.j-1][self.q-1], pos)
    return mat

# ******************************
# Mosfet Stamp
# ******************************
class M_Stamp(Stamp_Base):
  # example device
  #{'type':'M', 'd':0, 'g':1, 's':2, 'ro':'ro', 'gm':'gm', 'cgs':'cgs', 'cgd':'cgd'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 3
    self.nodes = {'d':0,'g':0, 's':0}
    self.ncurrents = 0
    self.d = dev['d']
    self.g = dev['g']
    self.s = dev['s']
    self.ro = dev['ro']
    self.gm = dev['gm']
    self.cgs = dev['cgs']
    self.cgd = dev['cgd']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    m_nets = [
    {'type':'G', 'k':self.d, 'j':self.s, 'p':self.g, 'q':self.s, 'val':self.gm},
    ]
    if self.ro != 'inf':
      m_nets.append({'type':'R', 'k':self.d, 'j':self.s, 'val':self.ro})
    if self.cgs != 0:
      m_nets.append({'type':'C', 'k':self.g, 'j':self.s, 'val':self.cgs})
    if self.cgd != 0:
      m_nets.append({'type':'C', 'k':self.g, 'j':self.d, 'val':self.cgd})

    m_stamps = compile_stamps(m_nets)
    return apply_stamps(m_stamps, mat)

# ******************************
# BJT Stamp
# ******************************
class B_Stamp(Stamp_Base):
  # example device
  #{'type':'B', 'c':0, 'b':1, 'e':2, 'ro':'ro', 'beta':'beta', 'gm':'gm', 'cbe':'cbe', 'cbc':'cbc'},
  def __init__(self, dev):
    self.dev = dev
    self.nnodes = 3
    self.nodes = {'c':0,'b':0, 'e':0}
    self.ncurrents = 0
    self.c = dev['c']
    self.b = dev['b']
    self.e = dev['e']
    self.ro = dev['ro']
    self.gm = dev['gm']
    self.beta = dev['beta']
    self.cbe = dev['cbe']
    self.cbc = dev['cbc']
    self.parse_nodes(dev, self.nodes)

  def stamp(self, mat):
    b_nets = [
    {'type':'G', 'k':self.c, 'j':self.e, 'p':self.b, 'q':self.e, 'val':self.gm},
    ]
    if self.ro != 'inf':
      b_nets.append({'type':'R', 'k':self.c, 'j':self.e, 'val':self.ro})    
    if self.beta != 'inf':
      self.rpi = '(' + str(self.beta) + '/' + str(self.gm) + ')'
      b_nets.append({'type':'R', 'k':self.b, 'j':self.e, 'val':self.rpi})
    if self.cbe != 0:
      b_nets.append({'type':'C', 'k':self.b, 'j':self.e, 'val':self.cbe})
    if self.cbc != 0:
      b_nets.append({'type':'C', 'k':self.b, 'j':self.c, 'val':self.cbc})

    b_stamps = compile_stamps(b_nets)
    return apply_stamps(b_stamps, mat)

def apply_stamps(stamps, mat):
  for i in range(len(stamps)):
    mat = stamps[i].stamp(mat)
  return mat
     
# Global Stamp lookup (for compiling)
stamp_lu = {
'R' : R_Stamp,
'C' : C_Stamp,
'L' : L_Stamp,
'I' : I_Stamp,
'O' : O_Stamp,
'V' : V_Stamp,
'E' : E_Stamp,
'F' : F_Stamp,
'H' : H_Stamp,
'G' : G_Stamp,
'X' : X_Stamp,
'M' : M_Stamp,
'B' : B_Stamp
}

def compile_stamps(netlist):
  stamps = []
  for dev in netlist:
    stamps.append(stamp_lu[dev['type']](dev))
  return stamps

