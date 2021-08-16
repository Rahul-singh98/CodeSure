#include<bits/stdc++.h>
#define ll long long int
using namespace std;

bool cmp(pair<ll , pair<ll ,ll>>& a , pair<ll , pair<ll,ll>>& b){
    return a.second.first < b.second.first;
}

int main(){
    int t;cin >> t;
    while (t--){
        ll n ,l=0 , count =0;cin >> n;
        vector<ll> a , b ;
        vector<pair<ll , pair<ll ,ll>>> mp , mp2;
        for(ll i =0;i<n;i++){
            ll x; cin >> x;
            a.push_back(x);
        }

        for(ll i =0;i<n;i++){
            ll x; cin >> x;
            b.push_back(x);
        }

        for(int i =0;i<n;i++){
            if (a[i]<=b[i]){
                mp.push_back(make_pair(i+1,make_pair(a[i] , b[i])));
            }
        }

        sort(mp.begin() , mp.end() , cmp);

        for (auto i:mp){
            if ((l + i.second.first) <= i.second.second){
                mp2.push_back(make_pair(i.first , make_pair(l , l+i.second.first)));
                l += i.second.first;
                count++;
            }
        }

        cout << count <<"\n";
        for (auto i:mp2)
            cout << i.first << " " << i.second.first << " " << i.second.second << '\n';

    }
    return 0;
}