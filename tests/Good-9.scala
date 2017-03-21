object Good9 {
   def main(args: Array[String]) {
      var x : Int = 0;
      // An infinite loop.
      while( true ){
         if( x == 2 ){
            x = x + 1;
         }
      }
   }
}
