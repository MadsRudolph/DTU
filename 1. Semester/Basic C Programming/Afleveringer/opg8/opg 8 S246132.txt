/*Program to write people to a list, and find them by phonenumber afterwards
Mads Rudolph 11.11.2024
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 50 // Define a constant for maximum length of names

// Function to add a person to the file
void addPerson(const char *filename) {
    FILE *fp = fopen(filename, "a"); // Open file for appending
    if (fp == NULL) { // Check if the file opened successfully
        fprintf(stderr, "Cannot open file %s\n", filename); // Print error message if file cannot be opened
        exit(1); // Exit the program with an error code
    }

    char firstName[MAX_LENGTH], lastName[MAX_LENGTH]; // Declare arrays for first and last names
    unsigned int phoneNumber; // Declare variable for phone number

    // Get user input for first name
    printf("Enter first name: ");
    scanf("%49s", firstName); // Read first name, limiting input to MAX_LENGTH
    // Get user input for last name
    printf("Enter last name: ");
    scanf("%49s", lastName); // Read last name, limiting input to MAX_LENGTH
    // Get user input for phone number
    printf("Enter phone number: ");
    scanf("%u", &phoneNumber); // Read phone number

    // Write the person's details to the file
    fprintf(fp, "%s,%s,%u\n", firstName, lastName, phoneNumber); // Format: firstName,lastName,phoneNumber
    fclose(fp); // Close the file
}

// Function to find a person by phone number
void findPerson(const char *filename) {
    FILE *fp = fopen(filename, "r"); // Open file for reading
    if (fp == NULL) { // Check if the file opened successfully
        fprintf(stderr, "Cannot open file %s\n", filename); // Print error message if file cannot be opened
        exit(1); // Exit the program with an error code
    }

    unsigned int searchNumber; // Declare variable for the phone number to search
    printf("Enter phone number to search: ");
    scanf("%u", &searchNumber); // Read the phone number to search for

    char firstName[MAX_LENGTH], lastName[MAX_LENGTH]; // Declare arrays for first and last names
    unsigned int phoneNumber; // Declare variable for phone number
    int found = 0; // Flag to indicate if the person was found

    // Read and search for the phone number in the file
    while (fscanf(fp, "%49[^,],%49[^,],%u\n", firstName, lastName, &phoneNumber) != EOF) { // Goes through the file from "," to "," searching for phonenumber, until it reaches EOF
        if (phoneNumber == searchNumber) { // Check if the current phone number matches the search number
            printf("Found: %s %s, Phone Number: %u\n", firstName, lastName, phoneNumber); // Print found details
            found = 1; // Sets found to 1
            break; // Exit the loop
        }
    }

    if (!found) { // If the person was not found
        printf("No person found with phone number %u.\n", searchNumber); // Print not found message
    }

    fclose(fp); // Close the file
}


int main() {
    const char *filename = "PersonData.txt"; // Define the filename to store data
    int choice; // Variable to store user choice

    do {
        // Prints the different options to use the program
        printf("1. Add Person\n");
        printf("2. Find Person\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice); // Read user choice

        switch (choice) { 
            case 1:
                addPerson(filename); // Call function to add a person
                break;
            case 2:
                findPerson(filename); // Call function to find a person
                break;
            case 3:
                printf("Exiting...\n"); // Print exit message
                break;
            default:
                printf("Invalid choice. Please try again.\n"); // Handle invalid choice
        }
    } while (choice != 3); // Repeat until the user chooses to exit

    return 0;
}
