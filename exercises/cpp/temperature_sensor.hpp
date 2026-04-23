#ifndef TEMPERATURE_SENSOR_HPP
#define TEMPERATURE_SENSOR_HPP

#include <string>

class Sensor {
private:
    int id;

protected:
    std::string name;

public:
    Sensor(int id, const std::string &name);
    virtual ~Sensor() = default;

    int get_id() const;
    const std::string &get_name() const;
    virtual double read() const;
};

class TemperatureSensor : public Sensor {
private:
    double celsius;

public:
    TemperatureSensor(int id, const std::string &name, double celsius);

    double read() const override;
    void set_celsius(double new_value);
};

#endif
