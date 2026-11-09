// Ride Sharing System, C++ version. Build and run:  make run
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

#include "driver.h"
#include "ride.h"
#include "ride_system.h"
#include "rider.h"

static void section(const std::string& title) { std::cout << "\n" << title << "\n"; }

int main() {
    std::cout << "Ride Sharing System (C++)\n" << std::string(64, '=') << "\n";

    RideSystem rideSystem;
    auto carlos = rideSystem.addDriver(std::make_shared<Driver>("D1", "Carlos", 4.9));
    auto aisha = rideSystem.addDriver(std::make_shared<Driver>("D2", "Aisha", 4.8));
    auto ben = rideSystem.addDriver(std::make_shared<Driver>("D3", "Ben", 4.5));
    Rider maya("R1", "Maya"), leo("R2", "Leo"), priya("R3", "Priya");

    section("1. Riders request rides");
    rideSystem.request(maya, std::make_shared<StandardRide>("S101", "Back Bay", "Logan Airport", 4.2));
    rideSystem.request(leo, std::make_shared<PremiumRide>("P102", "Cambridge", "Seaport", 5.5));
    rideSystem.request(priya, std::make_shared<SharedRide>("H103", "Fenway", "Harvard Square", 3.1));
    rideSystem.request(leo, std::make_shared<StandardRide>("S104", "Logan Airport", "Quincy", 9.8));
    rideSystem.request(maya, std::make_shared<PremiumRide>("P105", "North End", "South Boston", 1.6));
    rideSystem.request(priya, std::make_shared<SharedRide>("H106", "Somerville", "MIT", 2.5));
    rideSystem.request(priya, std::make_shared<Ride>("B107", "Brookline", "Back Bay", 3.0));

    section("2. Dispatch (premium rides need a driver rated 4.8 or higher)");
    rideSystem.dispatchAll();

    section("3. All rides in one list: rideDetails() and fare() on each, whatever its type");
    std::cout << "  " << text::padRight("ID", 6) << text::padRight("Type", 10)
              << text::padRight("Route", 28) << "Distance" << text::padLeft("Fare", 10) << "\n";
    Money total = 0;
    for (const auto& ride : rideSystem.rides()) {  // std::shared_ptr<Ride>, any subclass
        std::cout << "  " << ride->rideDetails() << "\n";
        total += ride->fare();
    }
    std::cout << "  All fares: " << text::money(total) << "\n";

    section("4. Drivers (getDriverInfo)");
    for (const auto& driver : rideSystem.drivers()) std::cout << "  " << driver->getDriverInfo() << "\n";

    section("5. Riders (viewRides)");
    maya.viewRides();
    leo.viewRides();
    priya.viewRides();

    section("6. Encapsulation");
    if (!carlos->updateRating(6.0))
        std::cout << "  Carlos: rating 6.0 rejected (must be 1.0 to 5.0), still "
                  << text::tenths(carlos->rating()) << "\n";
    if (ben->updateRating(4.6))
        std::cout << "  Ben: rating 4.6 accepted, now " << text::tenths(ben->rating()) << "\n";
    try {
        StandardRide bad("S108", "Allston", "Brighton", -3.0);
        std::cout << "  Ride S108 created\n";
    } catch (const std::invalid_argument& e) {
        std::cout << "  Ride S108 with -3.0 miles rejected: " << e.what() << "\n";
    }
    auto copy = aisha->rides();
    copy.push_back(std::make_shared<StandardRide>("S109", "Allston", "Brighton", 2.0));
    std::cout << "  Added a ride to a copy of Aisha's list: the copy has " << copy.size()
              << ", Aisha still has " << aisha->rideCount() << "\n";
    return 0;
}
