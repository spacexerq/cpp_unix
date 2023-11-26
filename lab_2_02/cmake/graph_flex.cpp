#include <iostream>
#include <cmath>
#include <chrono>
#include <cstdlib>
#include <random>
#include <matplot/matplot.h>

using namespace std;

void fill_rand(int &len, int massive[][], int &upp_lim, int &low_lim){
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distr(low_lim, upp_lim);
    for(int i=0; i < len; i++){
        massive[0][i] = distr(gen);
        massive[1][i] = distr(gen);
    };
}

float weight(int pos1[2], int pos2[2]){
    return sqrt(pow((pos1[1]-pos2[1]),2)+pow((pos1[2]-pos2[2]),2));
}

int main(){
    using namespace matplot;

    int len_sample = 10;
    int low_lim = 0;
    int upp_lim = 100;
    int coordinates[2][len_sample];
    fill_rand(len_sample, coordinates, upp_lim, low_lim);
    cout << "H";
    plot(,y);
}