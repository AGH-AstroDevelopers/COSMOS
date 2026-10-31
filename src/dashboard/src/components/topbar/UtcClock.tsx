import { useEffect, useState } from "react";
import { useSourceStatus } from "../../hooks/useSourceStatus";
import "./UtcClock.css";

// Day of the year (1-366) in UTC, the way mission control screens often show it
function dayOfYear(date: Date): number {
    const startOfYear = Date.UTC(date.getUTCFullYear(), 0, 0);
    return Math.floor((date.getTime() - startOfYear) / 86_400_000);
}

/* Info block below the top bar:
 * - current UTC time (displayed to the second)
 * - source selected on the server:
 *   "-" = none selected
 *   grey = selected but not sending data
 *   green = sending data
 *
 * NOTE: The clock displays the device's local time converted to UTC.
 */
function UtcClock() {
    const [now, setNow] = useState(() => new Date());
    const { sourceId, sending } = useSourceStatus();

    useEffect(() => {
        // Ticks twice a second so a second is never skipped on screen
        const timer = window.setInterval(() => setNow(new Date()), 500);
        return () => window.clearInterval(timer);
    }, []);

    const iso = now.toISOString();           // e.g. 2026-10-26T21:45:12.345Z
    const date = iso.slice(0, 10);           // 2026-10-26
    const time = iso.slice(11, 19);          // 21:45:12

    return (
        <div className="utcClock">
            <div className="utcClockTime">{time} <span>UTC</span></div>
            <div className="utcClockDate">{date} · DOY {dayOfYear(now)}</div>
            <div className="utcClockSource">
                <span className="sourceLabel">Source:</span> {sourceId ?? "-"}
                {sourceId && <span className={`sourceDot ${sending ? "receiving" : "idle"}`} />}
            </div>
        </div>
    );
}

export default UtcClock;