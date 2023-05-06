# Report. Lab1
Бабич Никита Станиславович 312400 Z33434 3 курс

## Цель
Познакомить студента с основами администрирования программных комплексов в ОС семейства UNIX, продемонстрировать особенности виртуализации и контейнеризации, продемонстрировать преимущества использования систем контроля версий (на
    примере GIT)
### Task 1
    cd /
    cd usr
    cd local
    sudo mkdir folder_max
    sudo mkdir folder_min
### Task 2
    sudo groupadd group_max
    sudo groupadd group_min
### Task 3
    sudo useradd user_max_1
    sudo useradd user_min_1
### Task 4
    sudo chown :group_min folder_min
    sudo chown :group_max folder_max
    
    sudo usermod -g group_max spacexer
    sudo chmod g+rwx folder_min

    sudo usermod -g group_min spacexer
    sudo chmod g+rwx folder_min
### Task 5
### Task 6
### Task 7
### Task 8
### Task 9
    git clone https://github.com/spacexerq/cpp_unix.git
    cd cpp_unix
    cd lab_01
    cd build
    git add README.md
    git commit -m \"initial
    cd..
    cd cmake
    git add README.md
    git commit -m \"initial\"
    cd ..
    cd doc
    git add README.md
    git commit -m \"initial\"
    cd ..
    cd src
    git add README.md
    git commit -m \"initial\"
    cd ..
    
    git branch -M dev
    git push origin dev
    
    git branch stg
    git push origin stg
    
    git branch prd
    git push origin prd
    
    git push origin --delete main

