#pragma once

#include "cpp14_utils.h"

#include <boost/shared_ptr.hpp>

namespace streamulus
{
    namespace detail {
        template<typename StropType>
        struct strop_return_type_impl;

        template<typename StropType>
        struct strop_return_type_impl<std::shared_ptr<StropType> > {
            using type = typename StropType::result_type;
        };
    }

    template<typename StropType>
    using strop_return_type = typename detail::strop_return_type_impl<remove_const_t<StropType>>::type;
}