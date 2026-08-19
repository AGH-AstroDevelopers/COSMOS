import { useState } from "react";
import type { WidgetConfig } from "../types/telemetry";
import "./Workspace.css"

type WidgetFrameProps = {
    config: WidgetConfig;
    title: string;
    subsystemName: string;
    children: React.ReactNode;
    onRemove: () => void;
};

function WidgetFrame(arg: WidgetFrameProps){
    const [locked, setLocked]= useState(false);

    return(
        <div className="widgetFrame">

            <div className="widgetHeader">
                <div className="widgetTitle">
                    <div className="parameterName">
                        {arg.title}
                    </div>

                    <div className="subsystemName">
                        {arg.subsystemName}
                    </div>
                </div>
                <div>
                    <button onClick={() => setLocked(!locked)}> {locked ? "🔒" :  "🔓"} </button>
                    <button onClick={arg.onRemove}>✕</button>
                </div>
            </div>

            <div className="widgetFrameBody">
                {arg.children}
            </div>
            
        </div>
    );
}
export default WidgetFrame;