#include <stdio.h>

int main(void){

    int icheck=0;
    float fkontrol=0;
    int a=0;            //Definere nogle variabler der skal bruges i programmet
    char valg;

    do{                 //starter et "do" loop da vi gerne vil have at programmet skal kunne starte forfra hvis brugeren ønsker det

    while(1){           //laver et while loop som bliver ved med at køre indtil brugeren indtaster et helt tal
    printf("indtast et tal: ");
    scanf("%f", &fkontrol);     //Tallet bliver sat ind på fkontrol variablen som er en Float, derfor kan den også modtage ikke hele tal

    icheck=fkontrol;    //konvertere til en int

    if((fkontrol-icheck)==0){ //Checker om tallet er et hel tal

        a=fkontrol; //hel tallet gemmes i "a"
        break; //slutter loopen
    }
    else{
        printf("indtast venligst et hel tal og ikke et decimal tal\n"); //Brugeren bliver spurgt om at indtaste et hel tal, hvis ikke tallet er helt
    }
    }
    if(a % 5 == 0){ //Tjekker om tallet er deleligt med 5
        printf("%d er et helt tal, og er deleligt med 5\n", a);  //Hvis det er sandt printes dette   

    }
    else{
        printf("%d er et helt tal, men er ikke deleligt med 5\n", a); //Hvis det er falsk printes dette
    }
    

    int num1;   //Definere variabler for indtastning af 2 tal, og en regneoperation
    int num2;
    int operation;
    printf("indtast 2 tal: ");  //Beder brugeren indtaste 2 tal
    scanf("%d %d", &num1, &num2);   //Indsætter tallene på num1 og num2

    printf("vælg en operation:\n"); //Brugeren bedes vælge en af 4 regneoperationer, som 1,2,3 eller 4
    printf("1: addition\n");
    printf("2: subtraction\n");
    printf("3: Multiplikation\n");
    printf("4: Division\n");
    
    scanf("%d", &operation);    //Indsætter det valgte nummer på operation variablen


    switch(operation){      //Laver en Switch istedet for en masse "if else loops"

        case 1:
            printf("Resultat: %d\n", num1+num2);    //Hvis brugeren vælger 1 udføres addition operationen og resultatet printes
            break;

        case 2:
            printf("Resultat: %d\n", num1-num2);    //Hvis brugeren vælger 2 udføres subtraction operationen og resultatet printes
            break;

        case 3:
            printf("Resultat: %d\n", num1*num2);    //Hvis brugeren vælger 3 udføres multiplikations operationen og resultatet printes
            break;
        
        case 4:
            while(num2 == 0) {                      //Hvis nævneren "num2" er 0 vil vi gerne have brugeren skal indtaste et nyt tal som ikke 0. Så dette loop tjekker om num2 er = 0
                printf("Nævneren er 0 :-( Indtast venligst et andet tal end 0:");   //printer at nævneren er 0 og beder om at indtaste et nut tal som ikke er 0 
                scanf("%d", &num2);                                                 //gemmer det nye tal i num2
            }
            printf("Resultat: %.1f\n", (float)num1/num2);                           //udfører division operationen og printer resultatet med et decimal %.1f
            break;

    }


    printf("Vil du køre programmet igen? (j/n: )");     //spørger brugeren om man vil køre programmet igen hvor "j" betyder ja
    scanf(" %c", &valg);                                //Gemmer char inputtet under valg variablen
    } while(valg == 'j');                               //Hvis brugeren vælger "j" starter "do loopet" forfra


return 0;
}  