#ifndef CPP_UNIX1_VARIABLES_G_H
#define CPP_UNIX1_VARIABLES_G_H
#include <string>

class Variables_g {
    //default integer variable
public:
    virtual void set_variable(std::string name, std::string type, std::string val);
    int var_get() const;
private:
    //int || string
    int value {0};
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
    std::string var_get(){return value;}
};

#endif //CPP_UNIX1_VARIABLES_G_H
