#include "temperature_sensor.hpp"

Sensor::Sensor(int id, const std::string &name) : id(id), name(name) {}

int Sensor::get_id() const {
    return id;
}

const std::string &Sensor::get_name() const {
    return name;
}

double Sensor::read() const {
    return 0.0;
}

TemperatureSensor::TemperatureSensor(int id, const std::string &name, double celsius)
    : Sensor(id, name), celsius(celsius) {}

double TemperatureSensor::read() const {
    return celsius;
}

void TemperatureSensor::set_celsius(double new_value) {
    this->celsius = new_value;
}
