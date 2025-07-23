#include <fstream>
#include <iostream>
#include <string>

float getCPUTemperature() {

    int temp_milli = 1000;
    return temp_milli / 1000.0f; // Convert millidegree to degree
}

int main() {
    float temp = getCPUTemperature();
    if (temp >= 0) {
        std::cout << temp << std::endl;
        return 0;
    } else {
        return 1;
    }
}