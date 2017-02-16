/*
//Bad test case for parsing - if -else ladder violated
#include<stdio.h>
void main(){
        int a = 0;
        if(a == 0){
                printf("if");
        }else{
                printf(" 1st else");
        }else{
                printf("Error 'else' without a previous 'if' ");
        }
}
*/

object Bad5 {
	def main(args: Array[String]) {
		var a: Int  = 0;
		if( a == 0 ){	
			println("if");
      		} 
		else {
         		println("1st else");
      		}
		else{
			println("Error 'else' without a previous 'if'");
		}
   	}
}
