#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/msg.h>
#include <sys/wait.h>
#include <values.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <semaphore.h>

int m; //Broj posjetitelja
int n; //Broj sjedala na vrtuljku
int IDss;
int IDs;
int IDk;
int IDu;
sem_t *semSjedi;
sem_t *semKreni;
sem_t *semUstani;
sem_t *sviSisli;
void posjetitelj(){
    sem_wait(semSjedi);
    printf("Posjetitelj je sjeo na vrtuljak\n");
    sem_post(semKreni);
    sem_wait(semUstani);
    sem_post(sviSisli);
    printf("Posjetitelj je sišao s vrtuljka\n");
}
void vrtuljak(int n){
    for(int i = 0; i <n; i++){
        sem_wait(sviSisli);
    }
    for (int i = 0; i < n; i++){
        sem_post(semSjedi);
    }
    for (int i = 0; i < n; i++){
        sem_wait(semKreni);
    }
    printf("Vrtuljak kreće!\n");
    sleep(2);
    printf("Vrtuljak završio.\n");
    for (int i = 0; i < n; i++){
        sem_post(semUstani);
    }
    
    
}
void exitAndDelete (int sig){
    for(int i = 0; i < m; i++){
        wait(NULL);
    }
    //free shared memory space
    shmdt((char * ) semSjedi);
    shmctl(IDs, IPC_RMID, NULL);

    shmdt((char * ) semKreni);
    shmctl(IDk, IPC_RMID, NULL);

    shmdt((char * ) semUstani);
    shmctl(IDu, IPC_RMID, NULL);

    shmdt((char * ) sviSisli);
    shmctl(IDss, IPC_RMID, NULL);
    exit(0);
}

void maskSignal(){
     //masking interrupt signal
    struct sigaction act;
    act.sa_handler = exitAndDelete;
    sigemptyset(&act.sa_mask);
    act.sa_flags = 0; 
    sigaction(SIGINT, &act, NULL);
}
int main(int argc, char *argv[]){
    
    if (argc!=3){
        printf("Krivo pokretanje programa!\n");
        exit(1);
    }else{
        m = atoi(argv[2]);
        n = atoi(argv[1]);
    } 
    IDs = shmget(IPC_PRIVATE, sizeof(sem_t), 0600);
    semSjedi = shmat(IDs, NULL, 0);
    sem_init(semSjedi, 1, 0);

    IDk = shmget(IPC_PRIVATE, sizeof(sem_t), 0600);
    semKreni = shmat(IDk, NULL, 0);
    sem_init(semKreni, 1, 0);

    IDu = shmget(IPC_PRIVATE, sizeof(sem_t), 0600);
    semUstani = shmat(IDu, NULL, 0);
    sem_init(semUstani, 1, 0);

    IDss = shmget(IPC_PRIVATE, sizeof(sem_t), 0600);
    sviSisli = shmat(IDss, NULL, 0);
    sem_init(sviSisli, 1, n);

    maskSignal();
    for (int i = 0; i < m; i++){
        if (fork()==0){
            posjetitelj();
            exit(0);
        }
    }

    while(1){
        vrtuljak(n);
    }
    /* for (int i = 0; i < (m/n); i++){
        vrtuljak(n);
    }

    for(int i = 0; i < m; i++){
        wait(NULL);
    }

    exitAndDelete(0); */


}


