object Ackermann {
    def acker(m : Int, n : Int) : Int = {
	var t : Int = 0;
	var z : Int = 0;
	var l : Int = 0;
        if(m == 0){
	    t = n + 1;
            return t;
        }
        if(n == 0){
		z = m - 1 ;
	    t  = acker(z,1);
            return t;
        }
    z = n - 1;
    l = acker(m,z);
	z = m - 1;
	t = acker(z, l);
    return t; 
    }

    def main()
    {
        var m : Int = 0;
        var n : Int = 0;
		var k : Int = 0;
        for ( m <- 0 until 3 )
		{
            for ( n <- 0 until 9 )
	    	{   
				k = acker(m,n);
	    		println(k);
      	  	}
      	} 

    }
}

/*
#include <iostream>

unsigned int ackermann(unsigned int m, unsigned int n) {
	if (m == 0) {
		return n + 1;
	}
	if (n == 0) {
		return ackermann(m - 1, 1);
	}
	return ackermann(m - 1, ackermann(m, n - 1));
}

int main() {
	for (unsigned int m = 0; m < 4; ++m) {
		for (unsigned int n = 0; n < 10; ++n) {
			std::cout << "A(" << m << ", " << n << ") = " << ackermann(m, n) << "\n";
		}
	}
}
*/
