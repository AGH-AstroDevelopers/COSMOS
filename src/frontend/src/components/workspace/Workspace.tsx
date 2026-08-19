import ReactGridLayout, { WidthProvider } from "react-grid-layout/legacy";

import "./Workspace.css";
import WidgetFrame from "./WidgetFrame";
import type { WidgetConfig, SubsystemConfig, VisualizationType, ParameterConfig } from "../types/telemetry";
import { telemetryConfig } from "../widgets/telemetryConfig";

type WorkspaceProps = {
    sidebarOpen: boolean;
    selectedWidgets: Set<string>;
    setSelectedWidgets: React.Dispatch<React.SetStateAction<Set<string>>>;
};

const GridLayout = WidthProvider(ReactGridLayout);

function Workspace(arg: WorkspaceProps){
    return(
        <main className={`workspace ${arg.sidebarOpen ? "open" : ""}`}>
            {arg.selectedWidgets.size ===0 ? (
                <div className="emptyWorkspaceText">
                    Open the menu (+) on the left and select a parameter to display.
                </div>
            ): (
                Array.from(arg.selectedWidgets).map(widgetId=>{
                    const [subsystemId,parameterId,visual]=widgetId.split(".");
                    const config: WidgetConfig = {
                        id: widgetId, 
                        subsystemId, 
                        parameterId, 
                        visualization: visual as VisualizationType
                    };
                    const subsystem = telemetryConfig.find(
                        (subsystem: SubsystemConfig) => subsystem.id === subsystemId);
                    const parameter = subsystem?.parameters.find(
                        (parameter: ParameterConfig) => parameter.id === parameterId);

                    return(
                        <WidgetFrame
                            key={widgetId}
                            config={config}
                            title={parameter?.name ?? parameterId}
                            subsystemName={subsystem?.name ?? subsystemId}
                            onRemove={() => {
                                arg.setSelectedWidgets(prev => {
                                    const next = new Set(prev);
                                    next.delete(widgetId);
                                    return next;
                                });
                            }}>
                            {visual}
                        </WidgetFrame>
                    );
                })
            )}
        </main>
    );
}

export default Workspace;