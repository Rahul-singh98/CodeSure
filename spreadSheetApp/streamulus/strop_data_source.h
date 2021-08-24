#pragma once

#include <iostream>

#include "strop_stream_producer.h"

namespace streamulus
{    
    
    template<typename R>
    class DataSource : public StropStreamProducer<R>  
    {
    public:
        
        DataSource(const std::string& name, bool verbose)
        : mIsValid(false)
        , mIsVerbose(verbose)
        {
            StropStreamProducer<R>::SetDisplayName(name);
        }
                
        virtual void Work()
        {
            // Return the last tick's value. 
            if (mIsValid)
                StropStreamProducer<R>::Output(mLastValue);
        }
            
        inline bool IsVerbose()
        {
            return mIsVerbose;
        }
        
        void Tick(const R& value)
        {
            if (IsVerbose())
                std::cout << "-------------   " 
                          << StropStreamProducer<R>::DisplayName() << " <-- " 
                          << value << "   -------------" << std::endl;
            StropStreamProducer<R>::Output(value); 
            mLastValue = value;
            mIsValid = true;
        }
                
    private:
        R           mLastValue;
        bool        mIsValid;
        bool        mIsVerbose;
    };
    
}