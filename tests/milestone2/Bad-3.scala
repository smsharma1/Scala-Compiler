object Bad3 {
    def f( a:Int ) : Int = { 
        a = a + 1;
		return a;
	 }
   def main(args: Array[String]) {
        var f : Int = 0;
        var g : Int = 0;
        g = f(4);
   }
}

/*
int f(int a) {
    return a+1;
}
int main() {
    int f, g;
    g = f(4);
    return 0;
}
*/