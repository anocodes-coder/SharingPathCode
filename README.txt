The goal of this library is to implement functions that represent the bulk
of the cost of the secret sharing scheme introduced in the submitted document.
We aim to compare its computational cost with the running time of the seminal
isogeny-based threshold scheme proposed by De Feo and Meyer [1]. Specifically,
this comparison is intended to highlight the efficiency of our technique relative
to the first threshold scheme relying on isogenies—particularly on
the class group action combined with Shamir’s secret sharing.

The cost of the algorithm in [1] is dominated by a class group action computation
[s]E, where s is a Shamir secret and E an elliptic curve, see [4, Algorithme 3, Line 5].  
On the other side Line 23 [4, Algorithm 2] that deals with isogeny recompuation of reprsents 
the main computational cost of our scheme. So, in the comparison focuses on the 
implementation of the related functions. As explained in the manuscrit the other 
sub-processes such as the encoding are negligible. However we give a blueprint of how 
to combine these sub-processes with isogeny computation for the sharing and recovery of a secret.


Remark on our table of comparison [4, Table 2]:
The values given in this table is a result of many execusission of the main functionin the 
the file secrets_handle.py. We took the average values after many execusission ofthe scripts.

Notes on the structure of the library

this library relies on function developped in Dartois's library [1] which itself
heavily depends on the computations in [3]. We adapt their packages in the context of our
threshold scheme where key exchange between two parties (e.g., Alice and Bob) is not required
and the torsion points should be secret parameters.


How to run the code

Before running the file secrets_handle.py we should run torsion_handle.py that defines the secret torsion points
given to the dealer.
 1)  >run torsion_handle.py # This file is in the directory isogeny_computations.
 2)  >run secrets_handle.py --Sharing_and_Recovering -p=pX # This file is in the main directory.
In the expression "-p=pX", X representes the size of the prime and is in the set 
{p128, p288, p434, p503, p610, p640, p751}

If we want just to display the public data and the private elements given to the dealer we 
modify the commande 2) as follows
3)   >run secrets_handle.py --Dealer_Data -p=pX
 

[1] L. De Feo, M. Meyer.: Threshold schemes from isogeny assumptions. In: Kiayias, A.,652
Kohlweiss, M., Wallden, P., Zikas, V. (eds.) PKC 2020. LNCS, vol. 12111, pp. 187–212.653
Springer, Cham (2020). https://doi.org/10.1007/978-3-030-45388-6_7

[2] P. Dartois.: Fast computation of 2-isogenies in dimension 4 and cryptographic628
applications Cryptology ePrint Archive, Paper 2024/1180, 2024, https://eprint.i629
acr.org/2024/1180

 [3] Pierrick Dartois, Luciano Maino, Giacomo Pope and Damien Robert, An Algorithmic Approach 
 to (2,2)-isogenies in the Theta Model and Applications to Isogeny-based Cryptography, In Advances 
 in Cryptology – ASIACRYPT 2024. https://eprint.iacr.org/2023/1747.

 [4] Our submitted manuscrit 
