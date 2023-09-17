#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include "variables_g.cpp"
#include <unistd.h>

using namespace std;

vector<Variables_g> var_int;
vector<Var_string> var_str;
vector<string> var_names;

void code_return(const string &error_name, vector<string> text, const string &j) {
    cout << error_name << endl;
    for (int k = 0; k < size(text); k++) {
        if (text[k] == j) {
            cout << j << " <- error here";
        }
        cout << text[k] << endl;
    }
}

vector<string> split(const string &sentence) {
    string word;
    istringstream iss(sentence);
    vector<string> line;
    while (getline(iss, word, ' ')) {
        line.push_back(word);
    }
    return line;
}

void initialization(vector<string> line) {
    if (line[1] == "int") {
        Variables_g var1;
        var1.set_variable(line[2], line[1], line[3]);
        var_int.push_back(var1);
        var_names.push_back(line[2]);
    } else if (line[1] == "string") {
        string local_name = line[2];
        Var_string var1;
        var1.set_variable(line[2], line[1], line[3]);
        var_str.push_back(var1);
        var_names.push_back(line[2]);
    } else {
        vector<string> out;
        string out_s = "...";
        out.push_back(out_s);
        code_return("Invalid type", out, out_s);
    }
}

Variables_g var_search_int(const string &name) {
    if (size(var_int) == 0) {
        Variables_g NoFound;
        NoFound.set_variable("NoFound", "int", "0");
        return NoFound;
    }
    for (int i = 0; i <= size(var_int); i++) {
        if (var_int[i].var_get_name() == name) {
            return var_int[i];
        }
    }
    Variables_g NoFound;
    NoFound.set_variable("NoFound", "int", "0");
    return NoFound;
}

Var_string var_search_str(const string &name) {
    if (size(var_str) == 0) {
        Var_string NoFound;
        NoFound.set_variable("NoFound", "int", "0");
        return NoFound;
    }
    for (int i = 0; i <= size(var_str); i++) {
        if (var_str[i].var_get_name() == name) {
            return var_str[i];
        }
    }
    Var_string NoFound;
    NoFound.set_variable("NoFound", "int", "0");
    return NoFound;
}

bool var_found(const string &var) {
    return find(var_names.begin(), var_names.end(), var) != var_names.end();
}

void overwrite(const string &name, const string &value) {
    int flag = -1;
    string var_type;
    if (var_search_int(name).var_get_name() == "NoFound") {
        for (int l = 0; l < size(var_str); l++) {
            if (var_str[l].var_get_name() == name) {
                flag = l;
            }
        }
        var_str.erase(var_str.begin() + flag);
        Var_string v1;
        v1.set_variable(name, var_type, value);
        var_str.insert(var_str.begin() + flag, v1);
    } else {
        for (int l = 0; l < size(var_int); l++) {
            if (var_int[l].var_get_name() == name) {
                flag = l;
                var_type = var_int[l].var_get_type();
            }
        }
        var_int.erase(var_int.begin() + flag);
        Variables_g v1;
        v1.set_variable(name, var_type, value);
        var_int.insert(var_int.begin() + flag, v1);
    }
}

