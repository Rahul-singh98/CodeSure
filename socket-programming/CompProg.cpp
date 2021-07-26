#include<iostream>
#include<bits/stdc++.h>
using namespace std;

int main(void){
    int t ;cin >> t;
    while (t--){
        string str ;
        getline(cin , str);
        
        map<char , int> firstHalf , secondHalf;
        for(int i =0 ; i<str.length() ; i++){
            
            if (i < str.length() / 2 ){
                if (firstHalf.find(str.c_str()[i]))
                    firstHalf[str.c_str()[i]] += 1;
                else 
                    firstHalf[str.c_str()[i]] = 1;
            }
            else if(str.length()%2 == 0){
                if (secondHalf.find(str.c_str()[i]))
                    secondHalf[str.c_str()[i]] += 1;
                else 
                    secondHalf[str.c_str()[i]]=1;
            }
            else{
                if(i>str.length()/2){
                        if (secondHalf.find(str.c_str()[i]))
                    secondHalf[str.c_str()[i]] += 1;
                else 
                    secondHalf[str.c_str()[i]]=1;
                }
            }
            
        }
        
        if (firstHalf == secondHalf)
            cout << "YES" << endl;
        else 
            cout << "NO" << endl;
        
        
    }
    return 0;
}