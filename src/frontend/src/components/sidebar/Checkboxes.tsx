import type { Dispatch, SetStateAction } from "react";
import type {ParameterConfig, SubsystemConfig, VisualizationType} from "../types/telemetry";
import "./SidePanel.css";

type CheckboxesProps = {
    subsystem: SubsystemConfig;
    parameter: ParameterConfig;
    selectedWidgets: Set<string>
    setSelectedWidgets: Dispatch<SetStateAction< Set<string> >>;
};

function Checkboxes({subsystem,parameter,selectedWidgets,setSelectedWidgets}: CheckboxesProps){
    
    function getWidgetId(visualization: VisualizationType) {
        return `${subsystem.id}.${parameter.id}.${visualization}`;
    }

    function isSelected(visualization: VisualizationType) {
        const widgetId = getWidgetId(visualization);
        return selectedWidgets.has(widgetId);
    }
    
    function handleClickCheckbox(visualization: VisualizationType) {
        const widgetId = getWidgetId(visualization);

        setSelectedWidgets(prev => {
            const next= new Set(prev);
            if(next.has(widgetId)){
                next.delete(widgetId);
            }else{
                next.add(widgetId);
            }
            return next;
        });
    }
    return(
        <div className="visualizationList">
            {parameter.visualizations.map(visualization => (
                <label key={visualization} className="visualizationOption">
                    <input
                        type="checkbox"
                        checked={isSelected(visualization)}
                        onChange={() => handleClickCheckbox(visualization)}
                    />
                    {visualization}
                </label>
            ))}
        </div>
    );
}
export default Checkboxes;