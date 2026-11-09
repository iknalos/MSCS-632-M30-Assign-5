#pragma once
// Ride and its subclasses. Fares are kept in whole cents.

#include <string>

#include "format.h"

// Base class: every ride has an ID, a route, a distance and a fare.
class Ride {
public:
    Ride(std::string rideID, std::string pickupLocation, std::string dropoffLocation,
         double distance);
    virtual ~Ride() = default;  // rides are deleted through Ride pointers

    virtual Money fare();                  // basic rate: $1.50 per mile
    virtual std::string rideType() const;  // "Basic"
    virtual bool needsTopDriver() const;   // only premium rides say yes
    virtual std::string rideDetails();     // one line: ID, type, route, miles, fare

    const std::string& rideID() const { return rideID_; }
    double distance() const { return distance_; }
    std::string route() const { return pickupLocation_ + " -> " + dropoffLocation_; }

protected:
    // Subclasses cannot touch fare_ directly; they store a fare through this.
    Money recordFare(Money cents);

private:
    std::string rideID_;
    std::string pickupLocation_;
    std::string dropoffLocation_;
    double distance_;
    Money fare_ = 0;  // the fare from the last fare() call
};

// $2.50 booking fee + $1.80 per mile.
class StandardRide : public Ride {
public:
    using Ride::Ride;  // constructors are not inherited unless asked for
    Money fare() override;
    std::string rideType() const override;
};

// $5.00 + $3.20 per mile, never less than $15.00, top-rated drivers only.
class PremiumRide : public Ride {
public:
    using Ride::Ride;
    Money fare() override;
    std::string rideType() const override;
    bool needsTopDriver() const override;
    std::string rideDetails() override;

private:
    Money meteredFare() const;  // the fare before the $15.00 minimum
};

// A Standard ride shared with other riders: the Standard fare with 30% off.
class SharedRide : public StandardRide {
public:
    using StandardRide::StandardRide;
    Money fare() override;
    std::string rideType() const override;
    std::string rideDetails() override;
};
