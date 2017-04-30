object GraphList {
var f3 = new List[Int](10);
    def main(){
        var i : Int = 0;
       	append(f3,1,2,3,4);
	append(f3,3,4);
	println(f3[1,0]);
	println(f3[1,1]);
	println(f3[1,2]);
	println(f3[3,0]);
    }
}
