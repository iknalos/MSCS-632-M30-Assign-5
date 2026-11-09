#pragma once
// Keeps every ride in one list and hands requested rides to drivers.

#include <memory>
#include <vector>

#include "driver.h"
#include "ride.h"
#include "rider.h"

class RideSystem {
public:
    static constexpr double kTopRating = 4.8;  // premium rides need at least this

    std::shared_ptr<Driver> addDriver(std::shared_ptr<Driver> driver);
    std::shared_ptr<Ride> request(Rider& rider, std::shared_ptr<Ride> ride);
    void dispatchAll();  // gives each waiting ride to a driver

    const std::vector<std::shared_ptr<Ride>>& rides() const { return rides_; }
    const std::vector<std::shared_ptr<Driver>>& drivers() const { return drivers_; }

private:
    std::shared_ptr<Driver> driverFor(const Ride& ride) const;

    std::vector<std::shared_ptr<Driver>> drivers_;
    std::vector<std::shared_ptr<Ride>> rides_;    // every ride, of every type
    std::vector<std::shared_ptr<Ride>> waiting_;  // requested but not yet dispatched
};
