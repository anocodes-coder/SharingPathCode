"""
suitable_prime_deepsearch(r) --> return prime p = 2^e3^f-1 with E/Fp^2
                                 and size(p) ~ r2^{r-4}
"""


import math as mt
import sympy as sp


"We use triple-extended RS that are MDS codes [2^r+2, 3, 2^r] of Theo 6"

   

""" Maximum number that divide an integer """
def proper_divisor(n):
    list_divisors = []
    for i in range (2, n):
        if n % i == 0:
            list_divisors.append(i)
    return list_divisors

""" Order of multiplicity """
def order_mult(n, p):
    if sp.isprime(p) == False:
        raise ValueError("We must have a prime number")
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count

""" Search for a prime p = 2^e3^f -1 """
def prime_specific_form(a, b):
    #possible_p = list(sp.primerange(a, b))
    for p in sp.primerange(a, b):        
        #print(sp.primefactors(p+1))
        print(p)
        if (p+1)%3 != 0:
            continue
        #dic_p = sp.factorint(p+1), very slow
        e = order_mult(p+1, 2)
        f = order_mult(p+1, 3)
        if ((2**e)*(3**f) - 1) == p:
            return p
        return False

""" Looking for a suitable prime number """
def suitable_prime(r):
    if r < 3:
        return "Operation impossible"
    #if we concatenate 4 points and consider E/Fp^2,
    #we can work with size(p) <= 3072, for r <= 12.
    size_p = r*2**(r-4) 
    low_p  = 2**(size_p - 1)
    high_p = 2**size_p - 1
    #p      = sp.randprime(low_p, high_p+1)
    #p, dic_p = prime_specific_form(low_p, high_p)

    """Another way to find the prime
    for i in range(low_p, high_p+1):
        if sp.isprime(i):
            p = i
            break"""
        
    return size_p, prime_specific_form(low_p, high_p)

#With this function we get p of size 6655 with r = 13, e=298, and f = 4011
def suitable_prime_deepsearch(r):
    if r < 4:
        raise ValueError("Operation impossible")
    size_p = r*2**(r-4)
    f = 1
    while (size_p - mt.log2(3)*f) > 0:
        e = int(size_p - mt.log2(3)*f)
        p = (2**e)*(3**f)-1
        if sp.isprime(p):
            print(f"(e, f) = ", (e, f))
            return e, f, mt.ceil(mt.log2(p))
        f += 1
    return False
    
    


        

"Subfield code and FF parameters given (n, t, sec)"
def sub_code_parameters(max_ext_deg):
    #List of possible number of participants using triple extended RS code
    list_ban_degs = []
    for r in range(2, max_ext_deg+1):
        ls = proper_divisor(2**r+2)
        #To exclude some degrees we consider Nist I.
        if int( (2**r-126) / ls[0] ) < 2:
            list_ban_degs.append(r)
            continue
        print("Using GF(2^%s) \n we can have at most %s participants" % (r, ls[-1]))
        print(ls)
        print("There are %s possible gamma" % int(len(ls)/2))
        tmaxI = int( (2**r-126) / ls[0] ) + 1 # The min ls[0] gamma gives the max t. 
        tmaxIII = int( (2**r-190) / ls[0] ) + 1
        tmaxV = tmax = int( (2**r-254) / ls[0] ) + 1
        #print("For Nist Level I, III, and V the threshold t is respectively less than %s, %s, %s" % (tmaxI, tmaxIII, tmaxV))
    print("Note: For security reason, we can't work with the following degrees %s" % list_ban_degs)

    #print("for the given maximum extension the better choice is GF(2^%s)")

    return "End"

def binrs_code_parameters(max_ext_deg):
    max_bin_cod_len = (max_ext_deg+1)*((2**max_ext_deg)+2)
    for r in range(2, max_ext_deg+1):
        bin_cod_len = (r+1)*((2**r)+2)
        ls = proper_divisor(bin_cod_len)
        "Possibible gamma < r+2"
        tabGams = []
        for g in ls:
            if g < r+2:
                tabGams.append(g)
            elif g >= r+2:
                break
        print("Using GF(2^%s) \n we can have at most %s participants" % (r, ls[-1]))
        print("Possible gamma %s" % len(tabGams))
        print(ls)       

        "With Elligator the bit length ~ log2(p) for E(Fp) which is ~ (bin_cod_len)/2"
        #fp_size = int(bin_cod_len / 2)
        #p = sympy.randprime(2**(fp_size - 1), 2**fp_size)
        #print("We define a supersingular EC over GF(%s)" %p)

    return max_bin_cod_len
       

"""RS code and FF parameters given extension degrees and security level"""
def rs_code_pamameters(max_ext_deg, lsec):

    for r in range(2, max_ext_deg+1):
        rst_cod_len = 2**r+2
        tab_gams_parts = proper_divisor(rst_cod_len)
        #note that n*gamma = rst_cod_len and t >0.
        #To exclude degs we consider any security level 
        ban_degs = []
        if int((r*(2**r+2)-lsec) / tab_gams_parts[0]) < 1:
            ban_degs.append(r)
            continue
        tmax = int((r*(2**r+2)-lsec) / tab_gams_parts[0]) +1
        print("Using GF(2^%s) \n we can have at most %s participants" % (r, tab_gams_parts[-1]))
        #print("For the security level %s the threshold t is less than %s " % (lsec, tmax))
        
        "With Elligator the bit length ~ log2(p) for E(Fp) which is ~ (bin_cod_len)/2"

        
                                   
    return ban_degs
                

"Triple extended RS Code and FF parameters given (n, t)"
def code_parameters(n, t):
    RScodeMinDist = 2*(n-t)+1
    while math.log2(RScodeMinDist).is_integer() == False or bin_cod_len % n != 0:
        RScodeMinDist = RScodeMinDist+1
        if math.log2(RScodeMinDist).is_integer() == True:
            ext_deg = int(math.log2(RScodeMinDist))
            bin_cod_len = (ext_deg+1)*((2**ext_deg)+2)
    #ext_deg = int(math.log2(RScodeMinDist))
    print("We use an tripled extended RS code over\n GF(2^%s)" % ext_deg )
    bin_cod_len = (ext_deg+1)*((2**ext_deg)+2)
    print("The binary representation of the RS code has length: %s" % bin_cod_len)
    Gamma = int(bin_cod_len / n) 
    print("The sharing bits function uses %s" % Gamma)
    if Gamma >= ext_deg + 2:
        print ("The chosen parameters do not work")
        #return 0
        
    return RScodeMinDist #, PossibleGamValues

       
        
"Values of affected symboles in RS(2^r, d) code extending binary code C+"
"Following Theorem 7 we consider epsilon > 1 to avoid gamma = 1"
"triple-extended RS that are MDS codes [2^r+2, 3, 2^r] of Theo 6"
def epsilon_values(ext_deg):
    #Possible code length gamma*n
    RScodeMinDist = 2**ext_deg
    NumParts = []
    bin_cod_len = (ext_deg+1)*((2**ext_deg)+2)
    GamNumpartElts = [i for i in range (2, bin_cod_len) if bin_cod_len % i == 0]
    #num_participants.append((deg_ext+1)*((2**deg_ext)-1))
    #Possible values of \gamma depending on \epsilon
    PossibleGamValues = [i for i in range(2, ext_deg+2) if i in GamNumpartElts ]
    PossibleNumpartValues = []
    for i in PossibleGamValues:
        PossibleNumpartValues.append(int(bin_cod_len / i))
    
    return bin_cod_len, PossibleGamValues, PossibleNumpartValues

    
    
    
