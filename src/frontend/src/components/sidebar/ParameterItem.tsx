import "./SidePanel.css";
import { useState } from "react";
/*Responsible for the logic and expansion of a single parameter received from the SubsystemItem*/

type ParameterItemProp = {
    key: string;
    name: string;
    visualizations: string[];
}

function ParameterItem(arg: ParameterItemProp){
    const [isOpen,setIsOpen] = useState(false);
    return(
        <div>
            <button className="parameterButton" onClick={() => setIsOpen(!isOpen)}>
                <span className={`arrow ${isOpen ? "open" : ""}`}> ▶ </span> {arg.name}
            </button>
            
            {isOpen && (
                <div className="visualizationList">
                    { arg.visualizations.map(visualization =>(
                        <label key={visualization}>
                            <input type="checkbox" />
                            {visualization}
                        </label>
                    ))}
                </div>
            )}
        </div>
    );
}
export default ParameterItem;