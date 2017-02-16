// This test is to test the user-defined data type.
// typedef int myint; /* here myint should be identifier*/
// myint a; /* Here myint should be Data Type*/ // By- Nishit
object Good12 {
def main(args: Array[String]) {

   var long_variable:Long = 1234567;
   printf("Size for long long int data type " + SizeEstimator.estimate(long_variable));
   return 0;
}
}
