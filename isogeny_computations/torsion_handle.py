from sage.all import *
from time import time
from basis_change.canonical_basis_dim1 import make_canonical
from Tests import random_walk
from utilities.strategy import precompute_strategy_with_first_eval
from utilities.supersingular import torsion_basis, weil_pairing_pari
from utilities.discrete_log import ell_discrete_log_pari
from utilities.order import has_order_D
from isogenies.Kani_endomorphism import KaniEndoHalf
from theta_structures.Tuple_point import TuplePoint
from montgomery_isogenies.isogenies_x_only import isogeny_from_scalar_x_only, evaluate_isogeny_x_only, random_isogeny_x_only


"""
Given the parameters of the finite field over which we want to define an 
appropriate supersingular elliptic curve, this function returns torsion 
point bases and their images under the secret isogeny. These points can later 
be used to recompute the secret isogeny. In our scheme, they represent the 
parameters given to the dealer. Through a coding process, he generates shared 
secrets for the participants.
"""
def Sharing_Data_Computation(params):
	t1=time()
	print("**************************")
	print("# Dealer Data Generation #")
	print("**************************\n")

	print("We use the following public parameters:")
	print("+ Initial curve  --> E1.")
	print("+ Curve codomain --> EA.")
	print("+ Finite Field   --> F_p^2.\n")

    #Finite Field Definition
	e2=params['e2']
	e3=params['e3']
	p=2**e2*3**e3-1
	Fp2=GF(p**2,'i',modulus=[1,0,1],proof=False)	

	# Definition of the initial curve E1
	E0=EllipticCurve(Fp2,[1,0])
	E1=random_walk(E0,ZZ(2**(e2-1)*3**(e3-1)))	

	# We compute two torsion points bases for two large integers NA and NB.
	NA=ZZ(2**e2)
	NB=ZZ(3**e3)
	PA,QA=torsion_basis(E1,NA)
	PA,QA,_,_,_=make_canonical(PA,QA,NA)
	PB,QB=torsion_basis(E1,NB)
    # <PA, QA> and <PB, QB> are secret torsions basis of E1[NA] and E1[NB].
	E1_params=(E1,PA,QA,PB,QB)	

	#Computation of a secret isogeny, the codomain EA, and the images of PB and QB.
	sa=randint(0,NA-1)
	phiA, EA=isogeny_from_scalar_x_only(E1, NA, sa, basis=(PA,QA))	

	t2=time()
	print("Parameter generation time: {} s\n".format(t2-t1))
	

	print("# !!! The parameters given to the dealer are !!! #")
	print("--------------------------------------------------\n")
	print(f"The first torsion point P:")
	print(f"{PA}\n")
	print(f"The second torsion point Q:")
	print(f"{QA}\n")
	#print(f"{E1}\n")
	#print(f"{EA}\n")
	print("The 2**e-isogeny I: E1-->EA:")
	print(f"{phiA}\n")	
	phiA_PB,phiA_QB=evaluate_isogeny_x_only(phiA, PB, QB, NB, NA)
	print(f"The image of the first torsion point I(P):")
	print(f"{phiA_PB}\n")
	print(f"The image of the second torsion point I(Q):")
	print(f"{phiA_QB}\n")

	# Public codomain and secret images
	imgA=(EA,phiA_PB,phiA_QB)
	dealer_data_A = [PB, QB, phiA_PB, phiA_QB] # secret data  

	t3=time()
	print("Dealer Protocol time: {} s".format(t3-t2))

	# We can also compute another secret isogeny phiB : E1 --> EB using NB
	sb=randint(0,NB-1)
	phiB, EB=isogeny_from_scalar_x_only(E1, NB, sb, basis=(PB,QB))
	phiB_PA,phiB_QA=evaluate_isogeny_x_only(phiB, PA, QA, NA, NB)
	imgB=(EB,phiB_PA,phiB_QA)
	dealer_data_B = [PA, QA, phiB_PA, phiB_QA] # other possible secret data  

	#Computation of optional curves EAB and EBA of same j-invariant.
	psiA,EBA=isogeny_from_scalar_x_only(EB, NA, sa, basis=(phiB_PA,phiB_QA))
	psiB,EAB=isogeny_from_scalar_x_only(EA, NB, sb, basis=(phiA_PB,phiA_QB))

	return E1_params,imgA,imgB,EAB



