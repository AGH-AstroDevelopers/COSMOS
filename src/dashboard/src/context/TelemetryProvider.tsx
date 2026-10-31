import { useEffect, useState, type ReactNode } from "react";
import {TelemetryContext,type ConnectionState,type ParameterValues,type ServerEntry} from "./TelemetryContext";

const RECONNECT_DELAY_MS = 2000;

// The dashboard connects to the place it was loaded from (host AND port of the page address).
// In production that is the telemetry server itself (it serves this page).
// In development (npm run dev) Vite forwards /ws to the server, see vite.config.ts.
const SERVER_URL = `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws/connect`;

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