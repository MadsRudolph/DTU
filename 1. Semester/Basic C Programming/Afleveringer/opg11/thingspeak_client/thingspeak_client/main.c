#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>


// Callback function to handle data received from the server
size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    FILE *fp = (FILE *)userp;  // Cast user pointer to file pointer
    size_t totalSize = size * nmemb;
    fwrite(contents, size, nmemb, fp);  // Write data to file
    return totalSize;
}
int main() {
    CURL *curl;
    CURLcode res;
    FILE *fp;

    // Open a file to write the response data
    fp = fopen("response_thing.json", "wb");
    if (!fp) {
        fprintf(stderr, "Could not open file for writing\n");
        return 1;
    }

    printf("Initializing libcurl...\n"); // Debugging statement

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (!curl) {
        fprintf(stderr, "Curl initialization failed.\n");
        return 1;
    }

    // Set the URL  channels/32/feeds.json?start=2019-03-01%2010:10:10&end=2019-04-30%2011:11:11  https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&exclude=hourly,daily&appid={API key}
   curl_easy_setopt(curl, CURLOPT_URL, "https://api.thingspeak.com/channels/274058/feeds.json?feeds.json?start=2023-02-20T15:24:11Z&end=2023-02-21T15:24:11Z");
    //curl_easy_setopt(curl, CURLOPT_URL,"https://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:trafiktaelling&outputFormat=CSV&SRSNAME=EPSG:4326");
    //  curl_easy_setopt(curl, CURLOPT_URL,"https://admin.opendata.dk/api/3/action/datastore_search?resource_id=6b50a51d-2cda-4581-88bd-277f4b71248e&limit=5");
   //curl_easy_setopt(curl, CURLOPT_URL,"http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid=b2d6bbcf713b2daa1ea5284670df331b");
 //curl_easy_setopt(curl, CURLOPT_URL,"api.openweathermap.org/data/2.5/forecast?lat=55.6761&lon=12.5683&appid=b2d6bbcf713b2daa1ea5284670df331b");
    // Set up callback function
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);  // Pass file pointer to callback
    // Enable verbose output
    curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

    printf("Performing HTTP request...\n"); // Debugging statement

    // Perform the request
    res = curl_easy_perform(curl);

    // Check for errors
    if (res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    } else {
        printf("Request completed successfully.\n");
    }

    curl_easy_cleanup(curl);
    curl_global_cleanup();
    return 0;
}