"""
!!! In the input, we have the necessary information to recompute a secret isogeny !!!
       + params gives the finite field over which the elliptic curves are defined.
       + E1_params contains the initial curve E1 and the torsion points.
       + imgA and imgB represent the images of the torsion points.
       + EAB is optional in the context of our scheme.
"""
def Isogeny_Recomputation(params,E1_params,imgA,imgB,EAB=None):
	t1=time()
	print("********************************************")
	print("# Recovering the Isogeny using SIDH Attack #")
	print("********************************************\n")
	
	E1,PA,QA,PB,QB=E1_params
	EA,phiA_PB,phiA_QB=imgA
	EB,phiB_PA,phiB_QA=imgB

    #Finite fields and embedding degrees parameters
	e2=params['e2']
	e3=params['e3']
	e=params['e']
	a1=params['a1']
	a2=params['a2']

	# Degree of secret isogeny to recover and torsion image
	if e3%2==1:
		q=3**e3
		phipB_PA=phiB_PA
		phipB_QA=phiB_QA
		EBp=EB
	else:
		# Tweaking of the secret isogeny by adding a 3-isogeny
		q=3**(e3+1)
		psi,EBp=random_isogeny_x_only(EB,3)
		phipB_PA,phipB_QA=evaluate_isogeny_x_only(psi, phiB_PA, phiB_QA, ZZ(2**e2), 3)

	assert q+a1**2+a2**2==2**e

	# m=max(v_2(a1),v_2(a2))
	if a1%2==0:
		ai_div=a1
	else:
		ai_div=a2

	ai_div=ai_div//2
	m=1
	while ai_div%2==0:
		ai_div=ai_div//2
		m+=1
	
	f1=ceil(e/2)
	f2=e-f1

    #print("# !!! Precomputation and dimension 4 embedding phases !!! #")
	#print("---------------------------------------------------------\n")

	# Strategy of precomputation	
	strategy1=precompute_strategy_with_first_eval(f1,m,M=1,S=0.8,I=100)
	if f2==f1:
		strategy2=strategy1
	else:
		strategy2=precompute_strategy_with_first_eval(f2,m,M=1,S=0.8,I=100)   		
	t2=time()
	print("Precomputation Time ----> {} s".format(t2-t1))

	# Strategy of embedding in high dimension
	F=KaniEndoHalf(PA,QA,phipB_PA,phipB_QA,q,a1,a2,e,e2,strategy1,strategy2)
	t3=time()
	print("Embedding Time   ----> {} s".format(t3-t2))


    #print("# !!! Isogeny evaluation and discret log computation phases !!! #")
	#print("------------------------------------------------------------\n")

	# Evaluation process
	T=TuplePoint(PB,E1(0),EBp(0),EBp(0))
	FT=F(T)
	phipB_PB=FT[2]

	U=TuplePoint(QB,E1(0),EBp(0),EBp(0))
	FU=F(U)
	phipB_QB=FU[2]

	t4=time()
	print("Evaluation of Isogeny Time ----> {} s ".format(t4-t3))

	# DL computations
	NB=ZZ(3**e3)
	backtrack=False
	if (NB//3)*phipB_QB!=EBp(0):
		sb=ell_discrete_log_pari(EBp,phipB_PB,phipB_QB,NB)
	else:
		backtrack=True
		sb=ell_discrete_log_pari(EBp,phipB_PB,phipB_QB,ZZ(NB//3))
	t5=time()
	print("DL computational Time ----> {} s \n".format(t5-t4))	

	# Find the correct sb
	if backtrack:
		# sb determined modulo NB//3=3**(e3-1) and up to a sign
		sb_candidates=[sb,-sb,sb+NB//3,-sb+NB//3,sb+2*NB//3,-sb+2*NB//3]
	else:
		# sb determined modulo NB=3**e3 up to a sign
		sb_candidates=[sb,-sb]

	print(" # !!! Codomain recovery and isogeny recomputation phases !!! #")
	print("------------------------------------------------------------\n")	

	found_sb=False
	for s in sb_candidates:
		Iso_secret, EC=isogeny_from_scalar_x_only(E1, NB, s, basis=(PB,QB))
		if EC.j_invariant()==EB.j_invariant():
			found_sb=True
			sb=s
			break
	t6=time()	
	print("Is the codomain curve recovered?")
	print(found_sb)
	print("Time to recompute the secret isogeny ---->  {} s\n".format(t6-t5))
    
	print("Through recomputation, we found the following isogeny: ")
	print(f"{Iso_secret}\n")

	t7=time()
	print("Total time of recovery process ----> {} s".format(t7-t1))

	return Iso_secret 

