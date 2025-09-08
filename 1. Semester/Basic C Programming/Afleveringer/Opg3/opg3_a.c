    #include <stdio.h>

    int main (void){
    int n=1;
    int bits=1; //sættes til 1 da 0 også er en bit.

    while(n>0){// når n bliver 0 ved vi at der er sket overflow så derfor stoppes loopen
    n=n*2;
    bits++;// Lægger 1 til i bits for hver gang n kan ganges med 2 uden at blive 0
    }
    printf("antal bits i en int:%d", bits);
    }
