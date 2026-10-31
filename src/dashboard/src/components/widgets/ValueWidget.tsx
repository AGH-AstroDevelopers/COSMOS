import { useParameterData } from "../../hooks/useParameterData";
import "./widgets.css";

type ValueWidgetProps = {
    parameterKey: string; // e.g. "thermal.temperature"
    unit?: string;        // unit from the catalog, used when the packet carries none
};

// Time of the packet (set by the source) as HH:MM:SS in UTC, the same time zone as the clock.
function formatTimestamp(timestamp: string): string {
    const date = new Date(timestamp);
    return Number.isNaN(date.getTime()) ? "--:--:--" : date.toISOString().slice(11, 19);
}

// Shows one number. Colour: red = critical, yellow = warning, normal text otherwise.
function ValueWidget({ parameterKey, unit }: ValueWidgetProps) {
    const { data, receiving } = useParameterData(parameterKey);

    if (!data || !receiving || data.value === null) {
        return (
            <div className="valueWidget">
                <div className="valueNumber valueEmpty">--</div>
                <div className="valueCaption">Not receiving data</div>
            </div>
        );
    }

    return (
        <div className="valueWidget">
            <div className="valueTimestamp" title={`Source time of this value: ${data.timestamp}`}>
                {formatTimestamp(data.timestamp)} UTC
            </div>
            <div className={`valueRow status-${data.status}`}>
                <span className="valueNumber">{String(data.value)}</span>
                <span className="valueUnit">{data.unit ?? unit ?? ""}</span>
            </div>
        </div>
    );
}

export default ValueWidget;