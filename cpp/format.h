#pragma once
// Small text helpers used by every class. The Smalltalk version has the same
// helpers in its Fmt class, so both programs print exactly the same text.

#include <cmath>
#include <string>

using Money = long long;  // whole cents, so fares never pick up rounding noise

namespace text {

inline std::string money(Money cents) {  // 1006 -> "$10.06"
    std::string c = std::to_string(cents % 100);
    if (c.size() < 2) c = "0" + c;
    return "$" + std::to_string(cents / 100) + "." + c;
}

inline std::string tenths(double x) {  // 4.2 -> "4.2"
    long long t = std::llround(x * 10);
    return std::to_string(t / 10) + "." + std::to_string(t % 10);
}

inline std::string padRight(const std::string& s, std::size_t width) {
    return s.size() >= width ? s : s + std::string(width - s.size(), ' ');
}

inline std::string padLeft(const std::string& s, std::size_t width) {
    return s.size() >= width ? s : std::string(width - s.size(), ' ') + s;
}

}  // namespace text
