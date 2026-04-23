#include "temperature_sensor.hpp"

#include <cassert>
#include <cmath>
#include <memory>
#include <string>

static bool close_enough(double a, double b) {
    return std::fabs(a - b) < 1e-9;
}

static void test_constructor_stores_data(void) {
    TemperatureSensor sensor(7, "Lab", 21.5);

    assert(sensor.get_id() == 7);
    assert(sensor.get_name() == "Lab");
    assert(close_enough(sensor.read(), 21.5));
}

static void test_virtual_dispatch_works_through_base_pointer(void) {
    std::unique_ptr<Sensor> sensor = std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);

    assert(sensor->get_name() == std::string("Server Room"));
    assert(close_enough(sensor->read(), 18.0));
}

static void test_setter_updates_temperature(void) {
    TemperatureSensor sensor(2, "Office", 19.0);
    sensor.set_celsius(23.25);

    assert(close_enough(sensor.read(), 23.25));
}

int main() {
    test_constructor_stores_data();
    test_virtual_dispatch_works_through_base_pointer();
    test_setter_updates_temperature();
}
