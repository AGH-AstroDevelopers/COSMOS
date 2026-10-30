import { createContext } from "react";

// One parameter exactly as the telemetry server sends it.
export type ServerEntry = {
    value: number | boolean | string | null;
    unit?: string | null;
    status: "ok" | "warning" | "critical" | "unknown";
    timestamp: string; // time set by the source (can differ from this device's clock)
};

// The same entry plus the moment THIS browser received it and the id of the source it came from.
// Freshness is measured with receivedAt, so a tablet whose clock differs
// from the computer's clock still shows correct "receiving / not receiving".
export type ParameterValue = ServerEntry & { receivedAt: number; source: string };

// Latest value of every parameter, keyed like "thermal.temperature".
export type ParameterValues = Record<string, ParameterValue>;

export type ConnectionState = "connecting" | "connected" | "disconnected";

export type TelemetryContextValue = {
    values: ParameterValues;
    connection: ConnectionState;
    sourceId: string | null; // source selected on the server (null = not connected to a server)
};

// Default is used only when a component is rendered outside of the provider.
export const TelemetryContext = createContext<TelemetryContextValue>({
    values: {},
    connection: "disconnected",
    sourceId: null,
});