CXX ?= g++
CXXFLAGS ?= -std=c++17 -Wall -Wextra -Wpedantic -O2
SRC := main.cpp ride.cpp driver.cpp rider.cpp ride_system.cpp

ride_sharing: $(SRC) $(wildcard *.h)
	$(CXX) $(CXXFLAGS) -o $@ $(SRC)

run: ride_sharing
	./ride_sharing

clean:
	rm -f ride_sharing

.PHONY: run clean
