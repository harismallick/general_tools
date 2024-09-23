#include <stdio.h>
#include <stdlib.h>

typedef __uint8_t BYTE;

int main()
{
    char s1[8];
    char *s2 = malloc( sizeof(BYTE) * 8);
    int counter = 0;

    while (counter < 5)
    {
        sprintf(s1, "%03d.jpg", counter);
        printf("%s\n", s1);
        counter++;
    }
    counter = 0;
    while (counter < 5)
    {        
        sprintf(s2, "%03d.jpg", counter);
        printf("%s\n", s2);
        counter++;
    }
    free(s2);
    return 0;
}