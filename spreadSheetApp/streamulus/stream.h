#pragma once

#include "stream_base.h"
#include <deque>
#include <boost/optional.hpp>

namespace streamulus {

    /**
     * A stream of Ts, FIFO.
     * Initially empty. Append adds data.
     * HasMore() indicates whether there is unread data in the queue.
     * IsValid() is true if there is data in the queue (read or unread).
     * Current() returns the current value, which is the oldest unread data if there is any, or the youngest read data otherwise.
     */
    template<typename T>
    class Stream : public StreamBase
    {
    public:

        void Append(const T& item)
        {
            mBuffer.push_back(item);
        }

        bool HasMore()
        {
            return !mBuffer.empty();
        }

        bool IsValid()
        {
            return mLastValue || !mBuffer.empty();
        }

        const T& Current()
        {
            if (!mBuffer.empty())
            {
                mLastValue = mBuffer.front();
                mBuffer.pop_front();
            }

            if (!mLastValue) {
                throw std::invalid_argument("Current() called for an empty stream");
            }
            assert(mLastValue);

            // No new data - return last
            return *mLastValue;
        }

    private:

        std::deque<T> mBuffer;
        boost::optional<T> mLastValue;
    };

}