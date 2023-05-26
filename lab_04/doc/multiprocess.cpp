#include <iostream>
#include <ctime>
#include <cmath>
#include <unistd.h>
#include <sys/wait.h>

using namespace std;

int formula1(int &x){
    int f = pow(x,2)- pow(x,2)+ x *4- x *5+ x + x;
    return f;
}

int formula2(int &x){
    int f = x+x;
    return f;
}

int formula3(int &f1, int &f2){
    int f = f1 + f2 - f1;
    return f;
}

int main(){
    int num_iterations = 10000;
    cout << "Evaluation with parallel processes" << "\n";
    while(num_iterations < 100001){
        clock_t start = clock();
        int x[num_iterations];
        for(int i=0; i<=num_iterations; i++) {
            x[i] = rand();
        }
        int pipe_from_f1[2], pipe_from_f2[2], pipe_initial[2];
        //pipe[0] - write
        //pipe[1] - read
        pipe(pipe_initial);
        pipe(pipe_from_f2);
        pipe(pipe_from_f1);
        write(pipe_initial[1],&x, sizeof(x));
        close(pipe_initial[1]);
        pid_t pid_f1 = fork();
        if (pid_f1 == 0){
            //child 1 process
            int x_f1[num_iterations];
            int f1[num_iterations];
            for(int i1 = 0; i1<=num_iterations; i1++) {
                read(pipe_initial[0], &x_f1[i1], sizeof(pipe_initial[0]));
                f1[i1] = formula1(x_f1[i1]);
                close(pipe_initial[0]);
                write(pipe_from_f1[1], f1, sizeof(f1));
                close(pipe_from_f1[1]);
            }
            return 0;
        } else if (pid_f1 == -1){
            cerr << "Multiprocessing failed.";
            return 1;
        }
        //parent process
        pid_t pid_f2 = fork();
        if (pid_f2 == 0){
            //child 2 process
            int x_f2[num_iterations];
            int f2[num_iterations];
            for(int i2=0; i2<= num_iterations;i2++) {
                read(pipe_initial[0], &x_f2[i2], sizeof(pipe_initial[0]));
                close(pipe_initial[0]);
                f2[i2] = formula2(x_f2[i2]);
            }
            write(pipe_from_f2[1],f2,sizeof(f2));
            close(pipe_from_f2[1]);
            return 0;
        } else if (pid_f2 == -1){
            cerr << "Multiprocessing failed.";
            return 1;
        }
        //parent process
        int from_f1[num_iterations], from_f2[num_iterations];
        read(pipe_from_f1[0], &from_f1, sizeof(from_f1));
        read(pipe_from_f2[0], &from_f2, sizeof(from_f2));
        int f3[num_iterations];
        for(int i=0;i<=num_iterations;i++) {
            f3[i] = formula3(from_f1[i], from_f2[i]);
        }
        close(pipe_from_f1[0]);
        close(pipe_from_f2[0]);
        //end of the main evaluation

        clock_t end = clock();
        auto seconds = ((double) (end - start)) / CLOCKS_PER_SEC;
        cout << "Time spent for " << num_iterations << " calculations is " << seconds << " seconds" << "\n";
        num_iterations *= 10;
    }
    return 0;
}