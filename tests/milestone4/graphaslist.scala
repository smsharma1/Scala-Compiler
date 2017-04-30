object GraphList {
    def main(){
        var f3 = new List[Int](10);
        var inp : Int = 0;
        var i : Int = 0;
        var j : Int = 0;
        var t : Int = 0;
        for ( i <- 0 until 9){
            read(inp);
            inp = inp - 1;
            for ( j <- 0 untill inp){
                read(t);
                f3[i] = t;
            }
        }
    }
}