#pragma once


#include <sstream>

#include <boost/optional.hpp>

#include "strop.h"

namespace streamulus {
    template<class F, typename... Args>
    class Func : public Strop<typename std::result_of<F(Args...)>::type(Args...)> {
    public:

        using R = typename std::result_of<F(Args...)>::type;
        using StropType = Strop<R(Args...)>;

        Func(const std::function<R(Args...)> &f)
                : mFunction(f), mInputExists(false) {
            std::stringstream ss;
            ss << "Func_" << "F";
            Strop<R(Args...)>::SetDisplayName(ss.str());
        }

        R ApplyFunction() {
            return Strop<R(Args...)>::Invoke(mFunction);
        }


        virtual void Work() {
            mInputExists |= StropType::IsValid();
            if (mInputExists) {
                if (StropType::NoInputs()) {
                    // apply function once for strop without inputs
                    StropStreamProducer<R>::Output(ApplyFunction());
                } else {
                    while (StropType::HasMore()) {
                        // apply function as long as there are more inputsfor strop without inputs
                        StropStreamProducer<R>::Output(ApplyFunction());
                    }
                }
            }
        }

    private:
        bool mInputExists;
        std::function<R(Args...)> mFunction;
    };


}