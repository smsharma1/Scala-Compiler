object sort {
    var a = new Array[Int](5,5);
    var b = new Array[Int](5,5);
    var c = new Array[Int](5,5);
    def scana(size: Int){
            var i : Int = 0;
            var j : Int = 0;
            var t : Int = 0;
            for ( i <- 0 until size )
		    {
                 for ( j <- 0 until size )
		        {
                    read(t);
                    a[i , j] = t;
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
                    b[i,j] = t;
                }
            }
     }
     def multiply(size: Int){
            var i : Int = 0;
            var j : Int = 0;
            var k : Int = 0;
            for ( i <- 0 until size )
		    {
                for ( j <- 0 until size )
		        {
                    c[i,j] = 0;
                    for ( k <- 0 until size )
		            {
                        c[i,j] = c[i,j] + a[i,k]*b[k,j];
                    }
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
                    println(a[i,j]);
                }
            }
     }
     def main(){
         scana(4);
         scanb(4);
         multiply(4);
         printc(4);
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