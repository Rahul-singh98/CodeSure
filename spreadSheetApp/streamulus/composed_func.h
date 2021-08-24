#pragma once

#include <boost/optional.hpp>

namespace streamulus 
{
    
    struct ArgType;
    
    template<typename Signature>
    class ComposedFunc;

    template<typename F, typename G>
    class ComposedFunc<F(G(ArgType))>
    {
    public:
        
        
        explicit ComposedFunc(const F& f_ = F(), const G& g_ = G())
            : f(f_)
            , g(g_)
        {
            std::cout << "Composed two functions!" << std::endl;
        }
    
        template<typename Signature>
        struct result;
    
        template<typename This, typename Arg>
        struct result<This(Arg)>
        {
            using G_result_type = typename std::result_of<G(Arg)>::type;
            using F_result_type = typename std::result_of<F(G_result_type)>::type;
            using type = F_result_type;
        };
            
        template<typename Arg>
        typename boost::optional<typename result<ComposedFunc<F(G(ArgType))>(Arg)>::type>
        operator()(const Arg& arg)
        {
            boost::optional<typename result<ComposedFunc<F(G(ArgType))>(Arg)>::G_result_type> g_res = g(arg);
            if (!g_res)
                return boost::none;
            boost::optional<typename result<ComposedFunc<F(G(ArgType))>(Arg)>::F_result_type> f_res = f(*g_res);
            if (!f_res)
                return boost::none;
            return *f_res;
        }
        
    private:
        F f;
        G g;
    };


}