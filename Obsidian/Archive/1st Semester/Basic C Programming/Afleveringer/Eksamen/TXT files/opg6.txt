/*program to generate 20 sentences with random words from each subcategory
Mads Rudolph 28.10.2024
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <ctype.h>

#define NUM_SENTENCES 20
#define MAX_SENTENCE_LENGTH 100
//define the words used in each subcategory as a constant char
const char *artikler[] = {"den", "en", "nogle", "enhver", "det", "flere"};
const char *navneord[] = {"person", "studerende", "arbejdsloese", "by", "cykel", "s-tog"};
const char *verbs[] = {"koerte", "hoppede", "loeb", "gik", "sad", "bevaegede"};
const char *prepositions[] = {"til", "fra", "over", "under", "paa", "ved siden af"};

void generate_sentence(char *sentence) {
    int artikle_index1 = rand() % 6;
    int navneord_index1 = rand() % 6;
    int udsagnsord_index = rand() % 6;
    int preposition_index = rand() % 6;
    int artikle_index2 = rand() % 6;
    int navneord_index2 = rand() % 6;
    //chooses a random number bettween 0-6 indicating a word in the subcategories
    // Construct the sentence
    snprintf(sentence, MAX_SENTENCE_LENGTH, "%s %s %s %s %s %s.",
             artikler[artikle_index1], navneord[navneord_index1], verbs[udsagnsord_index],
             prepositions[preposition_index], artikler[artikle_index2], navneord[navneord_index2]);

    // Capitalize the first letter
    sentence[0] = toupper(sentence[0]);
}

int main() {
    // Initialize random number generator
    srand((unsigned int)time(NULL));

    char sentence[MAX_SENTENCE_LENGTH];

    for (int i = 0; i < NUM_SENTENCES; i++) {
        generate_sentence(sentence);
        printf("%s\n", sentence);
    }

    return 0;
}
