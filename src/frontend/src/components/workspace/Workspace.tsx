import ReactGridLayout, { WidthProvider } from "react-grid-layout/legacy";
import { useEffect, useState } from "react";
import type { Layout } from "react-grid-layout/legacy";

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
const GRID_COLS=12;

//Default size of an widget
const DEFAULT_W=4;
const DEFAULT_H=6;

function Workspace(arg: WorkspaceProps){    
    const[layout, setLayout]=useState<Layout>([]); //stores widget positions on dashboard
    useEffect(() => {
        setLayout(prevLayout => {
            const existingById = new Map(prevLayout.map(item => [item.i, item]));
            const widgetIds = Array.from(arg.selectedWidgets);

            return widgetIds.map((widgetId, index) => {
                const existing = existingById.get(widgetId);
                if (existing) {return existing;}
                return {
                    i: widgetId,
                    x: (index * DEFAULT_W) % GRID_COLS,
                    y: Infinity,
                    w: DEFAULT_W,
                    h: DEFAULT_H,
                };
            });
        });
    }, [arg.selectedWidgets]);

    return(
        <main className={`workspace ${arg.sidebarOpen ? "open" : ""}`}>
            {arg.selectedWidgets.size ===0 ? (
                <div className="emptyWorkspaceText">
                    Open the menu (+) on the left and select a parameter to display.
                </div>
            ): (
                <GridLayout
                    layout={layout}
                    cols={GRID_COLS}
                    rowHeight={30}
                    margin={[12, 12]}
                    containerPadding={[24, 24]}
                    onLayoutChange={setLayout}
                    draggableCancel=".widgetHeaderActions"
                >
                    {Array.from(arg.selectedWidgets).map(widgetId=>{
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
                            <div key={widgetId}>
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
                            </div>
                        );
                    })}
                </GridLayout>
            )}
        </main>
    );
}

export default Workspace;