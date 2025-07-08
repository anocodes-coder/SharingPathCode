How to run the code

Before running the file secrets_handle.py we should run torsion_handle.py that defines the secret torsion point
given to the dealer.
 1)  >run torsion_handle.py # This file is in the directory isogeny_computations.
 2)  >run secrets_handle.py --Sharing_and_Recovering -p=pX # This file is in the main directory.
In the expression "-p=pX", X representes the size of the prime and in the set 
{p128, p288, p434, p503, p610, p640, p751,}

If we want just to display the public data and the private elements given to the dealer we 
modify the commande 2) as follows
3)   >run secrets_handle.py --Dealer_Data -p=pX

Note that this library relies on function developped in Dartois's library [] which itself
heavily relies on the computations in [3].   


 [3] Pierrick Dartois, Luciano Maino, Giacomo Pope and Damien Robert, An Algorithmic Approach 
 to (2,2)-isogenies in the Theta Model and Applications to Isogeny-based Cryptography, In Advances 
 in Cryptology – ASIACRYPT 2024. https://eprint.iacr.org/2023/1747.
