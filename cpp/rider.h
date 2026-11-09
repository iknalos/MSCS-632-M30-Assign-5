#pragma once

#include <memory>
#include <string>
#include <vector>

#include "ride.h"

class Rider {
public:
    Rider(std::string riderID, std::string name);

    void requestRide(std::shared_ptr<Ride> ride);
    void viewRides() const;  // prints the ride history and the total spent

    const std::string& riderID() const { return riderID_; }
    const std::string& name() const { return name_; }
    Money totalSpent() const;

private:
    std::string riderID_;
    std::string name_;
    std::vector<std::shared_ptr<Ride>> requestedRides_;
};
