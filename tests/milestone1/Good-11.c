// To check the structure of if-else statement:
#include<stdio.h>
void main() {
	int x;
	printf(“Enter a value”);
	scanf(“%d”, &x);
	if(x > 0)
 	printf(“%d”, x);
	else
 	printf(“Number is zero”);
}

object Good7 {
	def main(args: Array[String]) {
		println("Enter a value")
        val x=scala.io.StdIn.readInt();
		if( x > 0 ){
            println(x);
	    }
		else {
        	println("Number is zero");
		}
    }
}
