#pragma once

#include "cell.hpp"
#include "operators.hpp"
#include "math_funcs.hpp"

namespace spreadsheet {
    
class Spreadsheet
{
public:
    
    template<typename T>
    void InitCell(Cell<T>& cell, const std::string& name)
    {
        cell.SetEngine(&mStreamulusEngine, name);
    }
    
    template<typename T>
    Cell<T> NewCell(const std::string& name = "")
    {
        return Cell<T>(&mStreamulusEngine, name);
    }
    
private:
    streamulus::Streamulus mStreamulusEngine;
};
    
    
}