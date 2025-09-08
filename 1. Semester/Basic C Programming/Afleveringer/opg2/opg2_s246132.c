// Mads Rudolph 23.09.2024

#include <stdio.h>

int main(void){

int p1,p2,p3,p4;
float mean=0.0;

// Beder om input
printf("indtast point fra 0-100 for hver opgave 1-4\n");

// Beder om input, og tjekker om det er i det tilladte interval, hvis ikke bedes brugeren igen, og tallet gemmes i p variablen
do{
printf("point opgave 1:\n");
scanf("%d", &p1);
if(p1<0 || p1>100){
    printf("point skal være mellem 0 og 100, skriv venligst et nyt tal\n");
    }
} while (p1<0 || p1>100);

// det samme gøres for p2
do{
printf("point opgave 2:\n");
scanf("%d", &p2);
if(p2<0 || p2>100){
    printf("point skal være mellem 0 og 100, skriv venligst et nyt tal\n");
    }
} while (p2<0 || p2>100);

// og p3
do{
printf("point opgave 3:\n");
scanf("%d", &p3);
if(p3<0 || p3>100){
    printf("point skal være mellem 0 og 100, skriv venligst et nyt tal\n");
    }
} while (p3<0 || p3>100);

//og p4
do{
printf("point opgave 4:\n");
scanf("%d", &p4);
if(p4<0 || p4>100){
    printf("point skal være mellem 0 og 100, skriv venligst et nyt tal\n");
    }
} while (p4<0 || p4>100);

//Gennemsnittet udregnes            
mean=(p1+p2+p3+p4)/4.0;

//gennemsnittet konverteres til en int, og deles med 10 som symbolisere dens karakter kategori
int karakter= (int)mean/10;

switch(karakter){
    //Hvis karakter værdien er 10 eller 9 printes nedestående
    case 10:
    case 9:
        printf("\nkarakteren er: 12");
        break;
    //osv...
    case 8:
        printf("\nkarakteren er: 10");
        break;

    case 7:
        printf("\nkarakteren er: 7");
        break;

    case 6:
        printf("\nkarakteren er: 4");
        break;

    case 4:
    case 5:
        printf("\nkarakteren er: 02");
        break;
    // Hvis gennemsnitsværdien er under 40 får man 00. Så hvis karakter værdien ikke er mellem 4 og 10 skal man have 00, derfor køres default.
    default:
        printf("\nkarakteren er: 00");
        break;
}
//printer gennemsnits værdien som en float uden decimal tal
printf("\ngennemsnittet er: %1.f\n" , mean);

return 0;
}
