object sort {
    var a = new Array[Int](5,5);
    var b = new Array[Int](5,5);
    var c = new Array[Int](5,5);
    def scana(size: Int){
            var i : Int = 0;
            var j : Int = 0;
            var t : Int = 0;
//	    a[0,0] = i;
	//    var x : Int = 0;
	 /*   var y : Int = 0;	   
	   a[0 , 0] = 20;
	   a[1 , 0] = 30;
	   y = a[0 , 0] * a[1 , 0]; 
	   t = a[0 , 0];
	   x = a[1 , 0];
	   
	   println(t);
	   println(x);
	   println(y); */
	//    println(t);
            for ( i <- 0 until size )
            {
                 for ( j <- 0 until size )
		{
                    read(t);
                    a[i , j] = t;
                }
            }
	    for ( i <- 0 until size )
		{
                 for ( j <- 0 until size )
		 {
 		    t = a[i , j];
                    println(t);
                }
            }   
     }
    def scanb(size: Int){
            var i : Int = 0;
            var j : Int = 0;
            var t : Int = 0;
            for ( i <- 0 until size )
	    {
                 for ( j <- 0 until size )
		 {
                    read(t);
                    b[i , j] = t;
                }
            }
	    for ( i <- 0 until size )
		{
                 for ( j <- 0 until size )
		 {
 		    t = b[i , j];
                    println(t);
                }
            } 
     }
     def multiply(size: Int){
            var i : Int = 0;
            var j : Int = 0;
            var k : Int = 0;
	    var t : Int = 0;
	    var x : Int = 0;
            for ( i <- 0 until size )
		    {
                for ( j <- 0 until size )
		     {
                 //   c[i,j] = 0;
                    for ( k <- 0 until size )
		    {
		//	t = a[i,k];
		/*	x = b[k,j];
			t = 0;
			t = a[i,k];
			x = x * t;
			println(x);
			println(t);
			t = 0;
			t = c[i,j];
			t = 101;
			c[0,0] =  201;  */
			c[i,j] = c[i,j] + a[i,k]*b[k,j];
                    }
		//   println(c[i,j]);
		    
                }
            }
     }
     def printc(size: Int){
            var i : Int = 0;
            var j : Int = 0;
            for ( i <- 0 until size )
		  {
                 for ( j <- 0 until size )
		{
                    println(c[i,j]);
                }
            }
     } 
     def main(){
         scana(1);
         scanb(1);
         multiply(1);
         printc(1);
     }
}




/*
#include <stdio.h>
#define N 4
 
// This function multiplies A[][] and B[][], and stores
// the result in C[][]
void multiply(int A[][N], int B[][N], int C[][N])
{
    int i, j, k;
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
        {
            C[i][j] = 0;
            for (k = 0; k < N; k++)
                C[i][j] += A[i][k]*B[k][j];
        }
    }
}
 
int main()
{
    int A[N][N] = { {1, 1, 1, 1},
                    {2, 2, 2, 2},
                    {3, 3, 3, 3},
                    {4, 4, 4, 4}};
 
    int B[N][N] = { {1, 1, 1, 1},
                    {2, 2, 2, 2},
                    {3, 3, 3, 3},
                    {4, 4, 4, 4}};
 
    int C[N][N]; // To store result
    int i, j;
    multiply(A, B, C);
 
    printf("Result matrix is \n");
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
           printf("%d ", C[i][j]);
        printf("\n");
    }
 
    return 0;
}
*/
