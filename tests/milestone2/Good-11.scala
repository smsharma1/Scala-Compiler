object Good11 {
	def main(args: Array[String]) {
	var x : Int = 0;
    var y : Int = 0;
    var a : Double = 0.0;
    var b : Double = 0.0;
    var i : Int = 0;
    var j : Int = 0;
    x = 10;
    y = -1;
    for ( i <- 0 until 10 )
	{
		y = -1 * y;
        x = x + i * y;
        i = -1 * -1*i;
    }
    a = 10.0;
    b = -0.1;
    for ( i <- 1 until 10 )
	{
          b = -1 * b;
          a  = a + i*b;
          i= -1 * -1 * i;
    }
    println(x);
    println(a);
   }
}


/*
#include<stdio.h>
void main()
{
    int x;
    int y;
    float a;
    float b;
    int i;
    int j;
    x = 10;
    y = -1;
    for(i=0; i<10; i++){
        y = -y;
        x = x + i*y;
        i = - (-i);
    }

    a = 10.0;
    b = -0.1;
    for(i=0; i<10;i++){
        b=-b;
        a  = a+i*b;
        i= - (-i);
    }

    printf("Expected output:5 9.500000\n");

    printf("%d", x);

    printf("%f", a);
    printf("\n");
}
*/