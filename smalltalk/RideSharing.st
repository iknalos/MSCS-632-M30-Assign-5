"Ride Sharing System, GNU Smalltalk version: the classes.
 Run from this folder:  gst RideSharing.st main.st
 Fares are kept in whole cents. Fmt holds the same text helpers as
 cpp/format.h, so both programs print exactly the same text."

Object subclass: Fmt [
    <comment: 'Text helpers shared by every class.'>

    Fmt class >> money: cents [
        "1006 -> '$10.06'"
        ^'$', (cents // 100) printString, '.', ((cents \\ 100) printPaddedWith: $0 to: 2)
    ]

    Fmt class >> tenths: aNumber [
        "4.2 -> '4.2'"
        | t |
        t := (aNumber * 10) rounded.
        ^(t // 10) printString, '.', (t \\ 10) printString
    ]

    Fmt class >> pad: aString to: width [
        aString size >= width ifTrue: [^aString].
        ^aString, (String new: width - aString size withAll: Character space)
    ]

    Fmt class >> padLeft: aString to: width [
        aString size >= width ifTrue: [^aString].
        ^(String new: width - aString size withAll: Character space), aString
    ]
]

Object subclass: Ride [
    "Instance variables can only be read or changed by this object's own
     methods, including methods inherited by subclasses."
    | rideID pickupLocation dropoffLocation distance fare |
    <comment: 'Base class: every ride has an ID, a route, a distance and a fare.'>

    Ride class >> id: anID from: pickup to: dropoff miles: miles [
        "Class methods are inherited too, so every subclass gets this constructor
         and 'self new' makes an instance of whichever class received it."
        miles > 0 ifFalse: [^self error: 'distance must be greater than 0'].
        ^self new setID: anID from: pickup to: dropoff miles: miles
    ]

    setID: anID from: pickup to: dropoff miles: miles [
        <category: 'private'>
        rideID := anID.
        pickupLocation := pickup.
        dropoffLocation := dropoff.
        distance := miles
    ]

    rideID [ ^rideID ]
    distance [ ^distance ]
    route [ ^pickupLocation, ' -> ', dropoffLocation ]

    fare [
        "Basic rate: $1.50 per mile."
        ^fare := (150 * distance) rounded
    ]

    rideType [ ^'Basic' ]

    needsTopDriver [ ^false ]

    rideDetails [
        "rideType and fare are looked up on the receiver at run time, so this
         one method prints every kind of ride."
        ^(Fmt pad: rideID to: 6), (Fmt pad: self rideType to: 10),
            (Fmt pad: self route to: 28), (Fmt padLeft: (Fmt tenths: distance) to: 5), ' mi',
            (Fmt padLeft: (Fmt money: self fare) to: 10)
    ]
]

Ride subclass: StandardRide [
    <comment: '$2.50 booking fee + $1.80 per mile.'>

    fare [ ^fare := 250 + (180 * distance) rounded ]

    rideType [ ^'Standard' ]
]

Ride subclass: PremiumRide [
    <comment: '$5.00 + $3.20 per mile, never less than $15.00, top-rated drivers only.'>

    meteredFare [
        "The fare before the $15.00 minimum."
        ^500 + (320 * distance) rounded
    ]

    fare [ ^fare := self meteredFare max: 1500 ]

    rideType [ ^'Premium' ]

    needsTopDriver [ ^true ]

    rideDetails [
        ^super rideDetails, '  top-rated driver',
            (self meteredFare < 1500 ifTrue: [', minimum fare'] ifFalse: [''])
    ]
]

StandardRide subclass: SharedRide [
    <comment: 'A Standard ride shared with other riders: the Standard fare with 30% off.'>

    fare [
        "super fare reuses the parent's formula; 70%, rounded to the nearest cent."
        ^fare := (super fare * 7 / 10) rounded
    ]

    rideType [ ^'Shared' ]

    rideDetails [ ^super rideDetails, '  30% off Standard' ]
]

Object subclass: Driver [
    | driverID name rating assignedRides |
    <comment: 'assignedRides has no accessor: it is reached only through addRide:, rideCount, earnings and rides.'>

    Driver class >> id: anID name: aName rating: aNumber [
        ^self new setID: anID name: aName rating: aNumber
    ]

    setID: anID name: aName rating: aNumber [
        <category: 'private'>
        driverID := anID.
        name := aName.
        rating := aNumber.
        assignedRides := OrderedCollection new
    ]

    driverID [ ^driverID ]
    name [ ^name ]
    rating [ ^rating ]

    addRide: aRide [
        assignedRides add: aRide.
        ^aRide
    ]

    updateRating: aNumber [
        "Answers false, and changes nothing, outside 1.0 to 5.0."
        (aNumber between: 1.0 and: 5.0) ifFalse: [^false].
        rating := aNumber.
        ^true
    ]

    rideCount [ ^assignedRides size ]

    earnings [ ^assignedRides inject: 0 into: [:sum :ride | sum + ride fare] ]

    rides [
        "A copy, so callers cannot change the real list."
        ^assignedRides copy
    ]

    getDriverInfo [
        | ids |
        ids := WriteStream on: String new.
        assignedRides do: [:ride | ids nextPutAll: ride rideID] separatedBy: [ids nextPutAll: ', '].
        ^(Fmt pad: driverID to: 4), (Fmt pad: name to: 8), 'rating ', (Fmt tenths: rating),
            '   ', self rideCount printString, ' rides   earned ', (Fmt money: self earnings),
            (String with: Character nl), '      rides: ', ids contents
    ]
]

Object subclass: Rider [
    | riderID name requestedRides |

    Rider class >> id: anID name: aName [ ^self new setID: anID name: aName ]

    setID: anID name: aName [
        <category: 'private'>
        riderID := anID.
        name := aName.
        requestedRides := OrderedCollection new
    ]

    riderID [ ^riderID ]
    name [ ^name ]

    requestRide: aRide [
        requestedRides add: aRide.
        ^aRide
    ]

    totalSpent [ ^requestedRides inject: 0 into: [:sum :ride | sum + ride fare] ]

    viewRides [
        "Prints the ride history and the total spent."
        Transcript showCr: '  ', (Fmt pad: riderID to: 4), name, ': ',
            requestedRides size printString, ' rides, total ', (Fmt money: self totalSpent).
        requestedRides do: [:ride | Transcript showCr: '      ', ride rideDetails]
    ]
]

Object subclass: RideSystem [
    "Keeps every ride in one list and hands requested rides to drivers."
    | drivers rides waiting |

    RideSystem class >> new [ ^super new init ]

    RideSystem class >> topRating [
        "Premium rides need a driver rated at least this."
        ^4.8
    ]

    init [
        <category: 'private'>
        drivers := OrderedCollection new.
        rides := OrderedCollection new.     "every ride, of every type"
        waiting := OrderedCollection new    "requested but not yet dispatched"
    ]

    addDriver: aDriver [
        drivers add: aDriver.
        ^aDriver
    ]

    rider: aRider requests: aRide [
        aRider requestRide: aRide.
        rides add: aRide.
        waiting add: aRide.
        Transcript showCr: '  ', (Fmt pad: aRider name to: 7), 'requested ',
            (Fmt pad: aRide rideID to: 6), (Fmt pad: aRide rideType to: 10), aRide route.
        ^aRide
    ]

    driverFor: aRide [
        "The driver with the fewest rides so far; premium rides skip drivers rated
         below topRating. Ties go to the driver added first."
        | best |
        drivers do: [:driver |
            (aRide needsTopDriver and: [driver rating < self class topRating]) ifFalse: [
                (best isNil or: [driver rideCount < best rideCount]) ifTrue: [best := driver]]].
        ^best
    ]

    dispatchAll [
        waiting do: [:ride |
            | driver line |
            line := '  ', (Fmt pad: ride rideID to: 6), (Fmt pad: ride rideType to: 10).
            driver := self driverFor: ride.
            driver isNil
                ifTrue: [Transcript showCr: line, 'no driver available']
                ifFalse: [
                    driver addRide: ride.
                    Transcript showCr: line, '-> ', driver driverID, ' ', driver name,
                        ' (rating ', (Fmt tenths: driver rating), ')']].
        waiting := OrderedCollection new
    ]

    rides [ ^rides copy ]
    drivers [ ^drivers copy ]
]
