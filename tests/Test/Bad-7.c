//Expression parsing
//Bad test case for - 'for' loop
/*#include<stdio.h>
void main(){
	for(int i = 0; i++){
    	printf("there is an error");
	}}
*/
object Bad7 {
	def main(args: Array[String]) {
        for ( i <- 0 to) {
        println("there is an error");
        }
    }
}