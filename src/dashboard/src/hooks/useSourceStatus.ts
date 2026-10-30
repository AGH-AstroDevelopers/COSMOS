import { useContext, useEffect, useState } from "react";
import { TelemetryContext } from "../context/TelemetryContext";
import { STALE_AFTER_MS } from "./useParameterData";

// Is the selected source sending anything right now?
// True when ANY parameter of this source arrived recently and the server connection is up.
// (A source posts packets over HTTP, there is no permanent connection to "see",
// so "connected" here means "sending data".)
export function useSourceStatus(): { sourceId: string | null; sending: boolean } {
    const { values, connection, sourceId } = useContext(TelemetryContext);

    // 1 s clock tick: silence has to be noticed even when no new data arrives.
    const [now, setNow] = useState(() => Date.now());
    useEffect(() => {
        const timer = window.setInterval(() => setNow(Date.now()), 1000);
        return () => window.clearInterval(timer);
    }, []);

    if (!sourceId || connection !== "connected") return { sourceId, sending: false };

    let latest = 0; // newest receivedAt among parameters of this source
    for (const entry of Object.values(values)) {
        if (entry.source === sourceId && entry.receivedAt > latest) latest = entry.receivedAt;
    }
    return { sourceId, sending: latest > 0 && now - latest <= STALE_AFTER_MS };
}