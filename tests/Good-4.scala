//Good testcase - Syntax check for nested - if else
/*#include<stdio.h>
void main(){
int a = 0;
        if(a == 0){
                printf("if");
                        if(a > b){
                                        printf("nested if");
                        }else{
                                        printf(" nested else");
                        }
                }
}*/

object Good4 {
def main(args: Array[String]) {
	var a: Int = 0;
      	if( a == 0 ){
         	println("if");
		if(a > b){
			println("nested if");
		}
      	 	else {
         		println("nested else");
      		}
	}
   }
}
