//Good test case to test multiple line string.
object Good2 {
	def main(args: Array[String]) {
	val name :String = """I am in "
					"more than"
					"line."""";
	println(name);
   }
}
