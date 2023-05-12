# Report. Lab1
Бабич Никита Станиславович 312400 Z33434 3 курс

## Цель
Познакомить студента с основами администрирования программных комплексов в ОС семейства UNIX, продемонстрировать особенности виртуализации и контейнеризации, продемонстрировать преимущества использования систем контроля версий (на
    примере GIT)
## Task Unix
### Task 1
    cd /
    cd usr
    cd local
    sudo mkdir folder_max
    sudo mkdir folder_min

Result: 2 folders created
### Task 2
    sudo groupadd group_max
    sudo groupadd group_min

Result: 2 user groups created
### Task 3
    sudo useradd user_max_1
    sudo useradd user_min_1

    sudo usermod -a -G group_max user_max_1
    sudo usermod -a -G group_max user_min_1

Result: 2 users added. user_* moved to group_* groups
### Task 4
    sudo chown :group_min folder_min
    sudo chown :group_max folder_max
    
    sudo apt-get install acl

    sudo setfacl -m g:group_max:rwx folder_max
    sudo setfacl -m g:group_max:rwx folder_min
    sudo setfacl -m g:group_min:rwx folder_min

Used acl to define permissions

Result: users from group_max control by rwx folder_max directive
users from group_min control by rwx folder_min directive
### Task 5
    sudo -u user_max_1 vi script1.sh

    #!/bin/sh
    echo $(date -u) >> output.log

    chmod +x script1.sh
    sudo -u user_max_1 ./script1.sh

Result: shell script created with the code given above

script executed by user_max_1 user

output.log created in folder_max
### Task 6
    sudo -u user_max_1 vi script_to_f_min.sh

    #!/bin/sh
    echo $(date -u) >> ../folder_min/output.log

    sudo chmod +x script_to_f_min.sh
    sudo -u user_max_1 ./script_to_f_min.sh

Result: shell script created with the code given above

script executed by user_max_1 user

output.log created in folder_min
### Task 7
    sudo -u user_min_1 ./script_to_f_min.sh

    cannot create ../folder_min/output.log: Permission denied

Result: shell script created with the code given above

script executed by user_min_1 user

output.log could not be created in folder_min because already exists made by user_max_1

Its needed to remake permissions to 777 to debug it
### Task 8
    cd folder_min/
    sudo -u user_min_1 vi script_to_f_max.sh
    sudo chmod +x script_to_f_max.sh
    sudo -u user_min_1 ./script_to_f_max.sh

    ./script_to_f_max.sh: 2: cannot create ../folder_max/output.log: Permission denied
Result: Permission denied (uder_min_1 has no accept to the folder_max)
### Task 9
All permissions

    spx@LAPTOP-M7DTCFMM:/usr/local$ ls -l
    total 40
    drwxr-xr-x  2 root root      4096 Apr 19 00:35 bin
    drwxr-xr-x  2 root root      4096 Apr 19 00:35 etc
    drwxrwxr-x+ 2 root group_max 4096 May 13 00:43 folder_max
    drwxrwxr-x+ 2 root group_max 4096 May 13 00:49 folder_min
    drwxr-xr-x  2 root root      4096 Apr 19 00:35 games
    drwxr-xr-x  2 root root      4096 Apr 19 00:35 include
    drwxr-xr-x  3 root root      4096 Apr 19 00:35 lib
    lrwxrwxrwx  1 root root         9 Apr 19 00:35 man -> share/man
    drwxr-xr-x  2 root root      4096 Apr 19 00:35 sbin
    drwxr-xr-x  4 root root      4096 Apr 19 00:35 share
    drwxr-xr-x  2 root root      4096 Apr 19 00:35 src

/folder_max/ files permissions

    spx@LAPTOP-M7DTCFMM:/usr/local$ ls -l folder_max/
    total 12
    -rw-rw-r-- 1 user_max_1 user_max_1 29 May 13 00:33 output.log
    -rwxrwxr-x 1 user_max_1 user_max_1 40 May 13 00:30 script1.sh
    -rwxrwxr-x 1 user_max_1 user_max_1 54 May 13 00:43 script_to_f_min.sh

/folder_min/ files permission

    spx@LAPTOP-M7DTCFMM:/usr/local$ ls -l folder_min/
    total 8
    -rw-rw-r-- 1 user_max_1 user_max_1 29 May 13 00:43 output.log
    -rwxrwxr-x 1 user_min_1 user_min_1 54 May 13 00:49 script_to_f_max.sh

## Task Docker
### Task 1
    sudo mkdir docker_lab
    cd docker_lab/
    sudo vi scr.sh

script:

    #!/bin/sh
    echo $(dat  e -u) >> output.log
### Task 2
    sudo vi Dockerfile
    docker build -t docker_lab_1 .
    [+] Building 18.7s (8/8) FINISHED

script:

    FROM ubuntu:20.04
    RUN apt update -y && apt install -y nano
    COPY ./scr.sh /scr.sh

Image created with nano package and scr.sh script

    docker images
    REPOSITORY     TAG       IMAGE ID       CREATED         SIZE
    docker_lab_1   latest    b0c23f93550d   4 minutes ago   117MB
    hello-world    latest    9c7a54a9a43c   8 days ago      13.3kB
### Task 3
    docker run -it --rm d_lab_1
    root@12cd117da4ba:/# bash scr
    root@12cd117da4ba:/# bash scr.sh
    root@12cd117da4ba:/# ls
    bin   dev  home  lib32  libx32  mnt  output.log  root  sbin    srv  tmp  var
    boot  etc  lib   lib64  media   opt  proc        run   scr.sh  sys  usr
### Task 4
    docker run --rm d_lab_1 id
    uid=0(root) gid=0(root) groups=0(root)

Only 1 user - 0(root)
## Task Git
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
