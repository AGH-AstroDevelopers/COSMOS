import { useContext, useEffect, useState } from "react";
import { TelemetryContext, type ParameterValue } from "../context/TelemetryContext";

// Data older than this counts as "not receiving".
// The simulator sends every 1 s. TODO: make it a per-source setting.
export const STALE_AFTER_MS = 5000;

type ParameterData = {
    data: ParameterValue | undefined; // last known value (undefined = never received)
    receiving: boolean;               // true only if the value is fresh AND the server connection is up
    ageSeconds: number | null;        // seconds since the last value (null = never received)
};

// Gives a widget the data of ONE parameter, e.g. useParameterData("thermal.temperature").
export function useParameterData(parameterKey: string): ParameterData {
    const { values, connection } = useContext(TelemetryContext);

    // "Not receiving" means nothing arrives, so nothing would re-render the widget.
    // A 1 s clock tick makes the widget re-check how old its data is.
    const [now, setNow] = useState(() => Date.now());
    useEffect(() => {
        const timer = window.setInterval(() => setNow(Date.now()), 1000);
        return () => window.clearInterval(timer);
    }, []);

    const data = values[parameterKey];
    if (!data) {
        return { data: undefined, receiving: false, ageSeconds: null };
    }
    const ageMs = Math.max(0, now - data.receivedAt);
    return {
        data,
        receiving: connection === "connected" && ageMs <= STALE_AFTER_MS,
        ageSeconds: Math.round(ageMs / 1000),
    };
}