#include <iostream>
#include <cmath>
using namespace std;

long double rekurzija (long double b, long double c,int n, long double a0, long double a1){
    if (n==0){
        return a0;
    }
    if (n==1){
        return a1;
    }
    return b * rekurzija(b,c,n-1,a0,a1) + c * rekurzija(b,c,n-2,a0,a1);
}
long double opcaFormula(long double  b,long double c,long double a0,long double a1,int n){
    long double x1,x2,λ1,λ2;

    x1 = (b - sqrtl(powl(b,2) + 4*c))/2;
    x2 = (b + sqrtl(powl(b,2) + 4*c))/2;
   
    if (x1 != x2){
        
        λ2 = ((a1 - a0 * x1))/(x2 - x1);
        λ1 = a0 - λ2;
    
        
        return λ1 * powl(x1,n) + λ2 * powl(x2,n);
    }

    λ1 = a0;
    λ2 = (a1-λ1*x1)/x2;

    return λ1 * powl(x1,n) + λ2 * n * powl(x2,n);


}

int main(){
    long double b,c,a0,a1,n;
    
    cout << "Unesite prvi koeficijent λ_1 rekurzivne relacije: " << endl;
    cin >> b;
    cout << "Unesite drugo koeficijent λ_2 rekurzivne relacije: " << endl;
    cin >> c;
    cout << "Unesite vrijednost nultog clana niza a_0: " << endl;
    cin >> a0;
    cout << "Unesite vrijednost nultog clana niza a_1: " << endl;
    cin >> a1;
    cout << "Unesite redni broj n trazenog clana niza: " << endl;
    cin >> n;
    
    cout << "Vrijednost n-tog clana niza pomocu formule: " << opcaFormula(b, c, a0, a1, n) << endl;
    cout << "Vrijednost n-tog clana niza iz rekurzije: " << rekurzija(b, c, n, a0, a1) << endl;
    cout << "Vrijednost (n-1)-clana niza pomocu formule: " << opcaFormula(b, c, a0, a1, n-1) << endl;
    string odnos;
    if (opcaFormula(b,c,a0,a1,n) > opcaFormula(b,c,a0,a1,n-1)){
        odnos = "veci";
    }
    if (opcaFormula(b,c,a0,a1,n) < opcaFormula(b,c,a0,a1,n-1)){
        odnos = "manji";
    }else{
        odnos = "jednak";
    }
    cout << "N-ti clan niza je " << odnos<< " od n-1 clana." << endl;
  


}