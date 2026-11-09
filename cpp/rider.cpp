#include "rider.h"

#include <iostream>
#include <utility>

Rider::Rider(std::string riderID, std::string name)
    : riderID_(std::move(riderID)), name_(std::move(name)) {}

void Rider::requestRide(std::shared_ptr<Ride> ride) { requestedRides_.push_back(std::move(ride)); }

Money Rider::totalSpent() const {
    Money total = 0;
    for (const auto& ride : requestedRides_) total += ride->fare();
    return total;
}

void Rider::viewRides() const {
    std::cout << "  " << text::padRight(riderID_, 4) << name_ << ": " << requestedRides_.size()
              << " rides, total " << text::money(totalSpent()) << "\n";
    for (const auto& ride : requestedRides_) std::cout << "      " << ride->rideDetails() << "\n";
}
