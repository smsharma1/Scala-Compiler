object Good1 {
	var f2 = new List[Int];
	def t(a default 0 : Int, b : Int){
		println(a);
	} 
	def main() {
	var f1 = new Array[Int](10);
	var f = new List[Int];
	append(f,1,2,3);
	deletetail(f);
	append(f,4);
	println(f[2]);
	var a : Int = 55;
	// println("Double quote (\") is escaped");
	t(default a,10);

   }
}
