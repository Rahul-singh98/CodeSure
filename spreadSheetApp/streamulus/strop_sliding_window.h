#pragma once

#include <boost/circular_buffer.hpp>

namespace streamulus 
{

    enum WindowInOut { DATA_IN, DATA_OUT };
    
    template<typename T>
    using WindowUpdateType = std::pair<WindowInOut,T>;

    template<typename T>
    struct WindowBaseType;
    
    template<typename T>
    struct WindowBaseType<std::pair<WindowInOut,T> >
    {
        using type = T;
    };
    
    template<typename T>
    class Window : public Strop<WindowUpdateType<T>(T)>
    {
    public:
        using R = WindowUpdateType<T>;
        
        Window(size_t size)
            : mBuffer(size)
        {
        }
        
        virtual void Work()
        {
            Stream<T>* const input = Strop<R(T)>::template Input<0>();
            
            assert(input->IsValid());
            
            while (input->HasMore())
            {
                if (mBuffer.reserve() == 0)
                    StropStreamProducer<R>::Output(std::make_pair(DATA_OUT,mBuffer.front()));                       

                const T& value(input->Current());
                mBuffer.push_back(value);
                StropStreamProducer<R>::Output(std::make_pair(DATA_IN,value));   
            }
        }
        
    private:
        boost::circular_buffer<T> mBuffer;  
    };
    
}