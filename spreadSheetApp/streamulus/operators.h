#pragma once

#include "cpp14_utils.h"

#include <boost/type_traits.hpp> 
#include <boost/proto/proto.hpp>

namespace streamulus
{       
    template<typename TAG>
    struct functor_of;
    
    template<>
    struct functor_of<boost::proto::tag::unary_plus> 
    {
        template<typename A>
        A operator()(const A& value) const
        { 
            return +value; 
        }
    };
     
    template<>
    struct functor_of<boost::proto::tag::negate> 
    {
        template<typename A>
        A operator()(const A& value) const
        { 
            return -value; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::dereference> 
    {
        template<typename A>
        remove_pointer_t<A> operator()(const A& value) const
        { 
            return *value; 
        }
    };
    
    
    template<>
    struct functor_of<boost::proto::tag::complement> 
    {
        template<typename A>
        A operator()(const A& value) const
        { 
            return ~value; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::address_of>  
    {
        template<typename A>
        typename boost::add_pointer<A>::type operator()(A& value) const
        { 
            return &value; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::logical_not> 
    {
        template<typename A>
        bool operator()(const A& value) const
        { 
            return !value; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::pre_inc> 
    {
        template<typename A>
        A operator()(const A& value) const
        {
            remove_const_t<A> res(value);
            return ++res; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::pre_dec> 
    {
        template<typename A>
        A operator()(const A& value) const
        { 
            remove_const_t<A> res(value);
            return --res; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::post_inc> 
    {
        template<typename A>
        A operator()(const A& value) const
        {
            remove_const_t<A> res(value);
            return res++; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::post_dec> 
    {
        template<typename A>
        A operator()(const A& value) const
        {
            remove_const_t<A> res(value);
            return res--; 
        }
    };
    
    
    template<>
    struct functor_of<boost::proto::tag::shift_left> 
    {
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        { 
            return lhs<<rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::shift_right> 
    {
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            return lhs>>rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::multiplies> 
    {
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs*rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::divides> 
    {
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs/rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::modulus> 
    {
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs%rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::plus> 
    {
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs+rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::minus> 
    {    
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs-rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::less> 
    {
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs<rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::greater> 
    {    
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs>rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::less_equal> 
    {    
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs<=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::greater_equal> 
    {    
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs>=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::equal_to> 
    {    
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs==rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::not_equal_to> 
    {    
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs!=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::logical_or> 
    {
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs||rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::logical_and> 
    {    
        template<typename A, typename B>
        bool operator()(const A& lhs, const B& rhs) const
        { 
            return lhs&&rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::bitwise_or> 
    {
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs|rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::bitwise_and> 
    {    
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs&rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::bitwise_xor> 
    {    
        template<typename A, typename B>
        typename boost::common_type<A,B>::type
        operator()(const A& lhs, const B& rhs) const
        { 
            return lhs^rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::comma> 
    {
        template<typename A, typename B>
        B operator()(const A& lhs, const B& rhs) const
        { 
            return lhs,rhs; 
        }
    };
    
    
    template<>
    struct functor_of<boost::proto::tag::assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::shift_left_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy <<= rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::shift_right_assign> 
    {
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy >>= rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::multiplies_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy*=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::divides_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy/=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::modulus_assign> 
    {
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy%=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::plus_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy+=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::minus_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy-=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::bitwise_and_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy&=rhs; 
        }
    };
    
    template<>
    struct functor_of<boost::proto::tag::bitwise_or_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy|=rhs; 
        }
    };
    
    
    template<>
    struct functor_of<boost::proto::tag::bitwise_xor_assign> 
    {    
        template<typename A, typename B>
        A operator()(const A& lhs, const B& rhs) const
        {
            remove_const_t<A> dummy(lhs);
            return dummy^=rhs; 
        }
    };
    
    
    template<>
    struct functor_of<boost::proto::tag::subscript> 
    {    
        // TODO: this will work for arrays but not in general. fix or remove.

        template<typename A, typename B>
        remove_pointer_t<A>
        operator()(const A& array, const B& index) const
        { 
            return array[index]; 
        }
    };
    
    
    template<>
    struct functor_of<boost::proto::tag::if_else_> 
    {
        template<typename A, typename B, typename C>
        typename boost::common_type<A,B>::type
        operator()(const A& condition, const B& yes, const C& no) 
        { 
            return condition ? yes : no; 
        }
    };
    
} 