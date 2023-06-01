#include "variables_g.h"
#include <utility>

int Variables_g::var_get() const {
    return value;
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
