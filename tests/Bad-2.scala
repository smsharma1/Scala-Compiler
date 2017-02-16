/*
//Bad test case - Keyword is used as a identifier.
#include<stdio.h>
void main(){
        char *name[3];
        char if;
        printf("if is a keyword, it can't be an identifier");
}
*/

object Bad1 {
	def main(args: Array[String]) {
		var name : String = "Hello";
		var if : Char = "H";
		println("if is a keyword, it can't be an identifier"); 
   }
}
