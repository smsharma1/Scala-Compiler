class s () {
   var x: Int = 1;
   var b = new Array[Int](10,10);
    }

class t () {
    var x = new Array[Float](5,5);
}

object good4 {
    def f(a: Array[Int], b:Array[Float]){
		a[1] = 10;
	 }
   def main(args: Array[String]){
      var a = new Array[Float](10,10);
      var b = new Array[Int](10,10);
      var c = new Array[Int](5);
      var y = new t();
      var i : Int = 1;
      y.x[3,3] = 4.8;
    //   f(c, y.x[3].b);
    //   println(y.x[3].b[1][2]);
   }
}


/*#include<stdio.h>
struct s {
    int a;
    float b[5][5];
};

struct t{
    struct s x[10];
};

void f(int * a[10], float b[8][5]) {
    b[1][2] = 10.4;
}

void main() {
    float a[10][10];
    int b[10][10];
    int * c[5];
    struct t y;
    int i;
    float * fp;
    y.x[3].b[1][2] = 4.8;
    f(c,y.x[3].b);
    printf("%f",y.x[3].b[1][2]);
}
*/