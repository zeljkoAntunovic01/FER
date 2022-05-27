#include <iostream>
#include <math.h>
#include <vector>
#include <fstream>
using namespace std;

bool isValid (int c, vector<int>& colors, int v,int n, vector<int>& S,int size){
    for (int i = 1; i <=n; i++){
        int diff = abs(i-v);
        bool condition;
        for (int j = 0; j < size; j++){
            if (diff==S[j]){
                condition = true;
            }
        }
        if (condition){
            if (colors[i-1] == c){
                return false;
            }
        }
        condition = false;
    }
    return true;
}

bool graphColoringWithM(int m, vector<int>& colors, int n, int v, vector<int> S,int size){
    if (v== n+1){
        return true;
    }
    for (int c = 1; c <= m; c++){
        if (isValid(c, colors, v,n, S,size)){
            colors[v-1] = c;
            if (graphColoringWithM(m,colors,n,v+1,S,size)){
                return true;
            }
            colors[v-1] = 0;
            
        }
    }
    return false;
}

int chromaticNumber(int n, vector<int> S,int size){
    vector<int> colors(n,0);
    int chrNumber = 1;
    while (true){
        if (graphColoringWithM(chrNumber,colors,n,1, S,size)){
            
            return chrNumber;
        }
        chrNumber++;
    }


}

int main(){
    string file;

    cout << "Molimo upisite naziv datoteke: ";
    cin >> file;
    ifstream datoteka(file);

    int n,size;
    datoteka >> n >> size;
    vector<int> S(size);
    int input;
    for (int i = 0; i < size; i++){
        datoteka >> input;
        S[i] = input;
    }
    datoteka.close();

    int cN;
    cN = chromaticNumber(n,S,size);
    cout << "Kromatski broj = " << cN << endl;






    
    //matrica susjedstva
    /*int i,j,k;
    bool matricaSusjedstva[n][n] = {};
    
    for (i = 1; i <= n; i++){
        for (j = 1; j <= n; j++){
            matricaSusjedstva[i][j] = false;
        }
        cout << endl;

    }
    
    for (i = 1; i <= n; i++){
        for (j = 1; j <= n; j++){
            int diff = abs(i-j);
            bool adj;
            for (k = 0; k < size; k++){
                if (S[k] == diff){
                    adj = true;
                }
            }
            if (adj){
                matricaSusjedstva[i][j] = true;
            }
            adj = false;

        }
    }
    for (i = 1; i <= n; i++){
        for (j = 1; j <= n; j++){
            cout << matricaSusjedstva[i][j] << " ";
        }
        cout << endl;

    }
    
    */


  
    
    return 0;
}