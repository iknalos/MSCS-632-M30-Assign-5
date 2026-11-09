#include "ride.h"

#include <algorithm>
#include <cmath>
#include <stdexcept>
#include <utility>

// ---- Ride ----------------------------------------------------------------

Ride::Ride(std::string rideID, std::string pickupLocation, std::string dropoffLocation,
           double distance)
    : rideID_(std::move(rideID)),
      pickupLocation_(std::move(pickupLocation)),
      dropoffLocation_(std::move(dropoffLocation)),
      distance_(distance) {
    if (!(distance > 0)) throw std::invalid_argument("distance must be greater than 0");
}

Money Ride::recordFare(Money cents) {
    fare_ = cents;
    return fare_;
}

Money Ride::fare() { return recordFare(std::llround(150 * distance_)); }

std::string Ride::rideType() const { return "Basic"; }

bool Ride::needsTopDriver() const { return false; }

std::string Ride::rideDetails() {
    // rideType() and fare() are virtual, so this one method prints every kind of ride.
    return text::padRight(rideID_, 6) + text::padRight(rideType(), 10) +
           text::padRight(route(), 28) + text::padLeft(text::tenths(distance_), 5) + " mi" +
           text::padLeft(text::money(fare()), 10);
}

// ---- StandardRide --------------------------------------------------------

Money StandardRide::fare() { return recordFare(250 + std::llround(180 * distance())); }

std::string StandardRide::rideType() const { return "Standard"; }

// ---- PremiumRide ---------------------------------------------------------

Money PremiumRide::meteredFare() const { return 500 + std::llround(320 * distance()); }

Money PremiumRide::fare() { return recordFare(std::max<Money>(meteredFare(), 1500)); }

std::string PremiumRide::rideType() const { return "Premium"; }

bool PremiumRide::needsTopDriver() const { return true; }

std::string PremiumRide::rideDetails() {
    std::string line = Ride::rideDetails() + "  top-rated driver";
    if (meteredFare() < 1500) line += ", minimum fare";
    return line;
}

// ---- SharedRide ----------------------------------------------------------

Money SharedRide::fare() {
    Money full = StandardRide::fare();      // reuse the parent's formula
    return recordFare((full * 7 + 5) / 10);  // 70%, rounded to the nearest cent
}

std::string SharedRide::rideType() const { return "Shared"; }

std::string SharedRide::rideDetails() { return StandardRide::rideDetails() + "  30% off Standard"; }
