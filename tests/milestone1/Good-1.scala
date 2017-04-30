object Good1 {
	var f2 = new List[Int];
	var f3 = new List[Int](10);
/*	def t(a default 0 : Int, b : Int){
		println(a);
	} */
	def main() {
	var f1 = new Array[Int](10);
	var f = new List[Int];
	append(f,1,2,3);
	append(f3,1,2,3);
	deletetail(f);
	deletetail(f3,1);
	// println(f3[1]);
	append(f,4);
	// println(f3[0]);
	var a : Int = f3[0,1];
	println(a);
	// println("Double quote (\") is escaped");
//	t(default a,10);

   }
}
