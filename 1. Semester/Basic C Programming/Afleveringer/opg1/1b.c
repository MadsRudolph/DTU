#include <stdio.h>

int main(void){

  int a=0;
  int b=0;

  printf("%s","a:");
  scanf("%d",&a);  // Programmet får et input fra brugeren om hvilken værdi a skal have

  printf("%s","b:");
  scanf("%d",&b); // Programmet får et input fra brugeren om hvilken værdi b skal have

  int sum=(a+b); // Definere en ny variabel "sum" der lægger a og b sammen

  if(sum>b){

    a=(sum-b);
    
  }             // Hvis sum er større end b, gemmes differencen i variable a

  printf("\nSum er: %d", sum); //Printer summen i terminalen
   
}