import SearchBox from "./SearchBox";
import WidgetTree from "./WidgetTree";

import "./SidePanel.css";
import { useState } from "react";

type SidePanelProps = {
    sidebarOpen: boolean;
    setSidebarOpen: (value: boolean) => void;
}

function SidePanel(arg: SidePanelProps){
    const [search,setSearch] = useState("");

    return(
        <div>
            <button className={`openBar ${arg.sidebarOpen ? "open" : "closed"}`} onClick={()=> arg.setSidebarOpen(!arg.sidebarOpen)}>
                {arg.sidebarOpen ? "-" : "+"} 
            </button>
    
            <aside className={`sidebarContent ${arg.sidebarOpen ? "open" : "closed"}`}>
                <SearchBox search={search} setSearch={setSearch}/>
                <WidgetTree search={search}/>
            </aside>
        </div>
    );
}

export default SidePanel;