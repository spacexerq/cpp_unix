#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include "variables_g.cpp"

using namespace std;

vector<Variables_g> var_int;
vector<Var_string> var_str;
vector<string> var_names;

vector <string> split(const string& sentence){
    string word;
    istringstream iss(sentence);
    vector <string> line;
    while (getline(iss, word, ' ')) {
        line.push_back(word);
    }
    return line;
}

void initialization(vector <string> line){
    if(line[0]=="int"){
        Variables_g var1;
        var1.set_variable(line[2],line[1],line[3]);
        var_int.push_back(var1);
        var_names.push_back(line[2]);
    }else if(line[0]=="string"){
        string local_name = line[2];
        Var_string var1;
        var1.set_variable(line[2],line[1],line[3]);
        var_str.push_back(var1);
        var_names.push_back(line[2]);
    }
}

int main(){
    cout << "Welcome to Gecko.alpha!" << endl;
    cout << "Finish the entering by ~" << endl;
    cout << "The variables initialization begins from !" << endl;
    vector <string> text;
    string input;
    int i = 0;
    while (input != "~"){
        cout << i;
        getline(cin,input);
        text.push_back(input);
        i++;
    }
    text.erase(text.end());
    for(const auto & j : text){
        vector <string> line;
        line = split(j);
        bool var_found=find(var_names.begin(), var_names.end(), line[0]) != var_names.end();
        if(line[0]=="!"){
            initialization(line);
        }else if(var_found){

        }else if(line[0]=="for"){

        }else if(line[0]=="*"){

        }else if(line[0]=="~"){
            return 0;
        }else{
            cout << "Input error!" << endl;
            for(int k = 0; k <= size(text); k++){
                if(text[k]==j){
                    cout << j << " <- error here";
                    return 1;
                }
                cout << text[k] << endl;
            }
            return 1;
        }
    }
    return 0;
}