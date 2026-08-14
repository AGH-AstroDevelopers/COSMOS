import SearchBox from "./SearchBox";
import WidgetTree from "./WidgetTree";

import "./SidePanel.css";
import { useState } from "react";

function SidePanel(){
    const [sidebarOpen, setSidebarOpen]=useState(false);
    const [search,setSearch] = useState("");

    return(
        <div>
            <button className={`openBar ${sidebarOpen ? "open" : "closed"}`} onClick={()=> setSidebarOpen(!sidebarOpen)}>
                {sidebarOpen ? "-" : "+"} 
            </button>
    
            <aside className={`sidebarContent ${sidebarOpen ? "open" : "closed"}`}>
                <SearchBox search={search} setSearch={setSearch}/>
                <WidgetTree search={search}/>
            </aside>
        </div>
    );
}

export default SidePanel;