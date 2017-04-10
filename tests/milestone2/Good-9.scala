object Good9 {
    def returnInt() : Int = { 
		return 1;
	 }
   def main(args: Array[String]) {
        var a:Int =1;
        var b:Int =1;
        var c = new Array[Int](3);
        a = 2;
        b = 4;
        c[returnInt()] = 4;
        println(c[1]);
   }
/*
#include<stdio.h>
int returnInt () {
    return 1;
}

int main() {
    int a;
    int b;
    int c[3];

    a = 2;
    b = 4;

    *(&a) = b;

    c[returnInt()] = 4;
   printf("%d",c[1]);

}
*/