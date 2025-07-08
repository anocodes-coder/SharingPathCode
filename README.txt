The goal of this library is to implement functions that account for the majority
of the computational cost in the secret sharing scheme introduced in the submitted document.
We aim to compare this cost with the running time of the seminal isogeny-based threshold scheme
proposed by De Feo and Meyer [1]. Specifically, this comparison is intended to highlight
the efficiency of our approach relative to the first isogeny-based threshold scheme—
in particular, the one based on class group action combined with Shamir’s secret sharing.

The cost of the algorithm in [1] is dominated by a class group action computation
of the form [s]E[s]E, where ss is a Shamir secret and EE is an elliptic curve (see [4, Algorithm 3, Line 5]).
On the other hand, Line 23 of [4, Algorithm 2], which involves isogeny recomputation,
represents the main computational cost of our scheme. Therefore, the comparison focuses
on the implementation of these core functions. As explained in the manuscript,
other sub-processes—such as encoding—are negligible. Nevertheless, we provide a blueprint
for combining these sub-processes with isogeny computation during the sharing and recovery of a secret.


Remark on our comparison table [4, Table 2]:
The values presented in this table are the result of multiple executions of the main function
in the file secrets_handle.py. We took the average values after running the script several times.

Notes on the structure of the library:
This library relies on functions developed in Dartois's library [1], which itself
heavily depends on the computations presented in [3]. We adapt their packages to the context of our
threshold scheme, where key exchange between two parties (e.g., Alice and Bob) is not required,
and the torsion points are treated as secret parameters.


How to Run the Code?
Before running secrets_handle.py, you must first run torsion_handle.py, which defines the secret torsion points
provided to the dealer.

    > run torsion_handle.py
        This file is located in the isogeny_computations directory.

    > run secrets_handle.py --Sharing_and_Recovering -p=pX
        This file is located in the main directory.

In the argument -p=pX, the value X represents the bit-size of the prime and must be one of the following:
{p128, p288, p434, p503, p610, p640, p751}. If you only want to display the public data and the private 
elements given to the dealer, modify command (2) as follows:

    > run secrets_handle.py --Dealer_Data -p=pX
 

[1] L. De Feo, M. Meyer.: Threshold schemes from isogeny assumptions. In: Kiayias, A.,652
Kohlweiss, M., Wallden, P., Zikas, V. (eds.) PKC 2020. LNCS, vol. 12111, pp. 187–212.653
Springer, Cham (2020). https://doi.org/10.1007/978-3-030-45388-6_7

[2] P. Dartois.: Fast computation of 2-isogenies in dimension 4 and cryptographic628
applications Cryptology ePrint Archive, Paper 2024/1180, 2024, https://eprint.iacr.org/2024/1180

 [3] Pierrick Dartois, Luciano Maino, Giacomo Pope and Damien Robert, An Algorithmic Approach 
 to (2,2)-isogenies in the Theta Model and Applications to Isogeny-based Cryptography, In Advances 
 in Cryptology – ASIACRYPT 2024. https://eprint.iacr.org/2023/1747.

 [4] Our submitted manuscrit 
