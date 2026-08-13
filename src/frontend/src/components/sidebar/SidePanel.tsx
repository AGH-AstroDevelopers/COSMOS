import SearchBox from "./SearchBox";
import WidgetTree from "./WidgetTree";

import "./SidePanel.css";
import { useState } from "react";

function SidePanel(){
    const [sidebarOpen, setSidebarOpen]=useState(false);

    return(
        <div>
            <button className={`openBar ${sidebarOpen ? "open" : "closed"}`} onClick={()=> setSidebarOpen(!sidebarOpen)}>
                {sidebarOpen ? "-" : "+"} 
            </button>
    
            <aside className={`sidebarContent ${sidebarOpen ? "open" : "closed"}`}>
                <SearchBox />
                <WidgetTree/>
            </aside>
        </div>
    );
}

export default SidePanel;