class s () {
   var a: Int = 1;
    }

object good5 {
   def f(a:Int) : Int = { 
		return a;
	 }
   def main(args: Array[String]) {
        var a = new s();
        var p = new s();
        a.a = 3;
        p = a;
        var ip : Int = a.a;
        println(ip);
   }
}


/*
#include<stdio.h>
struct s {
    int a;
};

int * f(void * a) {
    return a;
}

void main() {
    struct s a, *p;
    int * ip;
    a.a = 3;
    p = &a;
    ip = f(p);
    printf("%d",*ip);
}
*/