// This test is to test the user-defined data type.
// typedef int myint; /* here myint should be identifier*/
// myint a; /* Here myint should be Data Type*/ // By- Nishit
#include <stdio.h>
#include <limits.h>
int main(){
   typedef long long int LLI;
   LLI long_variable;
   printf("Size for long long int data type  : %ld \n", sizeof(long_variable));
   return 0;
}
