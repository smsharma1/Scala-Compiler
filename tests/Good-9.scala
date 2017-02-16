// To check the the structure of for loop:
object Good9 {
   def main(args: Array[String]) {
      var x = 0;
      // An infinite loop.
      while( True ){
         if( x == 2 ){
            x = x + 1;
         }
      }
   }
}
