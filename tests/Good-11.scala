object Good11 {
	def main(args: Array[String]) {
		println("Enter a value");
        var x=scala.io.StdIn.readInt();
		if( x > 0 ){
            println(x);
	    }
		else {
        	println("Number is zero");
		}
    }
}
