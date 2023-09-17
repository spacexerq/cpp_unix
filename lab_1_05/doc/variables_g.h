#ifndef CPP_UNIX1_VARIABLES_G_H
#define CPP_UNIX1_VARIABLES_G_H
#include <string>

class Variables_g {
    //default integer variable
public:
    virtual void set_variable(std::string name, std::string type, std::string val);
    int var_get_val() const;
    void var_set_val(int a);
    std::string var_get_name() const;
    std::string var_get_type() const;
private:
    //int || string
    int value;
protected:
    //variable name and type
    std::string var_type {"int"};
    std::string var_name {"None"};
};

class Var_string : public Variables_g{
private:
    std::string value;
public:
    void set_variable(std::string name, std::string type, std::string val);
    void var_set_val(std::string a);
    std::string var_get_val(){return value;}
};

#endif //CPP_UNIX1_VARIABLES_G_H
