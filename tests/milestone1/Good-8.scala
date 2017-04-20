object Good8 {
	 def add(arr1: Int) : Int = {
		var arr = new Array[Int](4);
		var c: Int = 10 + 12;
		var i: Int = 0;
		while (i <= 4) {
              //  arr[i] = i+1;
				c = c + i;
				i = i + 1;
    	}
		return c;
	 }
	 def sub1(a : Int,b:Int) : Int ={
		return a;
	 }
	def sub2(a : Int){
		println(a);
	 }
	 def sub(a : Int) : Int = {
		return a;
	 }
	def main(args: Array[String]) {
        	var a = new Array[Int](4);
			var i : Int = 0;
			if( i == 2 )
			{
					i = i + 1;
         	}
			a[i] = 10;
			args[i] = "a";
			i = 10;
			var c : Int = 0;
			var d : Int = sub(i);
			d = sub(i+i+i*i-i%i);
			var x : Int = 0;
      		// An infinite loop.
      		while( c <= d )
			{
         		if( x == 2 )
				 {
					a[i] = x;
					break;
            		x = x + 1 * 4;
         		}
				else
				{
					continue;
					a[i] = x*10;
				}
			
     		 }
			for ( x <- 1 until 10 )
			{
				continue;
				x = x + 2;
         		//println( "Value of a: " + a );
      		}
			x  match 
			{
      			case c1 => "one"
				case c2 => "two"
				case c3 => "three"
   			}
		    /*var f : Int  = sub(i);
		    var g : Int = sub(i/c);
		    d = sub(i%c);
		    d = sub(i<<c);
			sub2(d);*/
		   // d = sub(i&&c);
		   // d = sub(i||c);
	}
}
/*
// Program to exercise the array feature implemented
#include<stdio.h>
void main()
{
int a[5]={1,2,3,4,5};
int c=0,d;
for(int i=0;i<5;i+)
        c += a[i];
printf(" sum is  %d  && random value is %d",c,d);
}
*/
