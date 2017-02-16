//Good test case for Expression parsing
/*#include<stdio.h>
void main(){
    int a = 1;
    int b = 2;
    int *p = &a;

    int c = a+++b;
int x = 23, y, z  = 23;
    x = y = z = x == z;
y = *p*b++**p;
}*/
/*There is no way to access addresses in Scala. It's governed by the Memory Management of the JVM controlling or knowing the addresses makes absolutely no sense in Scala. reference https://rosettacode.org/wiki/Address_of_a_variable#Scala*/
object Demo {
	def main(args: Array[String]) {
		var a : Int  = 10;	
		var b : Int  = 20;
		var d : Int  = 0;
		var c : Int = a + b;
		var x : Int = 23;
		var y : Int = 23;
		var z : Int = 23;
		x = x == z;
		y = x == z;
		z = x == z;
		y = d*b*d;
	}
} 
