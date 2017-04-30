object Listsearch {
	def main() {
	var f = new List[Int];
    var i : Int = 0;
	append(f,1,2,3);
	deletetail(f);
	append(f,4);
	for ( i <- 0 until 3 ){
        println(f[i]);
    }
   }
}
