#include <iostream>
#include <ctime>
#include <cmath>
#include <unistd.h>

using namespace std;

int formula1(int &x) {
    int f = pow(x, 2) - pow(x, 2) + x * 4 - x * 5 + x + x;
    return f;
}

int formula2(int &x) {
    int f = x + x;
    return f;
}

int formula3(int &f1, int &f2) {
    int f = f1 + f2 - f1;
    return f;
}

int main() {
    int num_iterations = 10000;
    cout << "Evaluation with parallel processes" << "\n";
    while (num_iterations < 100001) {
        clock_t start = clock();
        int x[num_iterations];
        for (int i = 0; i <= num_iterations; i++) {
            x[i] = rand();
        }
        int pipe_from_f1[2], pipe_from_f2[2], pipe_step_1[2], pipe_step_2[2];
        //pipe[0] - write
        //pipe[1] - read
        pipe(pipe_step_1);
        pipe(pipe_step_2);
        pipe(pipe_from_f2);
        pipe(pipe_from_f1);
        pid_t pid_f1 = fork();
        if (pid_f1 == 0) {
            cout << "1 init" << "\n";
            //child 1 process
            int f1[num_iterations];
            for (int i1 = 0; i1 <= num_iterations; i1++) {
                f1[i1] = formula1(x[i1]);
                write(pipe_from_f1[1], &f1[i1], sizeof(f1[i1]));
                write(pipe_step_1[1],&i1,sizeof(num_iterations));
                //cout << "p1" << i1 << endl;
            }
            close(pipe_from_f1[1]);
            close(pipe_step_1[1]);
            cout << "end of 1" << endl;
            return 0;
        } else if (pid_f1 == -1) {
            cerr << "Multiprocessing failed.";
            return 1;
        }
        //parent process
        pid_t pid_f2 = fork();
        if (pid_f2 == 0) {
            //child 2 process
            cout << "2 init" << "\n";
            int f2[num_iterations];
            for (int i2 = 0; i2 <= num_iterations; i2++) {
                f2[i2] = formula2(x[i2]);
                write(pipe_from_f2[1], &f2[i2], sizeof(f2[i2]));
                write(pipe_step_2[1],&i2,sizeof(num_iterations));
                //cout << "p2" << i2 << endl;
            }
            close(pipe_from_f2[1]);
            close(pipe_step_2[1]);
            cout << "end of 2" << endl;
            return 0;
        } else if (pid_f2 == -1) {
            cerr << "Multiprocessing failed.";
            return 1;
        }
        //parent process
        int p1_step = -1;
        int p2_step = -1;
        int from_f1[num_iterations], from_f2[num_iterations];
        int f3[num_iterations];
        read(pipe_from_f1[0], &from_f1, sizeof(from_f1));
        read(pipe_from_f2[0], &from_f2, sizeof(from_f2));
        for(int n=0;n<=num_iterations;n++){
            //cout << "p1" << p1_step << " p2" << p2_step << endl;
            read(pipe_step_1[0],&p1_step,sizeof(num_iterations));
            read(pipe_step_2[0],&p2_step,sizeof(num_iterations));
            if(p1_step<=n && p2_step<=n){
                //cout << "p1o" << from_f1[n] << endl;
                //cout << "p2o" << from_f2[n] << endl;
                f3[n] = formula3(from_f1[n], from_f2[n]);
                cout << n << ":"<<f3[n] << endl;
            }else{
                usleep(500);
            }
        }
        //end of the main evaluation
        clock_t end = clock();
        auto seconds = ((double) (end - start)) / CLOCKS_PER_SEC;
        cout << "Time spent for " << num_iterations << " calculations is " << seconds << " seconds" << "\n";
        num_iterations *= 10;
    }
    return 0;
}