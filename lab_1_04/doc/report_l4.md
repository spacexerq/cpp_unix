# Report. Lab4
Бабич Никита Станиславович 312400 Z33434 3 курс

## Цель
Познакомить студента с принципами параллельных вычислений. Составить несколько
программ в простейшими вычислительными действиями, чтобы освоить принципы
параллельных вычислений (когда одни алгоритмы зависят / не зависят от других).

## Task Sequence

Due to using simple functions, quite fast. Using < chrono > header to control the time.

    Sequence evaluation
    Time spent for 10000 calculations is 0.0014969 seconds
    Time spent for 100000 calculations is 0.0110329 seconds

## Task Threads

Using < future > to separate threads. Nevertheless, no optimization gained. The process of initialization of threads is using more time than any improve give. 

    Treads paralleling evaluation
    Time spent for 10000 calculations is 2.8801 seconds
    Time spent for 100000 calculations is 27.5155 seconds

## Task Processes

Compiled ny WSL Ubuntu. Using pipe()/fork() functions to separate 2 child processes ("formula 1" and "formula 2" execution)

    C:\windows\system32\wsl.exe --distribution Ubuntu --exec /bin/bash -c
        "cd /mnt/c/Users/user/cpp_unix1/lab_04/build && /mnt/c/Users/user/cpp_unix1/lab_04/build/multiprocess"
    Evaluation with parallel processes
    Time spent for 10000 calculations is 0.000508 seconds
    Time spent for 100000 calculations is 0.0024819 seconds

## Task Sequence (by Ubuntu)

sequence.cpp code was also complied by WSL Ubuntu, to be sure, that the data is correct.

    C:\windows\system32\wsl.exe --distribution Ubuntu --exec /bin/bash -c
        "cd /mnt/c/Users/user/cpp_unix1/lab_04/build && /mnt/c/Users/user/cpp_unix1/lab_04/build/sequence"
    Sequence evaluation
    Time spent for 10000 calculations is 0.0008834 seconds
    Time spent for 100000 calculations is 0.008602 seconds

It should be mentioned, that this code is executing faster than code complied by MinGW. But still multiprocessing system has an advantage in time of execution