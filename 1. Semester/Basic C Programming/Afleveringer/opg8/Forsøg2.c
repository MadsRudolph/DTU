#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_PEOPLE 100

typedef struct {
    char firstname[50];
    char lastname[50];
    char phone[15];
} Person;

// Function to read the database from a file
int readDatabase(const char *filename, Person people[]) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Unable to open file");
        return -1;
    }

    int count = 0;
    while (fscanf(file, "%49[^,],%49[^,],%14s\n",people[count].firstname,people[count].lastname,people[count].phone) == 3) {
        count++;
        if (count >= MAX_PEOPLE) break; // Prevent overflow
    }

    fclose(file);
    return count; // Return the number of people read
}

// Function to add a new person to the database
void addPerson(const char *filename, Person newPerson) {
    FILE *file = fopen(filename, "a");
    if (!file) {
        perror("Unable to open file");
        return;
    }

    fprintf(file,"%s,%s,%s\n",newPerson.firstname,newPerson.lastname,newPerson.phone);
    fclose(file);
}

// Function to search for a person by phone number
Person* searchByPhone(Person people[],int count,const char *phone) {
    for (int i = 0; i < count; i++) {
        if (strcmp(people[i].phone,phone) == 0) {
            return &people[i]; // Return pointer to the found person
        }
    }
    return NULL; // Not found
}

// Main function
int main() {
    Person people[MAX_PEOPLE];
    int count = readDatabase("database2.txt", people);
    Person newPerson; // Declare newPerson here

    // Example of adding a new person
    printf("Indtast en ny person til databasen, med (navn,efternavn,tlfnr) separeret med komma: \n");
    scanf("%49[^,],%49[^,],%14s",newPerson.firstname,newPerson.lastname,newPerson.phone); // Corrected input format
    addPerson("database.txt", newPerson);

    
    // Example of searching for a person
    printf("Indtast et tlf nummer du vil lede efter i databasen:\n");
    char searchPhone[15];
    scanf("%14s",searchPhone); // Allow user to input the phone number
    Person *found = searchByPhone(people,count,searchPhone);
    if (found) {
        printf("Found: %s, %s, %s\n", found->firstname, found->lastname, found->phone);
    } else {
        printf("Person not found.\n");
    }

    return 0;
}