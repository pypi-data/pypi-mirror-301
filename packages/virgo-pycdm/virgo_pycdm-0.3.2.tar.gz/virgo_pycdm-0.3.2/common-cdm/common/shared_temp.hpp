#pragma once

#include <array>

constexpr unsigned k_num_temp_sensors = 3;

struct BsdaTemperatureReadings {
    std::array<uint16_t, k_num_temp_sensors> val;
    std::array<uint64_t, k_num_temp_sensors> ts;

    std::array<uint32_t, 2> val_pt100;
    uint64_t ts_pt100;
};

/// struct to hold both, I2C temperatures for the 3 sensors and I2C temperatures
struct EbiTemperatureReadings {
    /// Raw I2C values
    std::array<uint16_t, k_num_temp_sensors> val;
    /// Timestamps
    std::array<uint64_t, k_num_temp_sensors> ts;
    /// Converted values to ºC
    std::array<float, k_num_temp_sensors> temps;

    std::array<uint32_t, 2> raw_pt100;
    /// Timestamps
    uint64_t ts_pt100;
    /// Converted values ºC
    float temp_pt100;
};

EbiTemperatureReadings bsda2EbiTemperatures(const BsdaTemperatureReadings& bsda_temps);
float convertPt100Temp(std::array<uint32_t, 2> v);
