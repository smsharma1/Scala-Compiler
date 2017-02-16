object Good8 {
	def main(args: Array[String]) {
        var a = Array(1, 2, 3, 4, 5);
        val c=0;
        for ( i <- 0 to 4) {
            c += a(i)
        }
        println("sum is " + c);
    }
}