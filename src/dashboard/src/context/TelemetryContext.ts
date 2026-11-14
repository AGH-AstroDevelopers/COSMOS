import { createContext } from "react";

// One parameter exactly as the telemetry server sends it.
export type ServerEntry = {
    value: number | boolean | string | null;
    unit?: string | null;
    // TODO: the server sends no status (null) for booleans and enums; this type does not allow it yet.
    status: "ok" | "warning" | "critical" | "unknown";
    timestamp: string; // set by the source, so it can differ from this device's clock
};

// A server entry plus data added by this browser on arrival.
// receivedAt (this device's clock) is used to judge freshness, so a device
// with a wrong clock still shows a correct "receiving / not receiving".
export type ParameterValue = ServerEntry & { receivedAt: number; source: string };

// Latest value of every parameter, keyed "<subsystem>.<parameter>", e.g. "thermal.temperature".
export type ParameterValues = Record<string, ParameterValue>;

export type ConnectionState = "connecting" | "connected" | "disconnected";

export type TelemetryContextValue = {
    values: ParameterValues;
    connection: ConnectionState;
    sourceId: string | null; // source the server is connected to; null while disconnected
};

// Used only by components rendered outside of TelemetryProvider.
export const TelemetryContext = createContext<TelemetryContextValue>({
    values: {},
    connection: "disconnected",
    sourceId: null,
});