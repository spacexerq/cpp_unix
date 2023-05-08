#include <iostream>
#include <cmath>
#include <ctime>
#include <cstdlib>

using namespace std;

double plusF(double a, double b){
    return a+b;
}

double minusF(double a, double b){
   return a-b;
}

double powerF(double a, double b){
    double result = 1;
    for(int i = 0; i<b; i++){
        result*=a;
    }
    return result;
}

int main() {
    double a, b, result;
    string operatorF;
    int flag = 0;
    cout << "Enter the numbers: ";
    cin >> a >> b;
    if (cin.get() != (double) '\n') {
        cout << "Invalid input type, calculation denied";
        return 0;
    }
    while (flag == 0) {
        cout << "Enter operator (+, -, ^): ";
        cin >> operatorF;
        if (operatorF == "+") {
            result = plusF(a, b);
            flag = 1;
        } else if (operatorF == "^") {
            result = powerF(a, b);
            flag = 1;
        } else if (operatorF == "-") {
            result = minusF(a, b);
            flag = 1;
        } else {
            cout << "Invalid operator, try again!\n";
        }
    }
    cout << "Result:" << result <<"\n";
    system("pause");
}