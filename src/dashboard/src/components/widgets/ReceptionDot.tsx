import { useParameterData } from "../../hooks/useParameterData";
import "./widgets.css";

type ReceptionDotProps = { parameterKey: string };

// Small light in the widget header: 
// green = data of this parameter arrives from source, 
// grey = it does not
function ReceptionDot({ parameterKey }: ReceptionDotProps) {
    const { receiving, ageSeconds } = useParameterData(parameterKey);

    let tooltip = "Not receiving data";
    if (receiving) tooltip = `Receiving data (last update ${ageSeconds} s ago)`;
    else if (ageSeconds !== null) tooltip = `Not receiving data (last update ${ageSeconds} s ago)`;

    return (
        <span
            className={`receptionDot ${receiving ? "receiving" : "idle"}`}
            title={tooltip}
        />
    );
}

export default ReceptionDot;