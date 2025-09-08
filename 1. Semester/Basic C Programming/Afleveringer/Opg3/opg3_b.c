
#include <stdio.h>
// erklærer funktionen der udregner kvadratroden vha Newton-Rhapson metoden
double sqrt_newton_raphson(double N) {
    double x_gammel = 1.0; 
    double x_ny;
    int iterationer = 10; //antal itterationer 
    //løkke som kører funktionen igennem 10 gange
    for (int i = 0; i < iterationer; i++) {
        x_ny = 0.5 * (x_gammel + N / x_gammel); //det nye gæt 
        x_gammel = x_ny;// sætter det gamle gæt til det nye gæt
    }

    return x_ny; //returnerer det endelige gæt
}

int main() {
    double N;
    // løkke der sikrer at man indtaster et positivt tal
    do{
    printf("Indtast et tal: ");
    scanf("%lf", &N);

    if(N<0){ // tjekker om input tallet er negativt
        printf("Fejl: indtast venligst et positivt tal.\n");
    }
    }while (N<0); // kører løkken igen hvis input er negativt

    double result = sqrt_newton_raphson(N); //udregner kvadratroden af inputtet vha den deklarerede formel 
    printf("N = %f\nkvadratroden af N = %f\nDette tal i anden er = %f\n", N, result, result * result); // printer resultaterne

    return 0;
}
