object bubbleSort{
    var f = new Array[Int](10);
    def bSort(n : Int )
    {
        var i : Int = 0;
        var j : Int = 0;
        var temp : Int = 0;
        n  = n - 1;
        for ( i <- 0 until n )
		{
            var t : Int = n - i - 1;
            for ( j <- 0 until t)
		    {
			   if( f[j] > f[j + 1] )
               {
                    temp = f[j];
                    f[j] = f[j + 1];
                    f[j + 1] = temp;
               }
      	    }
      	}
        for ( i <- 0 until n)
	{
		println(f[i]);
      	}

    }
    def scanf(n:Int)
    {
	var i : Int = 0;
        for ( i <- 0 until n )
	{
	    var x : Int  = 0; 
            read(x);
	    f[i] = x;
        }
    }
    def main(args: Array[String]) {
        scanf(9);
        bSort(9);
    }

}



/*
// C program for implementation of Bubble sort
#include <stdio.h>
 
void swap(int *xp, int *yp)
{
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}
 
// A function to implement bubble sort
void bubbleSort(int arr[], int n)
{
   int i, j;
   for (i = 0; i < n-1; i++)      
 
       // Last i elements are already in place   
       for (j = 0; j < n-i-1; j++) 
           if (arr[j] > arr[j+1])
              swap(&arr[j], &arr[j+1]);
}
 
 
// Driver program to test above functions
int main()
{
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr)/sizeof(arr[0]);
    bubbleSort(arr, n);
    printf("Sorted array: \n");
    printArray(arr, n);
    return 0;
}
*/
