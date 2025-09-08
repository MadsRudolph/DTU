// Mads Rudolph 07.10.2024
#include <stdio.h>

int main(void) {

int n, sum=0, min, max;
float gennemsnit;
        //Beder brugeren indtaste hvor mange tal de vil indtaste
    do{
        printf("Hvor mange tal vil du have at jeg skal gemme? (Maks 100)\n");
        scanf("%d", &n);
        //tjekker at tallet er imellem 0 og 100, hvis ikke kører loppet forfra
        if(n > 100){
        printf("Du kan ikke indtaste mere end 100 tal, indtast venligst igen\n");
        }
        else if(n<=0){
        printf("Ingen tal indtastet, indtast venligst igen!\n");
        }
    } while(n>100 || n<=0);
        //laver det array numrerne skal opbevares i
    int numrer[n];
        //beder brugeren indtaste numrene
    printf("indtast %d tal:\n", n);
    for (int i = 0; i <n; i++) {
        //læser nummeret og opdatere summen
        scanf("%d", &numrer[i]);
        sum += numrer[i];
        //opdatere min og max
        if (i == 0) {
            min = max = numrer[i];
        } else {
                if (numrer[i] < min) min = numrer[i];
                if (numrer[i] > max) max = numrer[i];
        }
    }
        //udregner gennemsnittet
    gennemsnit = (float)sum/n;
        //printer resultaterne
    printf("summen er: %d\n", sum);
    printf("gennemsnittet er: %.2f\n", gennemsnit);
    printf("det hoejeste tal er: %d\n", max);
    printf("det laveste tal er: %d\n", min);

        //checker om der er dubletter
int dubletter = 0;
    printf("Dubletter fundet:\n"); 
        //sammenligner hvert tal i arrayet med det næste
    for (int i = 0; i < n; i++) {
        //sikrer at der kun sammenlignes en gang
        for (int j = i + 1; j < n; j++) {  
        //Hvis i == j er det en dublet, og den printes
            if (numrer[i] == numrer[j]) {
                printf("%d\n", numrer[i]);
                dubletter = 1;
                break;
            }
        }
    }
        //hvis ingen dupletter bliver fundet, printes "ingen dubletter fundet"
    if (!dubletter) {
        printf("Ingen dubletter fundet.\n");
    }

    return 0;
}
