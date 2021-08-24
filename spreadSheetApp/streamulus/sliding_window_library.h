#pragma once

#include "boost/tuple/tuple.hpp"
#include "boost/tuple/tuple_io.hpp"

namespace streamulus
{
    struct WindowCount
    {
    public:
        WindowCount() : mCount(0)
        {
        }
        
        template<typename Sig>
        struct value_type
        {
            using type = long;
        };
        
        template<typename T>
        void Insert(const T& value)
        {
            mCount++;
        }
        
        template<typename T>        
        void Remove(const T& value)
        {
            mCount--;
        }
        
        long Value() const
        {
            return mCount;
        }
        
    private:
        long mCount;
    };

    
    template<typename T>
    struct WindowSum
    {
    public:
        WindowSum() : mSum(0)
        {
        }
    
        template<typename Sig>
        struct value_type
        {
            using type = T;
        };

        void Insert(const T& value)
        {
            mSum += value;
        }
    
        void Remove(const T& value)
        {
            mSum -= value;
        }
    
        const T& Value() const
        {
            return mSum;
        }
    
    private:
        T mSum;
    };

    template<typename T>
    struct WindowAvg
    {
    public:
        WindowAvg() 
        {
        }

        using OutputType = boost::tuple<double,double,long>;
        
        template<typename Sig>
        struct value_type
        {
            using type = OutputType;
        };

        void Insert(const T& value)
        {
            mSum.Insert(value);
            mCount.Insert(value);
        }
        
        void Remove(const T& value)
        {
            mSum.Remove(value);
            mCount.Remove(value);
        }
        
        const OutputType Value() const
        {
            long count(mCount.Value());
            double sum(sum);
            double avg(count ? sum/count : 0);
            return boost::make_tuple(avg,sum,count);
        }
        
    private:
        WindowSum<T> mSum;
        WindowCount mCount;
    };
    
}