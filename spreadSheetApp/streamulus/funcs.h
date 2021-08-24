#pragma once

#include "cpp14_utils.h"

namespace streamulus
{
    template<typename T>
    struct ConstFunc
    {  
    public:
        ConstFunc(const T& value_)
            : mValue(value_)
        {
        }
        
        remove_const_t<remove_reference_t<T>>
        operator()() const
        {
            return mValue;
        }
        
    private:
        T mValue;
    };
    
} // ns streamulus