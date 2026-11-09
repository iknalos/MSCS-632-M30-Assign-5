#include "driver.h"

#include <utility>

Driver::Driver(std::string driverID, std::string name, double rating)
    : driverID_(std::move(driverID)), name_(std::move(name)), rating_(rating) {}

void Driver::addRide(std::shared_ptr<Ride> ride) { assignedRides_.push_back(std::move(ride)); }

bool Driver::updateRating(double newRating) {
    if (newRating < 1.0 || newRating > 5.0) return false;
    rating_ = newRating;
    return true;
}

Money Driver::earnings() const {
    Money total = 0;
    for (const auto& ride : assignedRides_) total += ride->fare();  // virtual call
    return total;
}

std::vector<std::shared_ptr<Ride>> Driver::rides() const { return assignedRides_; }

std::string Driver::getDriverInfo() const {
    std::string ids;
    for (const auto& ride : assignedRides_) ids += (ids.empty() ? "" : ", ") + ride->rideID();
    return text::padRight(driverID_, 4) + text::padRight(name_, 8) + "rating " +
           text::tenths(rating_) + "   " + std::to_string(rideCount()) + " rides   earned " +
           text::money(earnings()) + "\n      rides: " + ids;
}
