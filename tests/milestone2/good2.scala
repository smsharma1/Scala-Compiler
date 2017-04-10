class node () {
   var x: Int = 1;
   var y: Float = 1.1; 
    }

class hello_world () {
    var a: Int = 1;
    var b: Int = 1.1;
}

object Good1 {
    def get_a(k: new node()) : Int = { //don't even know how to write code
		return k;
	 }
   def main(args: Array[String]) {
      var b : Int = 1;
      var a : Int = 1;
      var k = new node();
      a = get_a(k);
   }
}

/*struct hello {
    int a;
    float b;
};

struct hello_world {
    int a;
    float b;
};

int get_a(struct hello k) {
    return k.a;
}

int main() {
    int b;
    int a;
    struct hello k;  

    a = get_a(k);

    return 0;
}
*/