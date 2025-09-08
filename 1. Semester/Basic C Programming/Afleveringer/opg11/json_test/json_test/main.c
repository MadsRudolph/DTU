#include <stdio.h>
#include "cJSON.h"
#include <stdlib.h>
#include <string.h>
#define MAX_VALUES 200
#define MAX_ENTRIES 200
#define MAX_FEEDS 200

int values[MAX_VALUES];
int count = 0;



typedef struct
{
    char created_at[50];
    int entry_id;
    double field1;
    double field2;
} Feed;

typedef struct 
{
    int id;
    char name[50];
    char description[100];
    Feed feeds[MAX_FEEDS];
    int feed_count;
} ChannelData;

void parseThingspeakData(const char *jsonBuffer, ChannelData *data);
void traverseJSON(cJSON *item, int depth);


int writeJson()
{
    // create a cJSON object
    cJSON *json = cJSON_CreateObject();
    cJSON_AddStringToObject(json, "name", "John Doe");
    cJSON_AddNumberToObject(json, "age", 30);
    cJSON_AddStringToObject(json, "email", "john.doe@example.com");

    // convert the cJSON object to a JSON string
    char *json_str = cJSON_Print(json);

    // write the JSON string to a file
    FILE *fp = fopen("data.json", "w");
    if (fp == NULL)
    {
        printf("Error: Unable to open the file.\n");
        return 1;
    }
    printf("%s\n", json_str);
    fputs(json_str, fp);
    fclose(fp);
    // free the JSON string and cJSON object
    cJSON_free(json_str);
    cJSON_Delete(json);
    return 0;
}

int readJson()
{

    {
        FILE *fp1; // file pointer for output
        // open the file
        FILE *fp = fopen("response.json", "r");
        if (fp == NULL)
        {
            printf("Error: Unable to open the file.\n");
            return 1;
        }

        // read the file contents into a string
        char buffer[900024]; // huge buffer for reading all data from thingspeak request
        int len = fread(buffer, 1, sizeof(buffer), fp);
        printf("length", len);
        fclose(fp);

            ChannelData data = {0};
            parseThingspeakData(buffer, &data);

            // Print "channel" info
            printf("Channel ID: %d\n", data.id);
            printf("Channel Name: %s\n", data.name);
            printf("Channel Description: %s\n", data.description);

            // Print "feeds" info
            printf("\nFeeds (%d):\n", data.feed_count);
            for (int i = 0; i < data.feed_count; i++) {
                printf("  Feed %d:\n", i + 1);
                printf("    Created At: %s\n", data.feeds[i].created_at);
                printf("    Entry ID: %d\n", data.feeds[i].entry_id);
                printf("    Field1: %.2f\n", data.feeds[i].field1);
                printf("    Field2: %.2f\n", data.feeds[i].field2);
            }
            //write data into a comma separatet file
            const char *filename = "data.csv"; // file name
             fp1 = fopen(filename, "w");
                    if (fp1 == NULL)
                    { // check for error
                        fprintf(stderr, "cannot write file %s\n", filename);
                        exit(1);
                    }
                    else
                    {
                        for (int m = 1; m <=MAX_FEEDS; m++)
                        {

                            fprintf(fp1, "%s, %f\n", data.feeds[m].created_at, data.feeds[m].field2);
                        }
                        // do binary search finding a record retunrs the number where it is stored
                        //
                        fclose(fp1);
                    }
        

        //  Raw data parser for openwearthermap data
        cJSON *json = cJSON_Parse(buffer);
        if (json == NULL)
        {
            printf("Error parsing JSON!\n");
            return 1;
        }

        traverseJSON(json, 0);

        // Free the parsed JSON object
        cJSON_Delete(json);
    }
}
// function for converting thingspeak time to at standard time format.
void convert_time_format(const char *input, char *output)
{
    // Copy the input to the output to make changes
    strcpy(output, input);

    // Replace 'T' with a space
    char *t_pos = strchr(output, 'T');
    if (t_pos)
    {
        *t_pos = ' ';
    }

    // Remove the trailing 'Z' if it exists
    size_t len = strlen(output);
    if (output[len - 1] == 'Z')
    {
        output[len - 1] = '\0';
    }
}

