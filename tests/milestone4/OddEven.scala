object OddEven{
    def iseven(n : Int) : Int = {
        if(n == 0){
            return 1;
        }
        else{
            n = n - 1;
            var t : Int = isodd(n);
            return t;
        }
    }
    def isodd(l : Int) : Int = {
        if(l == 0){
            return -1;
        }
        else{
            l = l - 1;
            var z : Int = iseven(l);
            return t;
        }
    }
    def main(){
        var m : Int = 10;
        read(m);
        m = iseven(m);
        println(m);
    }
}

