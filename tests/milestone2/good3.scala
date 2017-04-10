class s () {
   var a: Int = 1;
   var b: Float = 1.1; 
    }

class t () {
    var a: Int = 1;
    var b: Float = 1.1;
}

object Good1 {
    def g(x:Int, y:Double){
		println(x);
        println("\n");
        println(y);
	 }
   def main(args: Array[String]){
      var x = new s();
      var y = new s();
      var q : Float = 1.1;
      x.b = 2.0;
      y = x;
      x.b = -4;
      g(x.b, y.b);
   }
}


/*
#include<stdio.h>

struct s {
    int a;
    float b;
};

struct t {
    int a;
    float b;
};

void g(int x, float y) {
    printf("%d",x);
    printf("\n");
    printf("%f",y);
}

void main() {
    struct s x;
    struct s y;
    float q;
    x.b = 2.0;
    y = x;
    x.b = -4;
    g(x.b, y.b);
}
*/