int compiler(vector<string> text) {
    int lines_iterator = 0;
    int len_code = size(text);
    for (int j_it = 0; j_it < len_code; j_it++) {
        string j = text[j_it];
        vector<string> line;
        line = split(j);
        if (line[0] == "!") {
            if (var_found(line[2])) {
                if (line[1] == "int") {
                    var_search_int(line[2]).var_set_val(stoi(line[3]));
                } else if (line[1] == "string") {
                    var_search_str(line[2]).var_set_val(line[3]);
                }
            }
            initialization(line);
        } else if (var_found(line[0])) {
            string res_var = line[0];
            string var1 = line[2];
            string var2 = line[4];
            string operator2 = line[3];
            if (not var_found(var1) or not var_found(var2)) {
                code_return("The variable was not initialized", text, j);
                return 1;
            } else if (line[1] != "=" or
                       not(operator2 == "+" or operator2 == "*" or operator2 == "/" or operator2 == "-")) {
                code_return("Input error", text, j);
                return 1;
            } else if (var_search_str(var1).var_get_type() == "string" or
                       var_search_str(var2).var_get_type() == "string") {
                code_return("Invalid variable's type", text, j);
                return 1;
            } else {
                if (operator2 == "+") {
                    int res = var_search_int(var1).var_get_val();
                    res += var_search_int(var2).var_get_val();
                    var_search_int(res_var).var_set_val(res);
                    overwrite(res_var, to_string(res));
                    /*
                    vector <Variables_g> gl_var_int = var_int;
                    vector <Var_string> gl_var_str = var_str;
                     */
                } else if (operator2 == "-") {
                    int res = var_search_int(var1).var_get_val();
                    res -= var_search_int(var2).var_get_val();
                    var_search_int(res_var).var_set_val(res);
                    overwrite(res_var, to_string(res));
                } else if (operator2 == "*") {
                    int res = var_search_int(var1).var_get_val();
                    res *= var_search_int(var2).var_get_val();
                    var_search_int(res_var).var_set_val(res);
                    overwrite(res_var, to_string(res));
                } else if (operator2 == "/") {
                    int res = var_search_int(var1).var_get_val();
                    res /= var_search_int(var2).var_get_val();
                    var_search_int(res_var).var_set_val(res);
                    overwrite(res_var, to_string(res));
                }
            }
        } else if (line[0] == "for") {
            int num_repeats = stoi(line[1]);
            vector<string> loop_inside;
            int t = 0;
            int flag_input = 0;
            string loop_sent;
            while (1 == 1) {
                if (text[t] == j) {
                    flag_input = 1;
                }
                if (text[t] == "%") {
                    flag_input = -1;
                }
                if (flag_input == 1 and t + 1 < size(text)) {
                    loop_sent = text[t + 1];
                    loop_inside.push_back(loop_sent);
                } else if (flag_input == -1) {
                    loop_inside.pop_back();
                    break;
                }
                t++;
            }
            for (int n = 0; n < num_repeats; n++) {
                text.insert(text.begin() + lines_iterator + n * size(loop_inside), loop_inside.begin(),
                            loop_inside.end());
            }
            int del_beg = lines_iterator + num_repeats * size(loop_inside);
            int del_end = lines_iterator + (num_repeats + 1) * size(loop_inside) + 2;
            text.erase(text.begin() + del_beg, text.begin() + del_end);
            len_code = size(text);
        } else if (line[0] == "*") {
            vector<string> child_inside;
            int t = 0;
            int flag_input = 0;
            string child_sent;
            while (1 == 1) {
                if (text[t] == j) {
                    flag_input = 1;
                }
                if (text[t] == "#") {
                    flag_input = -1;
                }
                if (flag_input == 1 and t + 1 < size(text)) {
                    child_sent = text[t + 1];
                    child_inside.push_back(child_sent);
                } else if (flag_input == -1) {
                    child_inside.pop_back();
                    break;
                }
                t++;
            }
            int del_beg_f = lines_iterator;
            int del_end_f = lines_iterator + size(child_inside) + 2;
            text.erase(text.begin() + del_beg_f, text.begin() + del_end_f);
            len_code = size(text);
            pid_t pid = fork();
            if (pid == 0) {
                compiler(child_inside);
            } else if (pid == -1) {
                cerr << "Fork error";
                return -1;
            }
            lines_iterator--;
            j_it--;
        } else if (line[0] == "~") {
            return 0;
        } else if (line[0] == "print") {
            if (var_found(line[1])) {
                Variables_g int_out = var_search_int(line[1]);
                Var_string str_out = var_search_str(line[1]);
                if (int_out.var_get_name() == "NoFound") {
                    cout << str_out.var_get_val() << endl;
                } else if (str_out.var_get_name() == "NoFound") {
                    cout << int_out.var_get_val() << endl;
                } else {
                    code_return("Error printing", text, j);
                }
            }
        } else {
            code_return("Input error", text, j);
            return 1;
        }
        lines_iterator++;
    }
}

int main() {
    cout << "Welcome to Gecko.alpha!" << endl;
    cout << "Finish the entering by ~" << endl;
    cout << "The variables initialization begins from ! vType vName value" << endl;
    cout << "Changes made by 'V1 = V2 + V3'" << endl;
    cout << "Loop begins with 'for nReps' and ends with %" << endl;
    cout << "Parallel process begins with '*' and ends with #" << endl << "\n";
    vector<string> text;
    string input;
    int i = 0;
    while (input != "~") {
        //cout << i;
        getline(cin, input);
        text.push_back(input);
        i++;
    }
    text.erase(text.end());
    cout << "Output:" << endl;
    compiler(text);
    return 0;
}