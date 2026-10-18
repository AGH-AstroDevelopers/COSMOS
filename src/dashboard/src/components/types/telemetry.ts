export type VisualizationType =
    | "line"
    | "gauge"
    | "value"
    | "bar";

export type ParameterType =
    | "number"
    | "boolean"
    | "enum"
    | "vector3";

export type VisualizationConfig = {
    id: VisualizationType;
    name: string;
};

export type ParameterConfig = {
    id: string;
    name: string;
    type: ParameterType;
    unit?: string;
    visualizations: VisualizationType[];
};

export type SubsystemConfig = {
    id: string;
    name: string;
    parameters: ParameterConfig[];
};

export type WidgetConfig = {
    id: string;
    subsystemId: string;
    parameterId: string;
    visualization: VisualizationType;
};