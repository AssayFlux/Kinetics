#include "kinetics/molecule.hpp"

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <map>
#include <sstream>
#include <stdexcept>
#include <tuple>
#include <vector>

namespace kinetics {
namespace {

std::string field(const std::string& line, std::size_t start, std::size_t length) {
    if (start >= line.size()) return {};
    return line.substr(start, std::min(length, line.size() - start));
}

std::string trim(std::string value) {
    const auto first = value.find_first_not_of(" \t\r\n");
    if (first == std::string::npos) return {};
    const auto last = value.find_last_not_of(" \t\r\n");
    return value.substr(first, last - first + 1);
}

int parse_int(const std::string& value, const std::string& label) {
    const auto text = trim(value);
    if (text.empty()) throw std::runtime_error("missing integer field: " + label);
    std::size_t used = 0;
    const int result = std::stoi(text, &used);
    if (used != text.size()) throw std::runtime_error("invalid integer field: " + label);
    return result;
}

double parse_double(const std::string& value, const std::string& label,
                    bool optional = false) {
    const auto text = trim(value);
    if (text.empty() && optional) return 0.0;
    if (text.empty()) throw std::runtime_error("missing numeric field: " + label);
    std::size_t used = 0;
    const double result = std::stod(text, &used);
    if (used != text.size() || !std::isfinite(result))
        throw std::runtime_error("invalid or non-finite numeric field: " + label);
    return result;
}

char char_at(const std::string& line, std::size_t index) {
    return index < line.size() ? line[index] : ' ';
}

std::string json_escape(const std::string& value) {
    std::ostringstream out;
    for (const unsigned char ch : value) {
        switch (ch) {
            case '"': out << "\\\""; break;
            case '\\': out << "\\\\"; break;
            case '\n': out << "\\n"; break;
            case '\r': out << "\\r"; break;
            case '\t': out << "\\t"; break;
            default:
                if (ch < 0x20U) {
                    out << "\\u" << std::hex << std::setw(4) << std::setfill('0')
                        << static_cast<int>(ch) << std::dec;
                } else {
                    out << static_cast<char>(ch);
                }
        }
    }
    return out.str();
}

void validate_atom_serials(const Structure& structure) {
    std::set<int> serials;
    for (const auto& atom : structure.atoms) {
        if (atom.serial <= 0) throw std::runtime_error("atom serials must be positive");
        if (!serials.insert(atom.serial).second)
            throw std::runtime_error("duplicate atom serial: " + std::to_string(atom.serial));
        for (const double coordinate : atom.position) {
            if (!std::isfinite(coordinate))
                throw std::runtime_error("atom coordinates must be finite");
        }
    }
}

}  // namespace

Structure load_pdb(const std::filesystem::path& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open PDB input: " + path.string());

    Structure structure;
    std::map<int, std::vector<int>> conect;
    std::string line;
    bool saw_model = false;
    bool in_first_model = true;
    bool finished_first_model = false;

    while (std::getline(input, line)) {
        const std::string record = trim(field(line, 0, 6));
        if (record == "MODEL") {
            if (!saw_model) {
                saw_model = true;
                in_first_model = true;
                const auto model_text = trim(field(line, 10, 4));
                if (!model_text.empty()) structure.model_number = parse_int(model_text, "MODEL");
            } else {
                in_first_model = false;
            }
            continue;
        }
        if (record == "ENDMDL") {
            if (in_first_model) {
                finished_first_model = true;
                in_first_model = false;
            }
            continue;
        }
        if (record == "CONECT") {
            const int source = parse_int(field(line, 6, 5), "CONECT source");
            for (std::size_t offset = 11; offset + 5 <= line.size(); offset += 5) {
                const auto target_text = trim(field(line, offset, 5));
                if (!target_text.empty())
                    conect[source].push_back(parse_int(target_text, "CONECT target"));
            }
            continue;
        }
        if (finished_first_model) continue;

        if (record == "ATOM" || record == "HETATM") {
            if (!in_first_model) continue;
            if (line.size() < 54) throw std::runtime_error("truncated PDB atom record");
            Atom atom;
            atom.serial = parse_int(field(line, 6, 5), "atom serial");
            atom.atom_name = trim(field(line, 12, 4));
            atom.alternate_location = char_at(line, 16);
            atom.residue_name = trim(field(line, 17, 3));
            atom.chain_id = char_at(line, 21);
            atom.residue_sequence = parse_int(field(line, 22, 4), "residue sequence");
            atom.insertion_code = char_at(line, 26);
            atom.position = {
                parse_double(field(line, 30, 8), "x"),
                parse_double(field(line, 38, 8), "y"),
                parse_double(field(line, 46, 8), "z")
            };
            atom.occupancy = parse_double(field(line, 54, 6), "occupancy", true);
            atom.temperature_factor = parse_double(field(line, 60, 6), "temperature factor", true);
            atom.element = trim(field(line, 76, 2));
            structure.atoms.push_back(std::move(atom));
        }
    }
    if (structure.atoms.empty()) throw std::runtime_error("PDB contains no atoms in first model");
    validate_atom_serials(structure);

    std::set<int> known;
    for (const auto& atom : structure.atoms) known.insert(atom.serial);
    std::set<std::pair<int, int>> unique_bonds;
    for (const auto& entry : conect) {
        if (known.count(entry.first) == 0)
            throw std::runtime_error("CONECT references unknown source atom serial");
        for (const int target : entry.second) {
            if (known.count(target) == 0)
                throw std::runtime_error("CONECT references unknown target atom serial");
            if (target == entry.first)
                throw std::runtime_error("CONECT self-bond is invalid");
            const auto key = std::minmax(entry.first, target);
            if (unique_bonds.insert(key).second)
                structure.bonds.push_back({key.first, key.second, "PDB_CONECT"});
        }
    }
    std::sort(structure.bonds.begin(), structure.bonds.end(),
              [](const Bond& a, const Bond& b) {
                  return std::tie(a.atom_serial_a, a.atom_serial_b) <
                         std::tie(b.atom_serial_a, b.atom_serial_b);
              });
    return structure;
}

MolecularScene::MolecularScene(Structure structure) : structure_(std::move(structure)) {
    validate_atom_serials(structure_);
}
const Structure& MolecularScene::structure() const noexcept { return structure_; }

void MolecularScene::set_selection(const std::vector<int>& atom_serials) {
    std::set<int> next;
    for (const int serial : atom_serials) {
        const auto found = std::find_if(structure_.atoms.begin(), structure_.atoms.end(),
            [serial](const Atom& atom) { return atom.serial == serial; });
        if (found == structure_.atoms.end())
            throw std::invalid_argument("selection references unknown atom serial");
        next.insert(serial);
    }
    selection_ = std::move(next);
}

void MolecularScene::set_highlights(const std::vector<int>& atom_serials) {
    std::set<int> next;
    for (const int serial : atom_serials) {
        const auto found = std::find_if(structure_.atoms.begin(), structure_.atoms.end(),
            [serial](const Atom& atom) { return atom.serial == serial; });
        if (found == structure_.atoms.end())
            throw std::invalid_argument("highlight references unknown atom serial");
        next.insert(serial);
    }
    highlights_ = std::move(next);
}
const std::set<int>& MolecularScene::selection() const noexcept { return selection_; }
const std::set<int>& MolecularScene::highlights() const noexcept { return highlights_; }

double distance_angstrom(const Atom& first, const Atom& second) {
    double squared = 0.0;
    for (std::size_t i = 0; i < 3; ++i) {
        const double delta = first.position[i] - second.position[i];
        squared += delta * delta;
    }
    return std::sqrt(squared);
}

std::string scene_to_json(const MolecularScene& scene) {
    const auto& structure = scene.structure();
    std::ostringstream out;
    out << std::setprecision(17);
    out << "{\"schema_version\":\"kinetics.molecular-scene/1.0\","
        << "\"engine_version\":\"" << kEngineVersion << "\","
        << "\"source_format\":\"" << structure.source_format << "\","
        << "\"coordinate_unit\":\"" << structure.coordinate_unit << "\","
        << "\"model_number\":" << structure.model_number << ",\"atoms\":[";
    for (std::size_t i = 0; i < structure.atoms.size(); ++i) {
        const auto& atom = structure.atoms[i];
        if (i) out << ',';
        out << "{\"serial\":" << atom.serial
            << ",\"atom_name\":\"" << json_escape(atom.atom_name)
            << "\",\"alternate_location\":\"" << json_escape(std::string(1, atom.alternate_location))
            << "\",\"residue_name\":\"" << json_escape(atom.residue_name)
            << "\",\"chain_id\":\"" << json_escape(std::string(1, atom.chain_id))
            << "\",\"residue_sequence\":" << atom.residue_sequence
            << ",\"insertion_code\":\"" << json_escape(std::string(1, atom.insertion_code))
            << "\",\"element\":\"" << json_escape(atom.element)
            << "\",\"occupancy\":" << atom.occupancy
            << ",\"temperature_factor\":" << atom.temperature_factor
            << ",\"position\":[" << atom.position[0] << ',' << atom.position[1]
            << ',' << atom.position[2] << "]}";
    }
    out << "],\"bonds\":[";
    for (std::size_t i = 0; i < structure.bonds.size(); ++i) {
        const auto& bond = structure.bonds[i];
        if (i) out << ',';
        out << "{\"atom_serial_a\":" << bond.atom_serial_a
            << ",\"atom_serial_b\":" << bond.atom_serial_b
            << ",\"source\":\"" << bond.source << "\"}";
    }
    out << "],\"selection\":[";
    bool first = true;
    for (const int serial : scene.selection()) {
        if (!first) out << ',';
        out << serial;
        first = false;
    }
    out << "],\"highlights\":[";
    first = true;
    for (const int serial : scene.highlights()) {
        if (!first) out << ',';
        out << serial;
        first = false;
    }
    out << "]}";
    return out.str();
}


std::string render_xy_ppm(const MolecularScene& scene, int width, int height) {
    if (width < 64 || height < 64 || width > 4096 || height > 4096)
        throw std::invalid_argument("render dimensions must be within [64, 4096]");
    using Pixel = std::array<int, 3>;
    const Pixel background{250, 250, 250};
    std::vector<Pixel> pixels(static_cast<std::size_t>(width) *
                              static_cast<std::size_t>(height), background);
    const auto& atoms = scene.structure().atoms;
    double min_x = atoms.front().position[0], max_x = min_x;
    double min_y = atoms.front().position[1], max_y = min_y;
    for (const auto& atom : atoms) {
        min_x = std::min(min_x, atom.position[0]);
        max_x = std::max(max_x, atom.position[0]);
        min_y = std::min(min_y, atom.position[1]);
        max_y = std::max(max_y, atom.position[1]);
    }
    const double span_x = std::max(max_x - min_x, 1.0);
    const double span_y = std::max(max_y - min_y, 1.0);
    const double scale = std::min((static_cast<double>(width) - 32.0) / span_x,
                                  (static_cast<double>(height) - 32.0) / span_y);
    const double center_x = (min_x + max_x) / 2.0;
    const double center_y = (min_y + max_y) / 2.0;
    const auto project = [&](const Atom& atom) {
        const int x = static_cast<int>(std::lround(
            static_cast<double>(width) / 2.0 +
            (atom.position[0] - center_x) * scale));
        const int y = static_cast<int>(std::lround(
            static_cast<double>(height) / 2.0 -
            (atom.position[1] - center_y) * scale));
        return std::pair<int, int>{x, y};
    };
    const auto set_pixel = [&](int x, int y, const Pixel& color) {
        if (x >= 0 && x < width && y >= 0 && y < height)
            pixels[static_cast<std::size_t>(y) * static_cast<std::size_t>(width) +
                   static_cast<std::size_t>(x)] = color;
    };
    const auto draw_line = [&](int x0, int y0, int x1, int y1, const Pixel& color) {
        const int dx = std::abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
        const int dy = -std::abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
        int error = dx + dy;
        while (true) {
            set_pixel(x0, y0, color);
            if (x0 == x1 && y0 == y1) break;
            const int twice = 2 * error;
            if (twice >= dy) { error += dy; x0 += sx; }
            if (twice <= dx) { error += dx; y0 += sy; }
        }
    };
    const auto draw_atom = [&](int cx, int cy, int radius, const Pixel& color) {
        for (int y = -radius; y <= radius; ++y)
            for (int x = -radius; x <= radius; ++x)
                if (x * x + y * y <= radius * radius)
                    set_pixel(cx + x, cy + y, color);
    };
    std::map<int, std::pair<int, int>> projected;
    for (const auto& atom : atoms) projected.emplace(atom.serial, project(atom));
    for (const auto& bond : scene.structure().bonds) {
        const auto left = projected.at(bond.atom_serial_a);
        const auto right = projected.at(bond.atom_serial_b);
        draw_line(left.first, left.second, right.first, right.second, {125, 125, 125});
    }
    for (const auto& atom : atoms) {
        const auto point = projected.at(atom.serial);
        Pixel color{90, 90, 90};
        if (atom.element == "O") color = {210, 55, 55};
        else if (atom.element == "N") color = {55, 85, 210};
        else if (atom.element == "S") color = {210, 175, 35};
        else if (atom.element == "P") color = {230, 130, 30};
        if (scene.highlights().count(atom.serial) != 0) color = {235, 90, 20};
        if (scene.selection().count(atom.serial) != 0) color = {20, 190, 75};
        draw_atom(point.first, point.second, 5, color);
    }
    std::ostringstream out;
    out << "P3\n" << width << ' ' << height << "\n255\n";
    for (const auto& pixel : pixels)
        out << pixel[0] << ' ' << pixel[1] << ' ' << pixel[2] << '\n';
    return out.str();
}

}  // namespace kinetics
