#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <math.h>
/* funkcije za obradu signala, navedene ispod main-a */
void obradi_dogadjaj(int sig);
void obradi_sigterm(int sig);
/*globalne varijable*/
int broj;
FILE *status;
FILE *obrada;

int main()
{
    struct sigaction act;
    /*maskiranje signala SIGUSR1 */
    act.sa_handler = obradi_dogadjaj;
    act.sa_flags = 0; 
    sigaction(SIGUSR1, &act, NULL); 
    /*maskiranje signala SIGTERM*/
    act.sa_handler = obradi_sigterm;
    sigaction(SIGTERM, &act, NULL);


    int x; // x = obrada(broj)
    obrada = fopen("obrada.txt","a+"); 
    status = fopen("status.txt","r+"); 
    fscanf(status,"%d",&broj); //procitaj trenutni broj na kojem smo stali
    fclose(status);
    if (broj==0){ //ako je broj == 0, iz Obrada izracunaj koji broj je bio zadnji
        char zadnjiBroj[1024];
        fseek(obrada, 0, SEEK_SET);
        while (!feof(obrada))
        { //procitaj zadnju liniju datoteke i spremi u zadnjiBroj
            memset(zadnjiBroj, 0x00, 1024); 
            fscanf(obrada, "%[^\n]\n", zadnjiBroj);
        }
        broj = sqrt(atoi(zadnjiBroj)); //pretvori zadnju liniju u int
    }
    fclose(obrada);
    status = fopen("status.txt","w"); 
    fprintf(status,"%d",0); //tijekom izvodenja programa u Status upisi 0
    fclose(status);

    printf("Program s PID=%ld krenuo s radom\n", (long) getpid());
    while (1)
    { //beskonacno radi posao
        broj++;
        x = broj * broj;
        obrada = fopen("obrada.txt","a"); 
        fprintf(obrada,"\n%d",x); //upisi kvadrat od "broj" u Obrada
        fclose(obrada);
        sleep(5);
    }
    return 0;
}
void obradi_dogadjaj (int sig)
{
    printf("Trenutni broj: %d\n", broj); //ispisi trenutni broj
}
void obradi_sigterm (int sig)
{
    status = fopen("status.txt","w");
    fprintf(status,"%d",broj); //zapisi zadnji broj u Status
    fclose(status);
    exit(1);
}
