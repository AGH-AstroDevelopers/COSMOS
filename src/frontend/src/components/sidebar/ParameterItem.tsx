import "./SidePanel.css";
import { useState, type Dispatch, type SetStateAction } from "react";
/*Responsible for the logic and expansion of a single parameter received from the SubsystemItem*/

type ParameterItemProp = {
    id: string;
    name: string;
    visualizations: string[];
    selectedWidgets: Set<string>;
    setSelectedWidgets: Dispatch<SetStateAction<Set<string>>>;
}

function ParameterItem(arg: ParameterItemProp){
    const [isOpen,setIsOpen] = useState(false);

    function handleWidgetClick(visualization: string){
        const widgetId=`${arg.id}-${visualization}`
        arg.setSelectedWidgets(prev =>{
            const next = new Set(prev);
            if(next.has(widgetId)){
                next.delete(widgetId);
            }else{
                next.add(widgetId);
            }
            return next;
        })
    }

    return(
        <div>
            <button className="parameterButton" onClick={() => setIsOpen(!isOpen)}>
                <span className={`arrow ${isOpen ? "open" : ""}`}> ▶ </span> {arg.name}
            </button>
            
            {isOpen && (
                <div className="visualizationList">
                    { arg.visualizations.map(visualization =>(
                        <label key={visualization}>
                            <input type="checkbox"  
                            onChange={() => handleWidgetClick(visualization)}/>
                            {visualization}
                        </label>
                    ))}
                </div>
            )}
        </div>
    );
}
export default ParameterItem;