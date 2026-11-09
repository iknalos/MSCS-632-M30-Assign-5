"Ride Sharing System, GNU Smalltalk version: the demo.
 Run from this folder:  gst RideSharing.st main.st"

| rideSystem carlos aisha ben maya leo priya total result copy |

Transcript showCr: 'Ride Sharing System (GNU Smalltalk)'; showCr: (String new: 64 withAll: $=).

rideSystem := RideSystem new.
carlos := rideSystem addDriver: (Driver id: 'D1' name: 'Carlos' rating: 4.9).
aisha := rideSystem addDriver: (Driver id: 'D2' name: 'Aisha' rating: 4.8).
ben := rideSystem addDriver: (Driver id: 'D3' name: 'Ben' rating: 4.5).
maya := Rider id: 'R1' name: 'Maya'.
leo := Rider id: 'R2' name: 'Leo'.
priya := Rider id: 'R3' name: 'Priya'.

Transcript cr; showCr: '1. Riders request rides'.
rideSystem rider: maya requests: (StandardRide id: 'S101' from: 'Back Bay' to: 'Logan Airport' miles: 4.2).
rideSystem rider: leo requests: (PremiumRide id: 'P102' from: 'Cambridge' to: 'Seaport' miles: 5.5).
rideSystem rider: priya requests: (SharedRide id: 'H103' from: 'Fenway' to: 'Harvard Square' miles: 3.1).
rideSystem rider: leo requests: (StandardRide id: 'S104' from: 'Logan Airport' to: 'Quincy' miles: 9.8).
rideSystem rider: maya requests: (PremiumRide id: 'P105' from: 'North End' to: 'South Boston' miles: 1.6).
rideSystem rider: priya requests: (SharedRide id: 'H106' from: 'Somerville' to: 'MIT' miles: 2.5).
rideSystem rider: priya requests: (Ride id: 'B107' from: 'Brookline' to: 'Back Bay' miles: 3.0).

Transcript cr; showCr: '2. Dispatch (premium rides need a driver rated 4.8 or higher)'.
rideSystem dispatchAll.

Transcript cr; showCr: '3. All rides in one list: rideDetails() and fare() on each, whatever its type'.
Transcript showCr: '  ', (Fmt pad: 'ID' to: 6), (Fmt pad: 'Type' to: 10), (Fmt pad: 'Route' to: 28),
    'Distance', (Fmt padLeft: 'Fare' to: 10).
total := 0.
rideSystem rides do: [:ride |
    "Any object that understands rideDetails and fare can be in this list."
    Transcript showCr: '  ', ride rideDetails.
    total := total + ride fare].
Transcript showCr: '  All fares: ', (Fmt money: total).

Transcript cr; showCr: '4. Drivers (getDriverInfo)'.
rideSystem drivers do: [:driver | Transcript showCr: '  ', driver getDriverInfo].

Transcript cr; showCr: '5. Riders (viewRides)'.
maya viewRides.
leo viewRides.
priya viewRides.

Transcript cr; showCr: '6. Encapsulation'.
(carlos updateRating: 6.0) ifFalse: [
    Transcript showCr: '  Carlos: rating 6.0 rejected (must be 1.0 to 5.0), still ', (Fmt tenths: carlos rating)].
(ben updateRating: 4.6) ifTrue: [
    Transcript showCr: '  Ben: rating 4.6 accepted, now ', (Fmt tenths: ben rating)].
result := [StandardRide id: 'S108' from: 'Allston' to: 'Brighton' miles: -3.0.
           'created']
    on: Error do: [:e | e return: 'with -3.0 miles rejected: ', e messageText].
Transcript showCr: '  Ride S108 ', result.
copy := aisha rides.
copy add: (StandardRide id: 'S109' from: 'Allston' to: 'Brighton' miles: 2.0).
Transcript showCr: '  Added a ride to a copy of Aisha''s list: the copy has ', copy size printString,
    ', Aisha still has ', aisha rideCount printString.
