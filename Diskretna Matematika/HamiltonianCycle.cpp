#include <iostream>
#include <math.h>
#include <bits/stdc++.h>
using namespace std;



int pohlepni(int (&parametri)[3]){
    int lijeviVrh, desniVrh,i,j;
    int duljinaCiklusa = 0;
    int trenutniBrid;
    int pocetniBrid = INT_MAX;  //arbitrarni broj koji ce sigurno biti veci od svakog brida
    int max = pocetniBrid;
    for (i = 1; i<=parametri[0]; i++){ //trazimo pocetni brid
        for (j = 1; j<=parametri[0]; j++){
            if (i>j){
                trenutniBrid =(parametri[1]*j+ parametri[2]*i)*(parametri[1]*j+ parametri[2]*i) + 1;
                if (trenutniBrid <= pocetniBrid){
                    pocetniBrid = trenutniBrid;
                    lijeviVrh = i;
                    desniVrh = j;
                }
            }
            if(j>i){                   
                trenutniBrid = (parametri[1]*i+ parametri[2]*j)*(parametri[1]*i+ parametri[2]*j) + 1;
                if (trenutniBrid <= pocetniBrid){
                    pocetniBrid = trenutniBrid;
                    lijeviVrh = j;
                    desniVrh = i;
                }
            }  
        }
    }
    duljinaCiklusa+=pocetniBrid;
    
    
    bool iskoristeniVrhovi[parametri[0]]{};
    iskoristeniVrhovi[desniVrh-1] = true;
    iskoristeniVrhovi[lijeviVrh-1] = true;
    
    int uvjet,sljedeciLijevi,sljedeciDesni,najmanjiDesniBrid,najmanjiLijeviBrid,najmanjiBrid;
    do{
        uvjet = 0;
        for (bool b : iskoristeniVrhovi){
            if (b==true){
                uvjet++;
            }
        }
        if (uvjet<parametri[0]){
            
            sljedeciLijevi = lijeviVrh;
            sljedeciDesni = desniVrh;
            najmanjiDesniBrid = max;
            najmanjiLijeviBrid = max;
            for (i = 1; i<=parametri[0]; i++){   //trazimo najmanji brid s lijeve strane
                if ( (lijeviVrh > i) && (iskoristeniVrhovi[i-1]==false)){
                    trenutniBrid = (parametri[1]*i+ parametri[2]*lijeviVrh)*(parametri[1]*i+ parametri[2]*lijeviVrh) + 1;
                    if (trenutniBrid <= najmanjiLijeviBrid){
                        najmanjiLijeviBrid = trenutniBrid;
                        sljedeciLijevi = i;
                    }
                }
                if ( (lijeviVrh < i) && (iskoristeniVrhovi[i-1]==false) ){
                    trenutniBrid = (parametri[1]*lijeviVrh+ parametri[2]*i)*(parametri[1]*lijeviVrh+ parametri[2]*i) + 1;
                    if (trenutniBrid <= najmanjiLijeviBrid){
                        najmanjiLijeviBrid = trenutniBrid;
                        sljedeciLijevi = i;
                    }
                }
            }
            for (i = 1; i<=parametri[0]; i++){ //trazimo najmanji brid s desne strane
                if ( (desniVrh > i) && (iskoristeniVrhovi[i-1]==false)){
                    trenutniBrid = (parametri[1]*i+ parametri[2]*desniVrh)*(parametri[1]*i+ parametri[2]*desniVrh) + 1;
                    if (trenutniBrid <= najmanjiDesniBrid){
                        najmanjiDesniBrid = trenutniBrid;
                        sljedeciDesni = i;
                    }
                }
                if ( (desniVrh < i) && (iskoristeniVrhovi[i-1]==false) ){
                    trenutniBrid = (parametri[1]*desniVrh+ parametri[2]*i)*(parametri[1]*desniVrh+ parametri[2]*i) + 1;
                    if (trenutniBrid <= najmanjiDesniBrid){
                        najmanjiDesniBrid = trenutniBrid;
                        sljedeciDesni = i;
                    }
                }
            }
            if (najmanjiDesniBrid<=najmanjiLijeviBrid){
                duljinaCiklusa+=najmanjiDesniBrid;
                desniVrh = sljedeciDesni;
                iskoristeniVrhovi[desniVrh-1] = true;    
            }else{
                duljinaCiklusa+=najmanjiLijeviBrid;
                lijeviVrh = sljedeciLijevi;
                iskoristeniVrhovi[lijeviVrh-1] = true;      
            }
            
        }else{
            
            if (lijeviVrh > desniVrh){
                    duljinaCiklusa = duljinaCiklusa + (parametri[1]*desniVrh + parametri[2]*lijeviVrh)*(parametri[1]*desniVrh + parametri[2]*lijeviVrh) + 1;
                   
                }
            if (desniVrh > lijeviVrh){
                    duljinaCiklusa = duljinaCiklusa +(parametri[1]*lijeviVrh + parametri[2]*desniVrh)*(parametri[1]*lijeviVrh + parametri[2]*desniVrh) + 1;
                    
                    
            }
            
            
        }
    }while (uvjet<parametri[0]);
    
    return duljinaCiklusa;
}   
int iscrpni(int (&parametri)[3]){
    vector<int> permutacije(parametri[0]-1);
    for (int i = 0; i <parametri[0]-1; i++){
        permutacije[i] = i + 2;
    }
    int prviVrh = 1;
    int trenutniCiklus = 0;
    int najmanjiCiklus = 0;
    int i;
    for (i = 0; i < parametri[0]-2;i++){
        najmanjiCiklus += (parametri[1]*permutacije[i] + parametri[2]*permutacije[i+1])*(parametri[1]*permutacije[i] + parametri[2]*permutacije[i+1]) + 1;
    }
    
    najmanjiCiklus += (parametri[1]*1 + parametri[2]*permutacije[i])*(parametri[1]*1 + parametri[2]*permutacije[i]) + (parametri[1]*1 + parametri[2]*permutacije[0])*(parametri[1]*1 + parametri[2]*permutacije[0]) + 2;


    while(next_permutation(permutacije.begin(),permutacije.end())){
        trenutniCiklus = 0;
        
        for (i = 0; i < parametri[0]-2;i++){
            if (permutacije[i] < permutacije[i+1]){
                trenutniCiklus += (parametri[1]*permutacije[i] + parametri[2]*permutacije[i+1])*(parametri[1]*permutacije[i] + parametri[2]*permutacije[i+1]) + 1;
            }else{
                trenutniCiklus += (parametri[1]*permutacije[i+1] + parametri[2]*permutacije[i])*(parametri[1]*permutacije[i+1] + parametri[2]*permutacije[i]) + 1;
            }
            
        }
        
        trenutniCiklus += (parametri[1]*1 + parametri[2]*permutacije[i])*(parametri[1]*1 + parametri[2]*permutacije[i]) + (parametri[1]*1 + parametri[2]*permutacije[0])*(parametri[1]*1 + parametri[2]*permutacije[0]) + 2;
        
        if (trenutniCiklus <= najmanjiCiklus){
            najmanjiCiklus = trenutniCiklus;
        }
    }
    return najmanjiCiklus;
}
int main(){
    cout << "Unesite redom, odvojene razmakom, parametre n, a i b: ";
    int parametri[3];
    for (int i = 0; i < 3; i++){
        cin >> parametri[i];
    }
    int p = pohlepni(parametri);
    int i = iscrpni(parametri);
    cout << endl;
    cout << "Pohlepni algoritam nalazi ciklus duljine "<< p<< endl;
    cout << "Iscrpni algoritam nalazi ciklus duljine " << i << endl;
    if (p == i ){
        cout << "Pohlepni algoritam na ovom grafu daje optimalno rjesenje!";
    }else{
        cout <<"Pohlepni algoritam na ovom grafu ne daje optimalno rjesenje!";
    }

    return 0;
}