import "./SidePanel.css";
import ParameterItem from "./ParameterItem";
import { useState, type Dispatch, type SetStateAction } from "react";

/*Responsible for the logic and development of a single subsystem received from the widget tree*/

type Parameter = {
    id: string;
    name: string;
    visualizations: string[];
};

type SubsystemItemArg = {
    name: string;
    parameters: Parameter[];
    isOpen: boolean;
    onToggle: () => void;
    selectedWidgets: Set<string>;
    setSelectedWidgets: Dispatch<SetStateAction<Set<string>>>;
}

function SubsystemItem(arg: SubsystemItemArg){
    return(
        <div>
            <button className= "subsystemButton" onClick={arg.onToggle}>   
                <span className={`arrow ${arg.isOpen ? "open" : ""}`}> ▶ </span> 
                {arg.name}
            </button>

            {arg.isOpen &&
                <div>
                    {arg.parameters.map(parameter =>(
                        <ParameterItem
                            key={parameter.id}
                            id={parameter.id}
                            name={parameter.name}
                            visualizations={parameter.visualizations}
                            selectedWidgets={arg.selectedWidgets}
                            setSelectedWidgets={arg.setSelectedWidgets}
                        />
                    ))}
                </div>
            }
        </div>
    );
}
   
export default SubsystemItem;


