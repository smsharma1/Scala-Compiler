object bubbleSort{
    def bSort(arr : Array[Int], n : Int )
    {
        var i : Int = 0;
        var j : Int = 0;
        var temp : Int = 0;
        n  = n - 1;
        for ( i <- 0 until n )
		{
            var t : Int = n - i - 1;
            for ( i <- 0 until t)
		    {
			   if( arr[j] > arr[j + 1] )
               {
                    temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
               }
      	    }
      	}
        for ( i <- 0 until n)
		{
			println(arr[i]);
      	}

    }
    def main(args: Array[String]) {
        var f = new Array[Int](10);
        f[0] = 64;
        f[1] = 34;
        f[2] = 25;
        f[3] = 12;
        f[4] = 22;
        f[5] = 11;
        f[6] = 90;
        f[7] = 5;
        f[8] = 9;
        f[9] = 71;
        bSort(f, 10);
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