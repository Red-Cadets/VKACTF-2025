#include <iostream>
#include <fstream>
#include <set>
#include <string>
#include <cryptopp/osrng.h>
#include <cryptopp/integer.h>
#include <cryptopp/nbtheory.h>

using namespace CryptoPP;
using namespace std;

Integer NextPrime(const Integer& n) {
    Integer p = n;
    if (p % 2 == 0) p++;
    
    while (!IsPrime(p)) {
        p += 2;
    }
    return p;
}

Integer Tonnelli_Shanks(const Integer& a, const Integer& p) {
    if (Jacobi(a, p) != 1) return 0;
    if (a == 0) return 0;
    if (p == 2) return 0;
    
    if (p % 4 == 3) {
        return a_exp_b_mod_c(a, (p + 1) / 4, p);
    }
    
    Integer s = p - 1;
    int e = 0;
    while (s % 2 == 0) {
        s /= 2;
        e++;
    }
    
    Integer n = 2;
    while (Jacobi(n, p) != -1) {
        n++;
    }
    
    Integer x = a_exp_b_mod_c(a, (s + 1) / 2, p);
    Integer b = a_exp_b_mod_c(a, s, p);
    Integer g = a_exp_b_mod_c(n, s, p);
    int r = e;
    
    while (true) {
        Integer t = b;
        int m = 0;
        for (; m < r; m++) {
            if (t == 1) break;
            t = a_exp_b_mod_c(t, 2, p);
        }
        if (m == 0) return x;
        
        Integer gs = a_exp_b_mod_c(g, Integer::Power2(r - m - 1), p);
        g = (gs * gs) % p;
        x = (x * gs) % p;
        b = (b * g) % p;
        r = m;
    }
}

class EllipticCurve {
public:
    Integer p, a, b;
    
    EllipticCurve(const Integer& p, const Integer& a, const Integer& b) 
        : p(p), a(a), b(b) {
        if (!check_curve()) {
            throw runtime_error("Заяц – Гусь! Кривая - Некривая!");
        }
    }
    
    bool check_curve() const {
        Integer d = -16 * (4*a*a*a + 27*b*b);
        return (d % p) != 0;
    }
    
    Integer lift_x(const Integer& px) const {
        Integer y2 = (a_exp_b_mod_c(px, 3, p) + a*px + b) % p;
        Integer py = Tonnelli_Shanks(y2, p);
        if (py == 0) {
            throw runtime_error("Точка не пренадлежит кривой!");
        }
        return py;
    }
};

int main() {
    AutoSeededRandomPool prng;
    
    ifstream flag_file("flag.txt", ios::binary);
    if (!flag_file) {
        cerr << "Флю… флю… флюгегехайм… Стоп-слово! Стоп-слово!" << endl;
        return 1;
    }
    
    string flag_str((istreambuf_iterator<char>(flag_file)), istreambuf_iterator<char>());
    Integer flag(reinterpret_cast<const byte*>(flag_str.data()), flag_str.size());
    
    cout <<""<< endl;
    cout << "Я гусь! Я до тебя (додолблюсь!)" << endl;
    cout <<""<< endl;
    
    Integer p, a, b, fy;
    while (true) {
        p = Integer(prng, 762);  // Семьсот шестьдесят два... Семь сотен. Шесть десятков. И два.
        p = NextPrime(p);
        a = Integer(prng, 512);
        b = Integer(prng, 512);
        
        try {
            EllipticCurve E(p, a, b);
            fy = E.lift_x(flag);
            cout << "p = " << p << endl;
            cout << "Истинный y = " << fy << endl;
            break;
        } catch (...) {
            continue;
        }
    }
    
    set<Integer> checked;
    int count = 0;
    
    while (count < 3826) {       
        Integer x(prng, 2, p-1);
        
        if (checked.count(x) || x < Integer::Power2(512) || 
            (x > p ? x - p : p - x) < Integer::Power2(512)) {  
            cout << "Ломай меня полностью!" << endl;
            continue;
        }
        
        try {
            Integer e(prng, 55);
            cout << "e = " << e << endl;
            
            EllipticCurve E(p, a^e, b^e);
            Integer py = E.lift_x(x);
            
            checked.insert(x);
            cout << "x = " << x << endl;
            cout << "y = " << py << endl;
            count++;
        } catch (...) {
            cout << "Жгучие пироги! Кто ж думал-то, что вот так подряд техника будет сбоить?" << endl;
        }
        
        cout << "Продолжаем > ";
        string more;
        getline(cin, more);
        if (more == "Stop") {
            break;
        }
    }
    
    cout << "Я гусь! Я, пожалуй, (убегусь!)" << endl;
    return 0;
}
