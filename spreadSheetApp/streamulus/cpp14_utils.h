#pragma once

#include <boost/optional.hpp>
#include <type_traits>

namespace streamulus {

    /**
     * emulate missing c++14 shortcuts
     */
    template<class T>
    using remove_reference_t = typename std::remove_reference<T>::type;

    template<class T>
    using remove_pointer_t = typename std::remove_pointer<T>::type;

    template<class T>
    using remove_const_t = typename std::remove_const<T>::type;



    /**
     * remove-optional (where should this live?)
     */

    namespace detail {
            template<typename T>
            struct remove_optional_impl {
                using type = T;
            };

            template<typename T>
            struct remove_optional_impl<boost::optional<T>> {
                using type = T;
            };
    }

    template<typename T>
    using remove_optional = typename detail::remove_optional_impl<remove_reference_t<remove_const_t<T>>>::type;

}