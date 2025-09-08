/*Program to write people to a sorted list by name, then delete them by name.
Mads Rudolph 25.11.2024
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define the structure for a record
typedef struct Record {
    char name[50];          // Name of the person
    char address[50];       // Address of the person
    unsigned int phone;     // Phone number of the person
    struct Record *nextPtr; // Pointer to the next record in the list
} Record, *recordPtr;

// Function prototypes
void loadRecords(const char *filename, recordPtr *head);
void insertRecord(recordPtr *head, const char *name, const char *address, unsigned int phone);
void writeRecords(const char *filename, recordPtr head);
void deleteRecord(recordPtr *head, const char *name);
void freeList(recordPtr head);
void addRecord(recordPtr *head);
void deleteRecordByName(recordPtr *head);

int main() {
    recordPtr head = NULL; // Initialize the head of the list to NULL

    // Load records from the file into the linked list
    loadRecords("myDatabase.txt", &head);

    int choice;
    do {
        // Display menu options to the user
        printf("Menu:\n");
        printf("1. Add a new record\n");
        printf("2. Delete a record\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar(); // Assures that the input buffer is empty

        // Perform action based on user's choice
        switch (choice) {
            case 1:
                addRecord(&head); // Add a new record
                break;
            case 2:
                deleteRecordByName(&head); // Delete a record by name
                break;
            case 3:
                writeRecords("myDatabase.txt", head); // Save records to the file
                freeList(head); // Free the memory allocated for the list
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 3); // Repeat until the user chooses to exit

    return 0;
}

// Load records from a file into the linked list
void loadRecords(const char *filename, recordPtr *head) {
    FILE *file = fopen(filename, "r");
    if (!file) return; // Return if the file cannot be opened

    char line[150];
    while (fgets(line, sizeof(line), file)) {
        char name[50], address[50];
        unsigned int phone;
        // Go through the line and extract name, address, and phone number
        sscanf(line, "%49[^,], %49[^,], %u", name, address, &phone);
        // Insert the record into the linked list
        insertRecord(head, name, address, phone);
    }
    fclose(file); // Close the file
}

// Insert a new record into the linked list in sorted order
void insertRecord(recordPtr *head, const char *name, const char *address, unsigned int phone) {
    recordPtr newRecord = malloc(sizeof(Record));
    if (!newRecord) {
        perror("Failed to allocate memory");
        return;
    }
    strcpy(newRecord->name, name);
    strcpy(newRecord->address, address);
    newRecord->phone = phone;
    newRecord->nextPtr = NULL;

    // Insert in sorted order
    if (*head == NULL || strcmp(name, (*head)->name) < 0) {
        newRecord->nextPtr = *head;
        *head = newRecord;
    } else {
        recordPtr current = *head;
        while (current->nextPtr != NULL && strcmp(name, current->nextPtr->name) > 0) {
            current = current->nextPtr;
        }
        newRecord->nextPtr = current->nextPtr;
        current->nextPtr = newRecord;
    }
}

// Write the records from the linked list to a file
void writeRecords(const char *filename, recordPtr head) {
    FILE *file = fopen(filename, "w");
    if (!file) {
        perror("Error opening file");
        return;
    }

recordPtr current = head;
    while (current != NULL) {
        // Write each record to the file
        fprintf(file, "%s, %s, %u\n", current->name, current->address, current->phone);
        current = current->nextPtr;
    }
    fclose(file); // Close the file
}

// Delete a record from the linked list by name
void deleteRecord(recordPtr *head, const char *name) {
    if (*head == NULL) return;

    recordPtr current = *head;
    recordPtr previous = NULL;

    // Find the record to delete
    while (current != NULL && strcmp(current->name, name) != 0) {
        previous = current;
        current = current->nextPtr;
    }

    if (current == NULL) {
        printf("Record not found.\n");
        return;
    }

    // Remove the record from the list
    if (previous == NULL) {
        *head = current->nextPtr;
    } else {
        previous->nextPtr = current->nextPtr;
    }

    free(current); // Free the memory allocated for the record
    printf("Record deleted successfully.\n");
}

// Free the memory allocated for the linked list
void freeList(recordPtr head) {
    while (head != NULL) {
        recordPtr temp = head;
        head = head->nextPtr;
        free(temp);
    }
}

// Add a new record by getting input from the user
void addRecord(recordPtr *head) {
    char name[50], address[50];
    unsigned int phone;

    // Get the name from the user
    printf("Enter name: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = '\0'; // Remove newline character

    // Get the address from the user
    printf("Enter address: ");
    fgets(address, sizeof(address), stdin);
    address[strcspn(address, "\n")] = '\0'; // Remove newline character

    // Get the phone number from the user
    printf("Enter phone number: ");
    scanf("%u", &phone);
    getchar(); // Consume newline character

    // Insert the new record into the linked list
    insertRecord(head, name, address, phone);
    printf("Record added successfully.\n");
}

// Delete a record by getting the name from the user
void deleteRecordByName(recordPtr *head) {
    char name[50];
    // Get the name of the record to delete from the user
    printf("Enter the name of the record to delete: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = '\0'; // Remove newline character

    // Delete the record from the linked list
    deleteRecord(head, name);
}