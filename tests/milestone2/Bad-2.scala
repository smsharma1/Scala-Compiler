object Bad2 {
    def f( a:Int ) : Int = { 
        a = a + 1;
		return a;
	 }
   def main(args: Array[String]) {
        f(4) = 4;
   }
}

/*
#include<stdio.h>
int f(int a) {
    return a+1;
}


void main() {
    f(4) = 4;
}
*/