void traverseJSON(cJSON *item, int depth)
{
    while (item != NULL)
    {
        // Print indentation for readability
        for (int i = 0; i < depth; i++)
        {
            printf("  ");
        }

        // Check the type of the current item
        if (cJSON_IsObject(item))
        {
            printf("Key: %s (Object)\n", item->string);
            traverseJSON(item->child, depth + 1); // Recurse into the object
        }
        else if (cJSON_IsArray(item))
        {
            printf("Key: %s (Array)\n", item->string);
            cJSON *arrayElement = NULL;
            cJSON_ArrayForEach(arrayElement, item)
            {
                traverseJSON(arrayElement, depth + 1); // Recurse into the array
            }
        }
        else if (cJSON_IsString(item))
        {
            printf("Key: %s, Value: %s\n", item->string, item->valuestring);
        }
        else if (cJSON_IsNumber(item))
        {
            printf("Key: %s, Value: %f\n", item->string, item->valuedouble);
        }
        else if (cJSON_IsBool(item))
        {
            printf("Key: %s, Value: %s\n", item->string, cJSON_IsTrue(item) ? "true" : "false");
        }
        else if (cJSON_IsNull(item))
        {
            printf("Key: %s, Value: null\n", item->string);
        }

        item = item->next; // Move to the next item in the current level
    }
}

void parseThingspeakData(const char *jsonBuffer, ChannelData *data)
{
    cJSON *json = cJSON_Parse(jsonBuffer);
    char time[30];
    if (!json)
    {
        printf("Error parsing JSON!\n");
        return;
    }

    // Parse "channel"
    cJSON *channel = cJSON_GetObjectItemCaseSensitive(json, "channel");
    if (channel)
    {
        cJSON *id = cJSON_GetObjectItemCaseSensitive(channel, "id");
        cJSON *name = cJSON_GetObjectItemCaseSensitive(channel, "name");
        cJSON *description = cJSON_GetObjectItemCaseSensitive(channel, "description");

        if (cJSON_IsNumber(id))
            data->id = id->valueint;
        if (cJSON_IsString(name))
            strncpy(data->name, name->valuestring, sizeof(data->name) - 1);
        if (cJSON_IsString(description))
            strncpy(data->description, description->valuestring, sizeof(data->description) - 1);
    }

    // Parse "feeds"
    cJSON *feeds = cJSON_GetObjectItemCaseSensitive(json, "feeds");
    if (cJSON_IsArray(feeds))
    {
        data->feed_count = 0;

        cJSON *feedItem = NULL;
        cJSON_ArrayForEach(feedItem, feeds)
        {
            if (data->feed_count >= MAX_FEEDS)
            {
                printf("Warning: Maximum number of feeds exceeded.\n");
                break;
            }

            Feed *feed = &data->feeds[data->feed_count];

            cJSON *created_at = cJSON_GetObjectItemCaseSensitive(feedItem, "created_at");
            cJSON *entry_id = cJSON_GetObjectItemCaseSensitive(feedItem, "entry_id");
            cJSON *field1 = cJSON_GetObjectItemCaseSensitive(feedItem, "field1");
            cJSON *field2 = cJSON_GetObjectItemCaseSensitive(feedItem, "field2");

            if (cJSON_IsString(created_at))
                strncpy(feed->created_at, created_at->valuestring, sizeof(feed->created_at) - 1);

            convert_time_format(feed->created_at, time);
            strcpy(feed->created_at, time);
            if (cJSON_IsNumber(entry_id))
                feed->entry_id = entry_id->valueint;
            if (cJSON_IsString(field1))
                feed->field1 = atof(field1->valuestring); // Convert string to double
            if (cJSON_IsString(field2))
                feed->field2 = atof(field2->valuestring);

            data->feed_count++;
        }
    }

    cJSON_Delete(json); // Clean up memory
}

int main()
{
    writeJson();
    readJson();
}