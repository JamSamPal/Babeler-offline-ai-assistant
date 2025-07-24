#include <cstdlib>
#include <iostream>
#include <string>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: ./tts_speaker \"Text to speak\"\n";
        return 1;
    }

    std::string text = argv[1];

    // Wrap the command
    std::string cmd = "espeak \"" + text + "\" --stdout | paplay";

    int result = std::system(cmd.c_str());

    if (result != 0) {
        std::cerr << "Failed to run TTS command\n";
        return 1;
    }

    return 0;
}