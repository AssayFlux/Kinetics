#include "kinetics/molecule.hpp"

#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

#ifndef KINETICS_FIXTURE_DIR
#error KINETICS_FIXTURE_DIR must be defined
#endif

int main() {
    try {
        const auto structure = kinetics::load_pdb(
            std::string(KINETICS_FIXTURE_DIR) + "/reference.pdb");
        if (structure.atoms.size() != 2) throw std::runtime_error("atom count mismatch");
        if (structure.bonds.size() != 1) throw std::runtime_error("CONECT bond count mismatch");
        if (structure.atoms[0].serial != 1 || structure.atoms[1].serial != 2)
            throw std::runtime_error("atom serial identity changed");
        if (structure.atoms[0].element != "C" || structure.atoms[1].element != "O")
            throw std::runtime_error("element identity changed");
        if (std::abs(structure.atoms[1].position[0] - 1.25) > 1e-12)
            throw std::runtime_error("coordinate parsing mismatch");
        if (std::abs(kinetics::distance_angstrom(structure.atoms[0], structure.atoms[1]) - 1.25) > 1e-12)
            throw std::runtime_error("reference distance mismatch");

        kinetics::MolecularScene scene(structure);
        scene.set_selection({1});
        scene.set_highlights({2});
        const auto json = kinetics::scene_to_json(scene);
        if (json.find("\"coordinate_unit\":\"angstrom\"") == std::string::npos)
            throw std::runtime_error("coordinate unit missing from scene contract");
        if (json.find("\"selection\":[1]") == std::string::npos)
            throw std::runtime_error("selection missing from scene contract");
        if (json.find("\"highlights\":[2]") == std::string::npos)
            throw std::runtime_error("highlight missing from scene contract");

        bool rejected = false;
        try { scene.set_selection({999}); }
        catch (const std::invalid_argument&) { rejected = true; }
        if (!rejected) throw std::runtime_error("unknown atom selection was accepted");
        std::cout << "native molecular reference tests passed\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
