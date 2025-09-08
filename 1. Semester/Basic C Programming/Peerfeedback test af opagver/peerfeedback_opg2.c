#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start;
    do
    {
        start = get_int("Start: ");
    }
    while (start < 9);
    // TODO: Prompt for end size
    int goal;
    do
    {
        goal = get_int("Goal: ");
    }
    while (goal < start);

    // TODO: Calculate number of years until we reach threshold
    int years = 0;
    while (start < goal)
    {
        start = start + (start / 3) - (start / 4);
        years++;
    }
    // TODO: Print number of years
    printf("Years: %i\n", years);
}