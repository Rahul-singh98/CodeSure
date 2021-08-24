#pragma once

#include <boost/graph/adjacency_list.hpp>

namespace streamulus
{
    
    struct StropTag { using kind = boost::vertex_property_tag; };
    struct StreamTag { using kind = boost::edge_property_tag; };
    
    class StropBase;
    class StreamBase;
    
    using StropPtr = std::shared_ptr<StropBase>;
    using StreamPtr = std::shared_ptr<StreamBase>;
    
    
    using BoostGraph = boost::adjacency_list<boost::vecS
    , boost::vecS
    , boost::bidirectionalS 
    , boost::property<StropTag, StropPtr>
    , boost::property<StreamTag, StreamPtr>
    >;
    
    class Graph : public BoostGraph 
    {
    public:
        using type = BoostGraph;
        
        StropPtr& operator[](const BoostGraph::vertex_descriptor& d)
        {
            return boost::get(StropTag(), *this)[d];
        }
        
        StreamPtr& operator[](const BoostGraph::edge_descriptor& d)
        {
            return boost::get(StreamTag(), *this)[d];
        }	
    };
    
    
} // ns streamulus