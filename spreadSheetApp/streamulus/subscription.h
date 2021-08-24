#pragma once 

#include "strop_stream_producer.h"

namespace streamulus {
    
template<typename T>
struct Subscription
{
    using strop_type = const std::shared_ptr<StropStreamProducer<T>>;
    using terminal_type = typename boost::proto::terminal<strop_type>::type;
    using type = const terminal_type;
};

}