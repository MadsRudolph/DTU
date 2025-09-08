/*Program to write people to a list, then sort the list by phone number and find them by phonenumber afterwards using binary search.
Focusing on clearer annotations and comments.
Mads Rudolph 16.11.2024
*/
#include <stdio.h>   
#include <stdlib.h>  
#include <string.h>  

#define MAX_LENGTH 50   // Define a constant for the maximum length of strings
#define MAX_RECORDS 100 // Define a constant for the maximum number of records

// Structure to hold the data of each record
typedef struct {
    char firstName[MAX_LENGTH];  // Array to store the first name
    char lastName[MAX_LENGTH];   // Array to store the last name
    unsigned int phoneNumber;    // Variable to store the phone number
} Record;

// Function to add a person to the file
void addPerson(const char *filename) {
    FILE *fp = fopen(filename, "a"); // Open file for appending
    if (fp == NULL) {                // Check if the file was opened successfully
        exit(1);                     // Exit the program if the file cannot be opened
    }

    Record person;                   // Create a variable to store the person's data
    // Prompt the user to enter the person's data
    printf("Enter first name: ");    
    scanf("%49s", person.firstName); // Read the first name from the user input
    printf("Enter last name: ");     
    scanf("%49s", person.lastName);  // Read the last name from the user input
    printf("Enter phone number: ");  
    scanf("%u", &person.phoneNumber);// Read the phone number from the user input

    // Write the person's data to the file in CSV format
    fprintf(fp, "%s,%s,%u\n", person.firstName, person.lastName, person.phoneNumber);
    fclose(fp);                      // Close the file to save changes
    printf("Record added successfully!\n"); // Inform the user that the record was added successfully
}

// Function to load records from a file into an array
int loadRecords(const char *filename, Record records[]) {
    FILE *fp = fopen(filename, "r"); // Open file for reading
    if (fp == NULL) {                // Check if the file was opened successfully
        return 0;                    // Return 0 if the file cannot be opened
    }

    int count = 0;                   // Initialize a counter for the number of records
    // Read records from the file until the end of the file or the maximum number of records is reached
    while (fscanf(fp, "%49[^,],%49[^,],%u\n", records[count].firstName, records[count].lastName, &records[count].phoneNumber) == 3) {
        count++;                     // Increment the counter for each record read
        if (count >= MAX_RECORDS) break; // Stop reading if the maximum number of records is reached
    }
    fclose(fp);                      // Close the file
    return count;                    // Return the number of records loaded
}

// Bubble Sort function to sort the records by phone number
void bubbleSort(Record records[], int n) {
    for (int i = 0; i < n - 1; i++) { // Outer loop for each element
        for (int j = 0; j < n - i - 1; j++) { // Inner loop for comparison
            if (records[j].phoneNumber > records[j + 1].phoneNumber) { // Compare phone numbers
                Record temp = records[j]; // Swap records if out of order
                records[j] = records[j + 1];
                records[j + 1] = temp;
            }
        }
    }
}

// Binary Search function to find a record by phone number
int binarySearch(Record records[], int n, unsigned int phoneNumber) {
    int left = 0, right = n - 1; // Initialize left and right pointers
    while (left <= right) { // Continue while there is a search space
        int mid = left + (right - left) / 2; // Calculate mid index
        if (records[mid].phoneNumber == phoneNumber) { // Check if mid is the target
            return mid; // Return index if found
        } else if (records[mid].phoneNumber < phoneNumber) { // If target is greater, ignore left half
            left = mid + 1;
        } else { // If target is smaller, ignore right half
            right = mid - 1;
        }
    }
    return -1; // Return -1 if not found
}

// Main function
int main() {
    const char *filename = "Records.txt"; // File name to store records
    Record records[MAX_RECORDS]; // Array to hold records
    int count = loadRecords(filename, records); // Load records from file

    if (count == 0) { // Check if any records were loaded
        printf("No records to load or file not found.\n");
    } else {
        bubbleSort(records, count); // Sort records by phone number
        printf("Records sorted by phone number.\n");
    }

    int choice;
    do {
        printf("\nMenu:\n1. Add Person\n2. Search by Phone Number\n3. Exit\nEnter choice: ");
        scanf("%d", &choice); // Read users choice

        switch (choice) {
            case 1:
                addPerson(filename); // Add a new person to the file
                count = loadRecords(filename, records); //sort after adding a new record
                bubbleSort(records, count);
                break;
            case 2:
                if (count == 0) { // Check if there are records to search
                    printf("No records to search.\n");
                } else {
                    unsigned int searchPhone;
                    printf("Enter phone number to search: ");
                    scanf("%u", &searchPhone); // Read phone number to search

                    int index = binarySearch(records, count, searchPhone); // Search for the phone number
                    if (index != -1) {
                        printf("Record found: %s %s, Phone: %u\n", records[index].firstName, records[index].lastName, records[index].phoneNumber);
                    } else {
                        printf("Record not found.\n");
                    }
                }
                break;
            case 3:
                printf("Exiting...\n"); // Exit the program
                break;
            default:
                printf("Invalid choice. Please try again.\n"); // Handle invalid menu choice
                break;
        }
    } while (choice != 3); // Continue until user chooses to exit

    return 0; 
}
