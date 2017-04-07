object Good9 {
   def main(args: Array[String]) {
      var x : Int = 0;
      var y : Int = 10;
      x = x + y - 10 * 5 / 4 ;
      x = x * y;
      var z : Int = 1;
      z  += y;
      // An infinite loop.
      while( true ){
         if( x == 2 ){
            x = x + y;
            x = x * y;
         }
      }
   }
}
