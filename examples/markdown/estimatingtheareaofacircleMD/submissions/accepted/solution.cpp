#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>

using namespace std;

int main() {
    double r;
    size_t n, c;

    while (cin >> r >> n >> c) {
        if (r == 0.0 && n == 0 && c == 0) { break; }
        double truth = M_PI * r * r;
        double est = c * 4.0 * r * r / n;
        cout << setprecision(10) << truth << " " << est << endl;
    }
    return 0;
}
