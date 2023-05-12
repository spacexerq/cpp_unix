#include <iostream>
#include <list>
#include <iterator>
#include <string>
#include <sstream>
#define pow(X, Y)

using namespace std;

void hanoy(int disk_num, int from_stick, int to_stick, int med_stick, list<string> route, int iterations){
    if(disk_num == 0){
        cout << route.size();
        if(route.size()==iterations-1){
            copy(route.begin(),route.end(),ostream_iterator<string>(cout, "\n"));
        }
        return;
    }
    hanoy(disk_num-1, from_stick, med_stick,to_stick,route,iterations);
    stringstream d_num, f_st, t_st;
    d_num << disk_num;
    f_st << from_stick;
    t_st << to_stick;
    cout << d_num.str() << f_st.str() << t_st.str() << "\n";
    string step = d_num.str() + f_st.str() + t_st.str();
    route.push_back(step);
    hanoy(disk_num-1, med_stick, to_stick, from_stick,route,iterations);
}

int main() {
    int disk_num = 3, final_stick = 3, med_stick = 2, first_stick = 1;
    list<string>route;
    int iterations = pow(2, disk_num) - 1;
    hanoy(disk_num, first_stick, final_stick, med_stick, route, iterations);
    return 0;
}
