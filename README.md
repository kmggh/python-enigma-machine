Enigma
======

Ken Guyton
Fri 2015-01-16 00:46:34 -0500


A Python emulator of an Enigma machine.  I'm writing this after
listening to Steve Gibson's description of the Enigma machine on
*Security Now*, which was in response to the new movie, *The Imitation
Game*.

Cylindar data and the machine design are from the references below.


A Note About Git
----------------

This is the first "serious" project for which I've used Git as the
only version control system.


Operation
---------

map: EKMF

Rotor in

    A 0 -  4  E
    B 1 - 10  K
    C 2 - 12  M
    D 3 -  5  F

    Forward  A -> 0 -> 4 -> E
    Reverse  E -> 4 -> 0 -> A

Shift
-----

When the rotor is stepped up one notch, the shift = 1 and it looks
like the below.  There is an "imaginary" layer of A--Z at the input
and output of the rotor, an imaginary band that stays stationary in
space.  It shows where the input of the next rotor, and the output of
the previous rotor, would be if they weren't shifted.


         A 0 -  4  E
    A -> B 1 - 10  K -> J
    B -> C 2 - 12  M -> L
    C -> D 3 -  5  F -> E



    input +-rotor-+  output
          A->E    A    
    A     B->K W->B    A
    B     C->M    C    B
    C     D->F    D    C
    D     E    A->E    D
    E     F    D->F    E
    F     G       G    F
    G     H       H    G
    H     I       I    H
    I     J       J    I
    J     K    B->K    J
    K     L       L    K
    L     M    C->M    L
    M     N       N    M
    N     O       O    N
    O     P       P    O
    P     Q       Q    P
    Q     R       R    Q
    R     S       S    R
    S     T       T    S
    T     U       U    T
    U     V       V    U
    V     W->B    W    V
    W     X       X    W
    X     Y       Y    X
    Y     Z       Z    Y 
    Z                  Z



References
----------

[Enigma Machine in Wikipedia](http://en.wikipedia.org/wiki/Enigma_machine)<br />
[Enigma rotor details in Wikipedia](http://en.wikipedia.org/wiki/Enigma_rotor_details)<br />
