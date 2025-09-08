/*  Opgave 5: find vokaler i en string skrevet af en bruger
    Af Mads Rudolph
    21 okt. 2024
*/
#include <stdio.h>

// definere funktionen der finder antallet af bestemte char i en given tekst fra brugeren
int countCharactersInSet(const char *tekst, const char *set) {
    int count = 0; // initialisere tælle variablen til 0
    while (*tekst) { //gennemløber hvert tegn i teksten     
        const char *s = set; // pointer til at itterere igennem hele teksten
        while (*s) {
            if (*tekst == *s) { //Hvis tegnet i teksten matcher et tegn i sættet forørges count med 1
                count++;
                break;
            }
            s++;   // gå til næste tegn i sættet    
        }
        tekst++;    // gå til næste tegn i teksten
    }
    return count;   //returnere det samlede antal tegn der matchede
}

int main() {
    const int maxlength = 100; // definere maksimale længde af inputteksten
    char tekst[maxlength];  //et array til at gemme inputteksten
    printf("Skriv en tekst: ");
    fgets(tekst, sizeof tekst, stdin); //læser inputteksten fra brugeren

    int vokaler = countCharactersInSet(tekst, "aeiouyAEIOUY"); // tæller antallet af vokaler i inputteksten
    printf("Antal vokaler: %d\n", vokaler); // printer antal vokaler fundet i teksten

    return 0;
}
