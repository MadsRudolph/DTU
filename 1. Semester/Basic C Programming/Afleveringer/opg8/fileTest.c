#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp1;           // file pointer for output
    FILE *fp2;           // file pointer for input
    const char *filename = "myfile.txt";  // file name

    // open file for writing
    fp1 = fopen(filename, "w");
    if (fp1 == NULL) {                        // check for error
        // write error message to standard error output
        fprintf(stderr, "cannot write file %s\n", filename);
        exit(1);                          // exit program with error code 1
    }
    // write comma-separated file
    fprintf(fp1, "%s,%s,%u\n", "Lucky",    "Luke",  11111111);
    fprintf(fp1, "%s,%s,%u\n", "Lady",     "Gaga",  66666666);
    fprintf(fp1, "%s,%s,%u\n", "Vladimir", "Putin", 99999999);
    // remember to close file
    fclose(fp1);

    // open file for reading
    fp2 = fopen(filename, "r");
    if (fp2 == NULL) {                        // check for error
        // write to standard error output
        fprintf(stderr, "cannot read file %s\n", filename);
        exit(1);                          // exit program 
    }
    // string buffers for name
    const int maxLength = 50;
    char firstName[maxLength], lastName[maxLength], space[maxLength];
    unsigned int phoneNumber;
    // read comma-separated file
    // repeat until end of file
    while (!feof(fp2)) {
        // fscanf works best if you read one string at a time
        fscanf(fp2, "%49[^,]", firstName); // read first name
        fscanf(fp2, "%*[ ,]");             // read and ignore comma
        fscanf(fp2, "%49[^,]", lastName);  // read last name
        fscanf(fp2, "%*[ ,]");             // read and ignore comma
        fscanf(fp2, "%u", &phoneNumber);   // read phone number
        fscanf(fp2, "%*[ ,\r\n]");         // read and ignore newline

        // output information
        printf("%-10s %-10s %u\n", firstName, lastName, phoneNumber);
    }
    // remember to close file
    fclose(fp2);

    // end program
    return 0;
}
