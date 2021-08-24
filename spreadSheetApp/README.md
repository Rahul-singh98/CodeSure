# SpreadSheetApp

This app is createded as an example on how we can create cell and how stream processing works.

## How to run :- 
* First of all you need to install boost in your system.
  [Download Boost](https://www.boost.org/users/download/)

  Boost provides free peer-reviewed portable C++ source libraries.

  Boost emphasize libraries that work well with the C++ Standard Library. Boost libraries are intended to be widely useful, and usable across a broad spectrum of applications. The Boost license encourages the use of Boost libraries for all users with minimal restrictions.
  
  Once you downloaded tarfile in you system , then you only need to untar file.
  ```shell
  tar --bzip2 -xf ~/Downloads/boost_1_77_0.tar.bz2
  ```

* After installing boost , now need to install streamulus functions. [Download streamulus](https://github.com/iritkatriel/streamulus)
  
  Streamulus is a C++ library that makes it very easy to process event streams. You need to write code that handles a single event and the library turns this code into a data structure that handles infinite streams of such events. The stream operators you write can have side effects and they can maintain an internal state.

  After successfull cloning respository , we are all set with prerequisites.

* Now , edit the path of **Boost** and **Streamulus** in ***CMakeLists.txt***.
  ```text
  set(BOOST_ROOT "/path/to/downloaded/boostdirectory/boost_1_77_0") # path where boost is installed
  set(BOOSTROOT "/path/to/downloaded/boostdirectory/boost_1_77_0")  # path where boost is installed
  ```
  and 

  ```text
  include_directories("/path/to/streamulus")
  ```

* Now , we jus need to build cmake.
  ```c++
  cmake ../spreadSheetApp
  ```

* Build app using cmake.
  ```c++
  cmake --build .
  ```

**Success !!! :dart:**
Now , we have successfully created our app we only need to run the app.

```c++
./spreadSheetApp
```

That's All :blush:.