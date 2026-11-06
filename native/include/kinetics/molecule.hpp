#pragma once

#include <array>
#include <cstddef>
#include <filesystem>
#include <set>
#include <string>
#include <vector>

namespace kinetics {

inline constexpr const char* kEngineVersion = "0.1.0";
inline constexpr const char* kCoordinateUnit = "angstrom";

struct Atom {
    int serial{};
    std::string atom_name;
    char alternate_location{' '};
    std::string residue_name;
    char chain_id{' '};
    int residue_sequence{};
    char insertion_code{' '};
    std::string element;
    double occupancy{};
    double temperature_factor{};
    std::array<double, 3> position{};
};

struct Bond {
    int atom_serial_a{};
    int atom_serial_b{};
    std::string source{"PDB_CONECT"};
};

struct Structure {
    std::string source_format{"PDB"};
    std::string coordinate_unit{kCoordinateUnit};
    int model_number{1};
    std::vector<Atom> atoms;
    std::vector<Bond> bonds;
};

class MolecularScene {
public:
    explicit MolecularScene(Structure structure);
    const Structure& structure() const noexcept;
    void set_selection(const std::vector<int>& atom_serials);
    void set_highlights(const std::vector<int>& atom_serials);
    const std::set<int>& selection() const noexcept;
    const std::set<int>& highlights() const noexcept;

private:
    Structure structure_;
    std::set<int> selection_;
    std::set<int> highlights_;
};

Structure load_pdb(const std::filesystem::path& path);
double distance_angstrom(const Atom& first, const Atom& second);
std::string scene_to_json(const MolecularScene& scene);

}  // namespace kinetics
