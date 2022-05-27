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
int inWorkVar = 0; //generated random number
int *workOutVar; //variable for synchronisation of work and out threads
int numberOfIterations;
int Id;


void *workThread (void *x){ //work thread
    printf("Pokrenuta RADNA DRETVA\n");
    for (int i = 0; i < numberOfIterations; i++){
        while(inWorkVar == 0); //waiting for IN thread
        *workOutVar = inWorkVar + 1; 
        printf("RADNA DRETVA: procitan broj %d i povecan na %d\n", inWorkVar, *workOutVar);
        inWorkVar = 0;
        while (*workOutVar!=0); //waiting for OUT thread
    }
    printf("Zavrsila RADNA DRETVA\n");
} 
void outThread(void){
    printf("Pokrenut IZLAZNI PROCES\n");
    for (int i = 0; i < numberOfIterations; i++){
        while (*workOutVar == 0); //wait for WORK thread
        FILE *f = fopen("rezultat.txt","a");
        fprintf(f, "%d\n", *workOutVar);
        printf("IZLAZNI PROCES: broj upisan u datoteku %d\n", *workOutVar);
        *workOutVar = 0;
        fclose(f);
    }
    printf("Zavrsio IZLAZNI PROCES\n");
}
void delete (int sig){
    //free shared memory space
    shmdt((char * ) workOutVar);
    shmctl(Id, IPC_RMID, NULL);
    exit(0);
}
void maskSignal(){
     //masking interrupt signal
    struct sigaction act;
    act.sa_handler = delete;
    sigemptyset(&act.sa_mask);
    act.sa_flags = 0; 
    sigaction(SIGINT, &act, NULL);
}
int main(int argc, char *argv[]){

    if (argc!=2){
        printf("Krivo pokretanje programa!\n");
        exit(1);
    }else{
        numberOfIterations = atoi(argv[1]);
    } 
    Id = shmget(IPC_PRIVATE, sizeof(int), 0600);
    if (Id == -1){
        printf("Nemoguce zauzimanje memorije!\n");
        exit(1); 
    }

    workOutVar = (int *) shmat(Id, NULL, 0); //workOutVar for synchronising OUT and WORK threads
    *workOutVar = 0;
    
    maskSignal();
    switch(fork()){
    case 0:
        //child, OUT thread
        outThread();
        exit(0);
    case -1:
        printf("Greska, nemoguce stvoriti proces");
    default:
        //IN thread (parent)
        srand(time(0));
        pthread_t thread_id;
        if (pthread_create(&thread_id, NULL, workThread, NULL)!=0){
            printf("Greska pri stvaranju dretve.\n");
            exit(1);
        }
        printf("Pokrenuta ULAZNA DRETVA\n");
        for (int i = 0;i < numberOfIterations; i++){
            while(inWorkVar!=0);
            inWorkVar = (rand() % 100) + 1; //the generated number, also used for synchronisation between IN and WORK threads
            printf("ULAZNA DRETVA: broj %d\n", inWorkVar);
            sleep(5);
            
        }

        pthread_join(thread_id, NULL);
        printf("Zavrsila ULAZNA DRETVA\n");
    }
    wait(NULL);
    delete(0);
}