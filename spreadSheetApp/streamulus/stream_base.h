#pragma once

#include "graph.h"

namespace streamulus
{
    class StreamBase 
    {
    public:
        StreamBase()
        : mGraph(nullptr)
        , mIsFeedbackEdge(false)
        {
        }
                 
        const Graph::edge_descriptor& Descriptor() const
        {
            return mEdgeDescriptor;
        }
        
        void SetGraph(const Graph::edge_descriptor& desc, Graph* g) 
        {
            mGraph = g;
            mEdgeDescriptor = desc;
        }
    
        bool IsFeedbackEdge()
        {
            return mIsFeedbackEdge;
        }

        void SetIsFeedbackEdge(bool v)
        {
            mIsFeedbackEdge = v;
        }

    private:
        Graph* mGraph;  // no ownership. do not delete.
        Graph::edge_descriptor mEdgeDescriptor;
        bool mIsFeedbackEdge;
    };
    
}