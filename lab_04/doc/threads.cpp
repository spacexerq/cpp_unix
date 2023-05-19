#include <iostream>
#include <ctime>
#include <cmath>

using namespace std;

int formula1(int x){
    int f = pow(x,2)- pow(x,2)+ x *4- x *5+ x + x;
    return f;
}

int formula2(int x){
    int f = x+x;
    return f;
}

int formula3(int f1, int f2){
    int f = f1 + f2 - f1;
    return f;
}

int main(){
    int num_iterations = 1000000;
    cout << "Treads paralleling evaluation" << "\n";
    while(num_iterations < 10000001){
        clock_t start = clock();
        for (int i = 0; i <= num_iterations; i++) {
            int x = rand();
            int f1 = formula1(x);
            int f2 = formula2(x);
            int f3 = formula3(f1, f2);
        }
        clock_t end = clock();
        auto seconds = ((double) (end - start)) / CLOCKS_PER_SEC;
        cout << "Time spent for " << num_iterations << " calculations is " << seconds << " seconds" << "\n";
        num_iterations *= 10;
    }
    return 0;
}
