from isogeny_computations.torsion_handle import Isogeny_Recomputation
import galois as gs
import random
from sage.all import GF
from time import time


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
This function distributes the secret shares to the participants.
The secrets are define by symbols in a codeword.
"""
def secret_symbol_sharing(r, b_chain, n):

    if len(b_chain) % r != 0:
        raise ValueError("Extension degree should divide the bit length")

    F2r = gs.GF(2**r)
    "Defining a basis of F2^r over F2"
    bs = [F2r.primitive_element**i for i in range(r)]
    #print(bs)

    #Representing an element in a polynomial basis
    x     = F2r.Random()
    poly  = F2r.irreducible_poly
    print(f"Is the polynomial irreducible?", poly.is_irreducible())
    print(x, poly)
    x_bin = x.vector()
    print(f"The binary representation of {x} is ", x_bin)

    #Representing the bit chain as symbols in F2r
    b_blocks = create_blocks(b_chain, r)
    print(b_blocks)
    symbols = []
    for  bk in b_blocks:
        #s0_bin = b_blocks[0]
        #print(bk)
        sym = F2r.Vector(bk)
        symbols.append(sym)
    print(f"the symbols corresponding to {b_chain} are {symbols}")

    #At this point we can use an RS code to encode the symbols
    RScode = symbols # to be coded
    
    #Sharing the secret symbols from codeword to the participants
    gamma       = int(len(RScode)/n)
    secrets     = create_blocks(RScode, gamma)

    #Dictionary that stock the index of participants and their secrets"
    dic_secrets = {}
    index = 0
    for sec in secrets:
        dic_secrets[index] = sec
        index += 1
    # print(dic_secrets)

"""
Secret bit chain recovery using threshold t. 
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
    #print(error_code)

    "At this point we can use the fficient decoding algorithm of Tang and Han RS to correct the erasures"
    rs_code = error_code # Correction process, to be coded.
    rs_word = rs_code # Decoding process, to be coded.

    "Mapping the symbols back to bit string"
    b_chain = []
    for w in rs_word:
        bin_w = w.vector()
        b_chain.extend(bin_w)
    #print(b_chain)

    return b_chain


"""
In this function we give a formal measurement of the time needed for decoding long or medium size
codes that fit the framework of our scheme. We follow Table III of 
N. Tang and Y. S. Han, “A new decoding method for Reed-Solomon codes based on FFT and modular approach,” 
To measure the timing of decoding. To the best of our knowledge the implementation of the algorithms of Tang and Han
is not avalaible. This is a formal verification that shows that the cost of the decoding 
process is negligible in our scheme. As we must in the manuscrit the bulk of our computations 
is dominated by Line 23 of Algorithm 2, that deals with isogeny computation in higher dimension.
We mainly focus on the implementation of this algorithms to evaluate the running time of our algoruthms.
"""
def FMA_decode_time():
    F12 = GF(2**12, name ='x')    
    a = F12.random_element() 
    while a == 0 or a == 1: 
        a = F12.random_element()
    b = F12.random_element() 
    while b == 0 or b == 1: 
        b = F12.random_element()    
    print(f"The numbers to multiply or add or divide are {a} and {b}")

    #Timing for multiplications
    t0 = time()      
    for i in range(0, 413185):
        prod = a*b 
    Tmult = time()  
    tmp0 = Tmult - t0  
    print(f"The running time for multiplications is {tmp0:.8f} seconds") 
    

    #Timing for additions
    for i in range(0, 573437):
        add = a+b     
    Tadd =  time()
    tmp1 = Tadd - Tmult
    print(f"The running time for additions is {tmp1:.8f} seconds")  
    
    
    #Timing for divisions
    for i in range(0, 257):
        div = a / b
    Tdiv =  time()
    tmp2 = Tdiv - Tadd 
    print(f"The running time for divisions is {tmp2:.8f} seconds") 
    

    print(f"The overall running time for RS decoding using FMA approach is {tmp0 + tmp1 + tmp2:.8f} seconds")


"""
Recover the isogeny using corresponding torsion bit chain
As in the other functions in the package, we compute two torsion bases in E1.
So the funtion takes two chains corresponding to the bases and their images in E2.
"""
def recover_shared_isogeny(A_chain, B_chain, E1, E2, params):   
    #We concatenated 4 points given by the bases and their images
    torsion_bitsA = create_blocks(A_chain, 4) 
    torsion_bitsB = create_blocks(B_chain, 4)

    #Recover the torsion points using the inverse of SESS"
    PA    = SESSinv(E1, torsion_bits[0])
    im_PA = SESSinv(E2, torsion_bits[1])
    QA    = SESSinv(E1, torsion_bits[2])    
    im_QA = SESSinv(E2, torsion_bits[3])
    PB    = SESSinv(E1, torsion_bits[0])
    im_PB = SESSinv(E2, torsion_bits[1])
    QA    = SESSinv(E1, torsion_bits[2])    
    im_QA = SESSinv(E2, torsion_bits[3])

    #Definition of the input for the isogeny recomputation
    E1_params = (E1,PA,QA,PB,QB)
    imgA = (E2,im_PA,im_QA)
    imgB = (E2,im_PB,im_QB)
    #Recomputation of the corresponding isogeny
    Iso_secret = Isogeny_Recomputation(params,E1_params,imgA,imgB,EAB=None)

    return Iso_secret
    

