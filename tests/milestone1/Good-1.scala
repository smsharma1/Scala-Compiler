object Good1 {
	def t(a default 0 : Int, b : Int){
		println(a);
	}
	def main() {
	var a : Int = 	55	;
	println("Double quote (\") is escaped");
	t(default a,10);
   }
}
