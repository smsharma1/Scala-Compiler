object Ackermann {
    def acker(m : Int, n : Int) : Int = {
        if(m == 0){
            return n + 1;
        }
        if(n == 0){
            return acker(m - 1,1);
        }
        return acker(m - 1, acker(m, n - 1));
    }
    def main(args: Array[String])
    {
        var m : Int = 0;
        var n : Int = 0;
        for ( m <- 0 until 4 )
		{
            for ( n <- 0 until 10 )
		    {       
			    print(acker(m,n));
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