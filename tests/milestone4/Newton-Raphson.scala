object newtonRaphson{
    def func( x : Float) : Float = {
        var k : Float = x*x*x - x*x + 2;
	println(k);
        return k;
    }
    def derivFunc( x : Float) : Float = {
        var k : Float = 3*x*x - 2*x;
	println(k);
        return k;
    }
    def newtonRaphson(x : Float){
        var h1 : Float = func(x);
	var h2 : Float = derivFunc(x);
	var h : Float = h1/h2;
        var t : Float = h;
	println(h);
        if ( t < 0 ){
            t = t * (-1);
        }
        while(t >= 1)
        {
            h = func(x) / derivFunc(x);  
            x = x - h;
            t = h;
            if ( t < 0 ){
                t = t * (-1);
            }   
        }
        println("The value of the root is :");
        println(x);
    }
     def main(args: Array[String]) {
        var x : Int = -20;
	println(x);
     //   newtonRaphson(x);

     }
}

/*
// C++ program for implementation of Newton Raphson Method for
// solving equations
#include<bits/stdc++.h>
#define EPSILON 0.001
using namespace std;

// An example function whose solution is determined using
// Bisection Method. The function is x^3 - x^2  + 2
double func(double x)
{
    return x*x*x - x*x + 2;
}

// Derivative of the above function which is 3*x^x - 2*x
double derivFunc(double x)
{
    return 3*x*x - 2*x;
}

// Function to find the root
void newtonRaphson(double x)
{
    double h = func(x) / derivFunc(x);
    while (abs(h) >= EPSILON)
    {
        h = func(x)/derivFunc(x);
 
        // x(i+1) = x(i) - f(x) / f'(x)  
        x = x - h;
    }

    cout << "The value of the root is : " << x;
}

// Driver program to test above
int main()
{
    double x0 = -20; // Initial values assumed
    newtonRaphson(x0);
    return 0;
}
*/
