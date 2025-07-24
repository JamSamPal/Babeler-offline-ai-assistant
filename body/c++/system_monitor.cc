#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

float get_cpu_temp() {
    std::ifstream file("/sys/class/thermal/thermal_zone0/temp");
    float temp = 0.0;

    if (file.is_open()) {
        int millidegrees;
        file >> millidegrees;
        file.close();
        temp = millidegrees / 1000.0; // Convert to °C
    } else {
        std::cerr << "Could not read CPU temperature." << std::endl;
    }

    return temp;
}

void get_memory_info(long &mem_total, long &mem_available) {
    std::ifstream file("/proc/meminfo");
    std::string line;
    mem_total = 0;
    mem_available = 0;

    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string key;
        long value;
        std::string unit;
        if (iss >> key >> value >> unit) {
            if (key == "MemTotal:")
                mem_total = value;
            if (key == "MemAvailable:")
                mem_available = value;
            if (mem_total && mem_available)
                break;
        }
    }
}

int main(int argc, char *argv[]) {
    std::cout << std::fixed << std::setprecision(2);

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " [temp|memory]" << std::endl;
        return 1;
    }

    std::string arg = argv[1];

    if (arg == "temp") {
        float temp = get_cpu_temp();
        std::cout << temp << std::endl;

    } else if (arg == "memory") {
        long mem_total = 0, mem_available = 0;
        get_memory_info(mem_total, mem_available);
        float mem_used = mem_total - mem_available;
        float mem_used_percent = mem_total ? (mem_used / mem_total) * 100.0 : 0;

        std::cout << "memory use is " << mem_used_percent << " percent" << std::endl;
    } else {
        std::cout << "invalid argument";
    }
}