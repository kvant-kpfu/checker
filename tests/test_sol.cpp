#include "stdio.h"
#include "string.h"

const char* str = "Hello, World!";

int main() {
    FILE* f = fopen("/output.txt", "w");
    fwrite(str, strlen(str), 1, f);
    fclose(f);
    return 0;
}