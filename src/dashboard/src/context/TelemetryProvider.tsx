import { useEffect, useState, type ReactNode } from "react";
import {
    TelemetryContext,
    type ConnectionState,
    type ParameterValues,
    type ServerEntry,
} from "./TelemetryContext";

// Port of the dashboard side of the telemetry server (see config.py).
const SERVER_PORT = 8082;
const RECONNECT_DELAY_MS = 2000;

// The host comes from the page address, so a dashboard opened on a tablet
// (http://<computer-ip>:5173) connects to the computer, not to the tablet itself.
const SERVER_URL = `ws://${window.location.hostname}:${SERVER_PORT}/ws/connect`;

type TelemetryProviderProps = { children: ReactNode };

export function TelemetryProvider({ children }: TelemetryProviderProps) {
    const [values, setValues] = useState<ParameterValues>({});
    const [connection, setConnection] = useState<ConnectionState>("connecting");
    const [sourceId, setSourceId] = useState<string | null>(null);

    useEffect(() => {
        let socket: WebSocket | null = null;
        let retryTimer: number | undefined;
        let stopped = false; // true after the provider is removed: no more retries

        function open() {
            setConnection("connecting");
            socket = new WebSocket(SERVER_URL);

            socket.onopen = () => setConnection("connected");

            socket.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    // The server tells which source it is connected to.
                    if (message.type === "status") {
                        setSourceId(message.source ?? null);
                        return;
                    }
                    if (message.type !== "telemetry") return;

                    // Remember WHEN this browser received each parameter.
                    const receivedAt = Date.now();
                    const incoming: ParameterValues = {};
                    for (const [key, entry] of Object.entries(message.data as Record<string, ServerEntry>)) {
                        incoming[key] = { ...entry, receivedAt, source: message.source };
                    }
                    // Merge: parameters missing in this packet keep their last value.
                    setValues((previous) => ({ ...previous, ...incoming }));
                } catch {
                    console.warn("Telemetry: cannot read message", event.data);
                }
            };

            socket.onclose = () => {
                if (stopped) return;
                setConnection("disconnected");
                setSourceId(null); // no server, so no source either
                setValues({});     // nothing shown after a reconnect may be older than the connection
                retryTimer = window.setTimeout(open, RECONNECT_DELAY_MS);
            };
        }

        open();

        // Cleanup: runs when the provider disappears.
        return () => {
            stopped = true;
            window.clearTimeout(retryTimer);
            socket?.close();
        };
    }, []);

    return (
        <TelemetryContext.Provider value={{ values, connection, sourceId }}>
            {children}
        </TelemetryContext.Provider>
    );
}