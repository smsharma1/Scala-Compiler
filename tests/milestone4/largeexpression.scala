object largeexpression {
    def sub(a : Int, b : Int, c : Int, d : Int, e : Int, f : Int, g : Int, h : Int) : Int ={
		return a - b + c * d + e - f * g + h * a * b * c * d * e * f * g * h - a - b - c - d - e - f - g - h + a + b + c + d + e + f + g;
	 }
    def main(args: Array[String]) {
        var k : Int = sub(1,2,3,4,5,6,7,8);
        println(k);
    }
}