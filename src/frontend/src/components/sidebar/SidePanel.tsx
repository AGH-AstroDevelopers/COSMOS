import { useState } from "react";

import SearchBox from "./SearchBox";
import ToggleList from "./ToggleLists";
import Checkboxes from "./Checkboxes";
import { telemetryConfig} from "../widgets/telemetryConfig";
import "./SidePanel.css";

type SidePanelProps = {
    sidebarOpen: boolean;
    setSidebarOpen: (value: boolean) => void;
    selectedWidgets: Set<string>;
    setSelectedWidgets: React.Dispatch<React.SetStateAction< Set<string> >>;
}

function SidePanel(arg: SidePanelProps){
    const [search,setSearch] = useState("");

    const filteredSubsystems = telemetryConfig.filter( subsystem => {
        const subsystemMatches = subsystem.name.toLowerCase().includes(search.toLowerCase());
        const parametersMatches= subsystem.parameters.some (parameter => 
            parameter.name.toLowerCase().includes(search.toLowerCase()) 
        );
        return subsystemMatches || parametersMatches;    
    });
    return(
        <div>
            <button className={`openBar ${arg.sidebarOpen ? "open" : "closed"}`} onClick={()=> arg.setSidebarOpen(!arg.sidebarOpen)}>
                {arg.sidebarOpen ? "-" : "+"} 
            </button>
    
            <aside className={`sidebarContent ${arg.sidebarOpen ? "open" : "closed"}`}>
                <SearchBox search={search} setSearch={setSearch}/>
                <div className="widgetTree">
                    {filteredSubsystems.map(subsystem => (
                        <ToggleList
                            key={subsystem.id}
                            title={subsystem.name}>
                            {subsystem.parameters.map(parameter => (
                                <ToggleList
                                    key={parameter.id}
                                    title={parameter.name}>
                                    <Checkboxes
                                        subsystem={subsystem}
                                        parameter={parameter}
                                        selectedWidgets={arg.selectedWidgets}
                                        setSelectedWidgets={arg.setSelectedWidgets}/>
                                </ToggleList>
                            ))}
                        </ToggleList>
                    ))}
                </div>
            </aside>
        </div>
    );
}

export default SidePanel;