import type { SubsystemConfig } from "../types/telemetry";

export const telemetryConfig: SubsystemConfig[] = [
    {
        id: "thermal",
        name: "Thermal subsystem",
        parameters: [
            {
                id: "temperature",
                name: "Temperature",
                type: "number",
                unit: "°C",
                visualizations: ["line", "gauge", "value", "bar"],
            },
            {
                id: "heater",
                name: "Heater",
                type: "boolean",
                visualizations: ["value"],
            },
            {
                id: "status",
                name: "Status",
                type: "enum",
                visualizations: ["value"],
            },
        ],
    },

    {
        id: "power",
        name: "Power subsystem",
        parameters: [
            {
                id: "voltage",
                name: "Voltage",
                type: "number",
                unit: "V",
                visualizations: ["line", "gauge", "value"],
            },
            {
                id: "current",
                name: "Current",
                type: "number",
                unit: "A",
                visualizations: ["line", "gauge", "value"],
            },
            {
                id: "battery",
                name: "Battery",
                type: "number",
                unit: "%",
                visualizations: ["line", "gauge", "value", "bar"],
            },
        ],
    },

    {
        id: "adcs",
        name: "Attitude system (ADCS)",
        parameters: [
            {
                id: "roll",
                name: "Roll",
                type: "number",
                unit: "°",
                visualizations: ["line", "gauge", "value"],
            },
            {
                id: "pitch",
                name: "Pitch",
                type: "number",
                unit: "°",
                visualizations: ["line", "gauge", "value"],
            },
            {
                id: "yaw",
                name: "Yaw",
                type: "number",
                unit: "°",
                visualizations: ["line", "gauge", "value"],
            },
        ],
    },

    {
        id: "obc",
        name: "On-board computer",
        parameters: [
            {
                id: "cpu",
                name: "CPU usage",
                type: "number",
                unit: "%",
                visualizations: ["line", "gauge", "value"],
            },
            {
                id: "memory",
                name: "Memory usage",
                type: "number",
                unit: "%",
                visualizations: ["line", "gauge", "value"],
            },
            {
                id: "status",
                name: "System status",
                type: "enum",
                visualizations: ["value"],
            },
        ],
    },
];