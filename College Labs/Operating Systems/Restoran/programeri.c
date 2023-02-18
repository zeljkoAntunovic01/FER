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
int br[2]; //polje "Unutra"
int ceka[2];
int posluzeno[2];
int vrstaLinux = 0;
int vrstaMS = 1;
int brLinux;
int brMS;
int propustljivost; //koliko mogu tih istih pustit unutra ako cekaju ovi drugi
pthread_mutex_t m;
pthread_cond_t redLinux;
pthread_cond_t redMS;
void udji(int vrsta){
    pthread_mutex_lock(&m);
    while (br[1-vrsta] > 0 || (ceka[1-vrsta] > 0 && posluzeno[vrsta] >= propustljivost)){
        ceka[vrsta]++;
        if (vrsta==0){
            pthread_cond_wait(&redLinux, &m);
        }else{
            pthread_cond_wait(&redMS, &m);
        }
        ceka[vrsta]--;
    }
    br[vrsta]++;
    posluzeno[1-vrsta] = 0;
    if (ceka[1-vrsta] > 0){
        posluzeno[vrsta]++; 
    }
    pthread_mutex_unlock(&m);
}
void izadji(int vrsta){
    pthread_mutex_lock(&m);
    br[vrsta]--;
    if (br[vrsta] == 0){
        if (vrsta==0){
            pthread_cond_broadcast(&redMS);
        }else{
            pthread_cond_broadcast(&redLinux);
        }
    }
    pthread_mutex_unlock(&m);
}
void *programer(void *vrstaAddr){
    int vrsta = *((int*)vrstaAddr);
    udji(vrsta);
    printf("Programer %d je ušao i sjeo za stol.\n", vrsta);
    sleep(rand()%5 + 1);
    izadji(vrsta);
    printf("Programer % d je izašao iz restorana.\n", vrsta);
}
int main(int argc, char *argv[]){
    if (argc!=4){
        printf("Krivo pokretanje programa!\n");
        exit(1);
    }else{
        brLinux = atoi(argv[1]);
        brMS = atoi(argv[2]);
        propustljivost = atoi(argv[3]);
    } 

    
    pthread_mutex_init(&m, NULL);
    pthread_cond_init(&redLinux,NULL);
    pthread_cond_init(&redMS, NULL);


    pthread_t thread_id[brLinux + brMS];
    int i, uvjet;
    int brl = 0;
    int brm = 0;
    uvjet = 1;
    /* for (i = 0 ; i < brMS; i++){
        pthread_create(&thread_id[i],NULL,(void *)programer, &vrstaMS);
    }
    for (; i < brMS + brLinux; i++){
        pthread_create(&thread_id[i],NULL,(void *)programer, &vrstaLinux);
    } */
    for (i = 0; i < brMS + brLinux; i++){

        if (rand()%2){
            pthread_create(&thread_id[i],NULL,(void *)programer, &vrstaMS);
        }
        else{
            pthread_create(&thread_id[i],NULL,(void *)programer, &vrstaLinux);

        }
        sleep(rand()%3 + 1);
    }
    /* for (i = 0; i < brMS + brLinux; i++){
        if (uvjet == 1 && brl < brLinux){
            pthread_create(&thread_id[i],NULL,(void *)programer, &vrstaLinux);
            uvjet = 0;
            brl++;
            continue;
        }
        if  (uvjet == 0 && brm < brMS){
            pthread_create(&thread_id[i],NULL,(void *)programer, &vrstaMS);
            uvjet = 1;
            brm++;
        }
        
    } */
    for (int i = 0; i < brLinux + brMS; i++){
        pthread_join(thread_id[i],NULL);
    }
    return 0;

}