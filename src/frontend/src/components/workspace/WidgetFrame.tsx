import { useState, type ReactNode } from "react";
import "./Workspace.css"

type WidgetFrameProps = {
    title:string;
    chartType?: ReactNode;
}

function WidgetFrame(arg: WidgetFrameProps){
    const [locked, setLocked]= useState(false);

    return(
        <div className="widgetFrame">

            <div className="widgetHeader">
                <span className="widgetTitle"> {arg.title} </span>
                <div>
                    <button onClick={() => setLocked(!locked)}> {locked ? "🔒" :  "🔓"} </button>
                    <button>✕</button>
                </div>
            </div>

            <div className="widgetFrameBody">
                {arg.chartType}
            </div>
            
        </div>
    );
}
export default WidgetFrame;