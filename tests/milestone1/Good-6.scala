class node () {
   var x: Int = 1;
   var y: Int = 2; 
   }

object Good6 {
   def main(args: Array[String]) {
      val n = new node(10, 20);
      var y:Int = n.x; 
   }
}
/*//To check for structure syntax
#include<stdio.h>
struct node {
        int x;
        int *y;
};void main() {
struct node n;
}
*/