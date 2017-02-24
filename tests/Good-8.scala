object Good8 {
	 def add(arr: Array[Int]) {
		var c = 0;
		var i = 0;
		while (i <= 4) {
                arr(i) = i+1;
				c = c + arr(i);
				i = i + 1;
    	}
	 }

	def main(args: Array[String]) {
        	var a = new Array[Int](4);
			a(0) = 1
			a(1) = 2
			a(2) = 3
			a(3) = 4
			var i = 0;
			var c = 0;
			add(a);
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

