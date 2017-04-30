object Fibonacci {
    def fibo(n : Int) : Int = {
        var f = new Array[Int](1000);
        var i : Int = 0;
        f[0] = 0;
        f[1] = 1;
        for ( i <- 2 until n )
	{
		f[i] = f[i - 1] + f[i - 2];
      	} 
        var t : Int = f[n];
        return t;
    }
    def main()
    {
            var k : Int = 0;
	    println("Please input for fibonacci:");
	    read(k);
	    k = fibo(k);
            println(k);
    }
}


