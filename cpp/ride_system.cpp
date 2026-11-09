#include "ride_system.h"

#include <iostream>
#include <utility>

std::shared_ptr<Driver> RideSystem::addDriver(std::shared_ptr<Driver> driver) {
    drivers_.push_back(driver);
    return driver;
}

std::shared_ptr<Ride> RideSystem::request(Rider& rider, std::shared_ptr<Ride> ride) {
    rider.requestRide(ride);
    rides_.push_back(ride);
    waiting_.push_back(ride);
    std::cout << "  " << text::padRight(rider.name(), 7) << "requested "
              << text::padRight(ride->rideID(), 6) << text::padRight(ride->rideType(), 10)
              << ride->route() << "\n";
    return ride;
}

// The driver with the fewest rides so far; premium rides skip drivers rated
// below kTopRating. Ties go to the driver added first.
std::shared_ptr<Driver> RideSystem::driverFor(const Ride& ride) const {
    std::shared_ptr<Driver> best;
    for (const auto& driver : drivers_) {
        if (ride.needsTopDriver() && driver->rating() < kTopRating) continue;
        if (!best || driver->rideCount() < best->rideCount()) best = driver;
    }
    return best;
}

void RideSystem::dispatchAll() {
    for (const auto& ride : waiting_) {
        std::cout << "  " << text::padRight(ride->rideID(), 6)
                  << text::padRight(ride->rideType(), 10);
        auto driver = driverFor(*ride);
        if (!driver) {
            std::cout << "no driver available\n";
            continue;
        }
        driver->addRide(ride);
        std::cout << "-> " << driver->driverID() << " " << driver->name() << " (rating "
                  << text::tenths(driver->rating()) << ")\n";
    }
    waiting_.clear();
}
