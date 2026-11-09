# MSCS-632-M30 Advanced Programming Language: Assignment 5

**A class-based Ride Sharing System**, written twice: in **GNU Smalltalk** and in
**C++17**, with the same classes, the same rules and the same output. It shows
encapsulation, inheritance and polymorphism in both languages.

**Author:** Rahul Solanki · University of the Cumberlands · Instructor: Jay Thom

---

## Classes

| Class | What it does |
|---|---|
| `Ride` | Base class: `rideID`, `pickupLocation`, `dropoffLocation`, `distance`, `fare`; `fare()` (basic rate $1.50/mile) and `rideDetails()` |
| `StandardRide` | `Ride` subclass: $2.50 booking fee + $1.80/mile |
| `PremiumRide` | `Ride` subclass: $5.00 + $3.20/mile, **$15.00 minimum**, needs a driver rated 4.8+ |
| `SharedRide` | `StandardRide` subclass: the Standard fare with **30% off** (calls the parent's `fare()`) |
| `Driver` | `driverID`, `name`, `rating`, private `assignedRides`; `addRide()`, `getDriverInfo()`, `updateRating()` (rejects values outside 1.0 to 5.0), `earnings()`, `rides()` (returns a copy) |
| `Rider` | `riderID`, `name`, `requestedRides`; `requestRide()`, `viewRides()` |
| `RideSystem` | Keeps every ride, of every type, in one list and dispatches each request to the driver with the fewest rides (premium rides skip drivers rated below 4.8) |

Fares are kept in whole cents in both languages, so totals never pick up
floating-point noise.

## OOP principles, side by side

| | C++ | Smalltalk |
|---|---|---|
| Encapsulation | `private` / `protected` / `public`; `assignedRides_` is private, subclasses store a fare through protected `recordFare()`; bad distance throws `std::invalid_argument` | No access keywords: instance variables are only reachable from the object's own methods. `Driver` has no `assignedRides` accessor; `rides` answers a copy; a bad distance signals `Error` |
| Inheritance | `class SharedRide : public StandardRide`; constructors reused with `using Ride::Ride;`; `StandardRide::fare()` | `StandardRide subclass: SharedRide [...]`; subclasses use inherited instance variables directly; the class-side constructor is inherited; `super fare` |
| Polymorphism | `virtual` + `override`, virtual destructor; rides held as `std::vector<std::shared_ptr<Ride>>` | Every message is bound at run time; rides held in an `OrderedCollection`; `rides do: [:ride \| ride rideDetails]` |

The dispatcher asks each ride `needsTopDriver()` (only `PremiumRide` answers
true) instead of checking its class.

## Layout

```
cpp/          ride.h/.cpp, driver.h/.cpp, rider.h/.cpp, ride_system.h/.cpp, format.h, main.cpp, Makefile
smalltalk/    RideSharing.st (all classes), main.st (the demo), run.sh
output/       captured runs of both versions and the comparison
report/       the submitted report (.docx and .pdf) and its screenshots
tools/        make_outputs.sh, make_screenshots.ps1, capture_console.ps1, code_shots.py, make_report.py, apa.py, export_pdf.ps1
```

## Running it

**C++** (g++ 13, C++17):

```bash
cd cpp
make run
```

**Smalltalk** (GNU Smalltalk 3.2.5):

```bash
cd smalltalk
gst RideSharing.st main.st     # or ./run.sh
```

GNU Smalltalk is no longer packaged for Ubuntu 24.04. `run.sh` uses `gst` from
`PATH` if there is one; otherwise it runs a copy unpacked without root from the
Ubuntu 22.04 packages:

```bash
mkdir -p ~/tools/gst-debs && cd ~/tools/gst-debs
base=http://archive.ubuntu.com/ubuntu/pool/universe/g/gnu-smalltalk
for p in gnu-smalltalk libgst7; do curl -sO $base/${p}_3.2.5-1.3ubuntu1_amd64.deb; done
curl -sO $base/gnu-smalltalk-common_3.2.5-1.3ubuntu1_all.deb
for f in *.deb; do dpkg -x $f ~/tools/gst; done
```

## Verification

`tools/make_outputs.sh` builds and runs both versions, saves the output in
`output/`, and diffs the two runs: **all 56 lines after the header line are
identical** ([`output/compare.txt`](output/compare.txt)). The C++ version also
builds with `-Wall -Wextra -Wpedantic -Werror` and runs clean under
`-fsanitize=address,undefined`.

Sample run (both languages print this after their header line):
[`output/cpp_output.txt`](output/cpp_output.txt),
[`output/smalltalk_output.txt`](output/smalltalk_output.txt).
