#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include "variables_g.cpp"

using namespace std;
int main(){
    string sentence = "int var1 15";
    string sentence2 = "string check_ck try";
    string word;
    string word2;
    istringstream iss(sentence);
    istringstream iss2(sentence2);
    vector <string> line;
    /*
    while (getline(iss, word, ' ')) {
        line.push_back(word);
    }*/
    while (getline(iss2, word2, ' ')) {
        line.push_back(word2);
    }

    if(line[0]=="int"){
        Variables_g var1;
        var1.set_variable(line[1],line[0],line[2]);
        cout << var1.var_get();
    }else if(line[0]=="string"){
        Var_string var1;
        var1.set_variable(line[1],line[0],line[2]);
        cout << var1.var_get();
    }
    return 0;
}