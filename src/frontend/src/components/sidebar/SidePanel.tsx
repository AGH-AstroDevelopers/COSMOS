import "./SidePanel.css";
import { useState } from "react";

function SidePanel(){
    const [sidebarOpen,setSidebarOpen]=useState(false);

    return(
        <div>
            <button className={`openBar ${sidebarOpen ? "open" : "closed"}`} onClick={()=> setSidebarOpen(!sidebarOpen)}>
                {sidebarOpen ? "-" : "+"} 
            </button>
            
            <aside className={`sidebarContent ${sidebarOpen ? "open" : "closed"}`}>
                <div className="searchBox">
                    <input placeholder="Search widgets..." />
                </div>
                <div className="widgetTree">
                    <button className="subsystemButton"> ▶  Thermal subsystem</button>
                        <div className="parameterList">
                            <button> ▶ Temperature </button>
                            <button> ▶ Heater </button>
                            <button> ▶ Status </button>
                        </div>
                    <button className="subsystemButton"> ▶  Power subsystem</button>
                    <button className="subsystemButton"> ▶  Attitude system (ADCS)</button>
                    <button className="subsystemButton"> ▶  On-board computer</button>
                </div>
            </aside>
        </div>
    );
}

export default SidePanel;