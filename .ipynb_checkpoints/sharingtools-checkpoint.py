import galois as gs
import random

"""
Suitable primes for the scheme
"""

"""
Slicing bits and symbols into blocks
"""
def create_blocks(chain, block_size):
    list_block = []
    for i in range(0, len(chain), block_size):
        block_i = chain[i:i + block_size]
        list_block.append(block_i)
    #for block in list_block: print(block)
    
    return list_block 

"""
Finite fields, RS code, and bits sharing
"""
def secret_symbol_sharing(r, b_chain, n):

    if len(b_chain) % r != 0:
        raise ValueError("Extension degree should divide the bit length")

    F2r = gs.GF(2**r)
    "Defining a basis of F2^r over F2"
    bs = [F2r.primitive_element**i for i in range(r)]
    #print(bs)

    "Representing an element in a polynomial basis"
    x     = F2r.Random()
    poly  = F2r.irreducible_poly
    print(f"Is the polynomial irreducible?", poly.is_irreducible())
    print(x, poly)
    x_bin = x.vector()
    print(f"The binary representation of {x} is ", x_bin)

    "Representing the bit chain as symbols in F2r"
    b_blocks = create_blocks(b_chain, r)
    print(b_blocks)
    symbols = []
    for  bk in b_blocks:
         #s0_bin = b_blocks[0]
        print(bk)
        sym = F2r.Vector(bk)
        symbols.append(sym)
    print(f"the symbols corresponding to {b_chain} are {symbols}")

    "Using RS code to encode the symbols"
    RScode = symbols # to be coded
    
    "Sharing the secret code to the participants"
    gamma       = int(len(RScode)/n)
    secrets     = create_blocks(RScode, gamma)
    #Dictionary that stock the index of participant and its secret
    dic_secrets = {}
    index = 0
    for sec in secrets:
        dic_secrets[index] = sec
        index += 1
    print(dic_secrets)

"""
Secret bit chain recovery using threshold t
"""
def secret_bit_recovery(dic_thresh_sec, n, F2r):
    t = len(dic_thresh_sec)
    if t > n or t < 1:
        raise ValueError("The threshold is not well defined")
    r     = F2r.degree
    gamma = len(random.choice(list(dic_thresh_sec.values())))
    #Adding erasures
    error_code = []
    for i in range(n):
        if i in dic_thresh_sec:
            error_code.append(dic_thresh_sec[i])
        elif i not in dic_thresh_sec:
            erasure = [F2r.Random() for _ in range(gamma)]
            error_code.append(erasure)
    print(error_code)

    "Using RS to correct the erasures"
    rs_code = error_code # To correct later
    rs_word = rs_code # To decode later

    "Mapping the symbols back to bit string"
    b_chain = []
    for w in rs_word:
        bin_w = w.vector()
        b_chain.extend(bin_w)
    #print(b_chain)

    return b_chain

"""
Recover the isogeny using corresponding torsion bit chain
"""
def recover_sharedd_isogeny(b_chain):    
    torsion_bits = create_blocks(b_chain, 4)#We concatenated 4 points

    "Recover the torsion points using SESS"
    #P    = SESSinv(E0, torsion_bits[0])
    #im_P = SESSinv(E1, torsion_bits[1])
    #Q    = SESSinv(E0, torsion_bits[2])    
    #im_Q = SESSinv(E1, torsion_bits[3])
    


"""
Testing the functions
"""
b_chain = [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1,
           0, 0, 1, 0, 0, 1, 1, 0, 1]
r = 3; n = 4
