object sort {
    var a = new Array[Int](10);
    def partition(low: Int, high: Int): Int= {
            var pivot: Int = a[high];
            var i :Int = low - 1;
            var j : Int = low;
            var till : Int = high - 1;
            for ( j <- low until till )
	   {
                if (a[j] <= pivot)
                {
                    i = i + 1;    // increment index of smaller element
                    var temp : Int = a[i];
                    a[i] = a[j];
                    a[j] = temp;
                }
            }
            till = a[i + 1];
            a[i + 1] = a[high];
            a[high] = till;
            i = i + 1;
            return i;
        }
     def quickSort(low: Int, high: Int){
            if (low < high)
            {
                var pi : Int = partition(low, high);
		var t : Int = pi - 1;
		var u : Int = pi + 1;
                quickSort(low, t);
                quickSort(u, high);
            }
     }
     def print(size: Int){
            var i : Int = 0;
	    var filew : Int = 0;
	    filew = fopen("output", "w");
	    var out : Int = 0;
            for ( i <- 0 until size )
	    {
		out = a[i];
		fwrite(filew, out);
//                println(a[i]);
            }
	    fclose(filew);
     } 
    def scan(size: Int){
            var i : Int = 0;
            var t : Int = 0;
	    var filep : Int = 0;
	    filep = fopen("data.txt", "r");
            for ( i <- 0 until size )
	    {
                fread(filep, t);
                a[i] = t;
            }
	    fclose(filep);
     } 
     def main() {
         scan(9);	 
         quickSort(0,9);
	// var iamwr : Int = 4;
	// var filep : Int = 0;
	// filep = fopen("output", "w");
	// fwrite(filep, iamwr);
	// fclose(filep);
         print(9);
     }
}


/*
#include<stdio.h>
 
// A utility function to swap two elements
void swap(int* a, int* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}
int partition (int arr[], int low, int high)
{
    int pivot = arr[high];    // pivot
    int i = (low - 1);  // Index of smaller element
 
    for (int j = low; j <= high- 1; j++)
    {
        // If current element is smaller than or
        // equal to pivot
        if (arr[j] <= pivot)
        {
            i++;    // increment index of smaller element
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}
void quickSort(int arr[], int low, int high)
{
    if (low < high)
    {
        int pi = partition(arr, low, high);
 
        // Separately sort elements before
        // partition and after partition
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
void printArray(int arr[], int size)
{
    int i;
    for (i=0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}
 
// Driver program to test above functions
int main()
{
    int arr[] = {10, 7, 8, 9, 1, 5};
    int n = sizeof(arr)/sizeof(arr[0]);
    quickSort(arr, 0, n-1);
    printf("Sorted array: \n");
    printArray(arr, n);
    return 0;
}
*/
