#include "kinetics/molecule.hpp"

#include <fstream>
#include <iostream>
#include <stdexcept>

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: kinetics-molecule-inspect INPUT.pdb OUTPUT.json\n";
        return 2;
    }
    try {
        kinetics::MolecularScene scene(kinetics::load_pdb(argv[1]));
        std::ofstream output(argv[2], std::ios::binary);
        if (!output) throw std::runtime_error("cannot create JSON output");
        output << kinetics::scene_to_json(scene) << '\n';
        if (!output) throw std::runtime_error("failed writing JSON output");
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "kinetics-molecule-inspect: " << error.what() << '\n';
        return 1;
    }
}
