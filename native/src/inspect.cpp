#include "kinetics/molecule.hpp"

#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

int main(int argc, char** argv) {
    try {
        if (argc == 4 && std::string(argv[1]) == "render-xy") {
            kinetics::MolecularScene scene(kinetics::load_pdb(argv[2]));
            std::ofstream output(argv[3], std::ios::binary);
            if (!output) throw std::runtime_error("cannot create PPM output");
            output << kinetics::render_xy_ppm(scene);
            if (!output) throw std::runtime_error("failed writing PPM output");
            return 0;
        }
        if (argc == 3) {
            kinetics::MolecularScene scene(kinetics::load_pdb(argv[1]));
            std::ofstream output(argv[2], std::ios::binary);
            if (!output) throw std::runtime_error("cannot create JSON output");
            output << kinetics::scene_to_json(scene) << '\n';
            if (!output) throw std::runtime_error("failed writing JSON output");
            return 0;
        }
        std::cerr << "usage: kinetics-molecule-inspect INPUT.pdb OUTPUT.json\n"
                  << "   or: kinetics-molecule-inspect render-xy INPUT.pdb OUTPUT.ppm\n";
        return 2;
    } catch (const std::exception& error) {
        std::cerr << "kinetics-molecule-inspect: " << error.what() << '\n';
        return 1;
    }
}
