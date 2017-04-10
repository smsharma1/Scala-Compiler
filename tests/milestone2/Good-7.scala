object Good7 {
    def f(b : Int) : Int = {
        var a : Int =0;
        a = 5 ;
		return a;
	 }
	def main(args: Array[String]) {
	var a : Int = 0;
    var b : Int = 0;
    a = 9;
    b = f(a);
	println(a);
    println(b);
   }
}

/*
#include<stdio.h>
int f (int b ) {
    int a;
    a=5;
    return a;
}

int main () {
    int a,b;
    a = 9;
    b = f(a);
    printf("%d\n%d",a,b);
}
*/