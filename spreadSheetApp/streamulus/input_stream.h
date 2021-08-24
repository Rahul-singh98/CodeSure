#pragma once

#include "strop_data_source.h"

#include <boost/make_shared.hpp>

namespace streamulus
{
    // Convenience utilities for defining input streams    

    namespace detail {

        template<typename T>
        using input_stream_data_source_t = std::shared_ptr<DataSource<T>>;

        template<typename T>
        using input_stream_proto_expression_t = typename boost::proto::terminal<input_stream_data_source_t<T>>::type;
    }

    template<typename T>
    using InputStream = const detail::input_stream_proto_expression_t<T>;

    // Create a new stream
    template<typename T>
    InputStream<T> NewInputStream(const std::string& name, bool verbose)
    {
        detail::input_stream_proto_expression_t<T> expr = {std::make_shared<DataSource<T> >(name, verbose)};
        return expr;
    }

    // Add an input to the stream
    template<typename T>
    void InputStreamPut(InputStream<T> terminal, const T& value)
    {
        boost::proto::value(terminal)->Tick(value);
    }
    
        
} // ns streamulus