#pragma once
#include <boost/optional.hpp>

#include "strop_sliding_window.h"

namespace streamulus
{
    template<typename F>
    class WindowFunc 
    {
    public:

        WindowFunc()
        : mFunction(F())
        {
        }
        
        WindowFunc(const F& f)
            : mFunction(f)
        {
        }

        template<typename WA>
        boost::optional<typename F::template value_type<F(typename WindowBaseType<WA>::type)>::type>
        operator()(const WA& window_update) 
        { 
            if (window_update.first == DATA_OUT)
            {
                mFunction.Remove(window_update.second);
                return boost::none;
            }
            mFunction.Insert(window_update.second);
            return mFunction.Value();
        }
        
    private:
        F mFunction;
    };
    
}