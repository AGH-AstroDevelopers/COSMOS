import type { VisualizationType } from "../types/telemetry";
import ValueWidget from "./ValueWidget";
import "./widgets.css";

type WidgetRendererProps = {
    visualization: VisualizationType;
    parameterKey: string;
    unit?: string;
};

// The one place that picks the widget for a visualization type.
// TODO: New widgets (line, gauge, bar) add here
function WidgetRenderer({ visualization, parameterKey, unit }: WidgetRendererProps) {
    switch (visualization) {
        case "value":
            return <ValueWidget parameterKey={parameterKey} unit={unit} />;
        default:
            return <div className="widgetPlaceholder">"{visualization}" widget - coming soon</div>;
    }
}

export default WidgetRenderer;