#pragma once

#include <memory>
#include <string>
#include <vector>

#include "ride.h"

class Driver {
public:
    Driver(std::string driverID, std::string name, double rating);

    void addRide(std::shared_ptr<Ride> ride);
    std::string getDriverInfo() const;
    bool updateRating(double newRating);  // false, and no change, outside 1.0 to 5.0

    const std::string& driverID() const { return driverID_; }
    const std::string& name() const { return name_; }
    double rating() const { return rating_; }
    std::size_t rideCount() const { return assignedRides_.size(); }
    Money earnings() const;
    std::vector<std::shared_ptr<Ride>> rides() const;  // a copy of the list

private:
    std::string driverID_;
    std::string name_;
    double rating_;
    std::vector<std::shared_ptr<Ride>> assignedRides_;  // only reachable through the methods above
};
