#include "variables_g.h"
#include <utility>

int Variables_g::var_get_val() const {
    return value;
}

std::string Variables_g::var_get_name() const {
    return var_name;
}

std::string Variables_g::var_get_type() const {
    return var_type;
}

void Variables_g::set_variable(std::string name, std::string type, std::string val) {
    var_type = std::move(type);
    var_name = std::move(name);
    value = stoi(val);
}

void Var_string::set_variable(std::string name, std::string type, std::string val) {
    var_type = std::move(type);
    var_name = std::move(name);
    value = std::move(val);
}

void Variables_g::var_set_val(int val) {
    value = val;
}

void Var_string::var_set_val(std::string val) {
    value = std::move(val);
}
