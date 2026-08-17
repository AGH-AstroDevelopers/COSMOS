import "./SidePanel.css";
import SubsystemItem from "./SubsystemItem";
import { useState, type Dispatch, type SetStateAction } from "react";

/*Manages the entire tree data and rules. The place for adding subsystems, their parameters, and visualizations.*/
type WidgetTreeProps = {
    search: string;
    selectedWidgets: Set<string>;
    setSelectedWidgets: Dispatch<SetStateAction<Set<string>>>;
};

function WidgetTree(arg: WidgetTreeProps){
    console.log("SEARCH:", arg.search);
    const [expanded, setExpanded] = useState(new Set<string>());
    const subsystems = [
        {
            id: "thermal",
            name: "Thermal subsystem",
            parameters: [
                {
                    id: "temperature",
                    name: "Temperature",
                    visualizations: ["line", "gauge", "value", "bar"]
                },
                {
                    id: "heater",
                    name: "Heater",
                    visualizations: ["value"]
                },
                {
                    id: "status",
                    name: "Status",
                    visualizations: ["value"]
                }
            ]
        },

        {
            id: "power",
            name: "Power subsystem",
            parameters: [
                {
                    id: "voltage",
                    name: "Voltage",
                    visualizations: ["line", "gauge", "value"]
                },
                {
                    id: "current",
                    name: "Current",
                    visualizations: ["line", "gauge", "value"]
                },
                {
                    id: "battery",
                    name: "Battery",
                    visualizations: ["line", "gauge", "value", "bar"]
                }
            ]
        },

        {
            id: "adcs",
            name: "Attitude system (ADCS)",
            parameters: [
                {
                    id: "roll",
                    name: "Roll",
                    visualizations: ["line", "gauge", "value"]
                },
                {
                    id: "pitch",
                    name: "Pitch",
                    visualizations: ["line", "gauge", "value"]
                },
                {
                    id: "yaw",
                    name: "Yaw",
                    visualizations: ["line", "gauge", "value"]
                }
            ]
        },

        {
            id: "obc",
            name: "On-board computer",
            parameters: [
                {
                    id: "cpu",
                    name: "CPU usage",
                    visualizations: ["line", "gauge", "value"]
                },
                {
                    id: "memory",
                    name: "Memory usage",
                    visualizations: ["line", "gauge", "value"]
                },
                {
                    id: "status",
                    name: "System status",
                    visualizations: ["value"]
                }
            ]
        }
    ];
    const filteredSubsystems = subsystems.filter( subsystem => {
        const subsystemMatches = subsystem.name.toLowerCase().includes(arg.search.toLowerCase());
        const parametersMatches= subsystem.parameters.some (parameter => 
            parameter.name.toLowerCase().includes(arg.search.toLowerCase()) 
        );
        return subsystemMatches || parametersMatches;    
    });

    function toggle(id: string) {
        setExpanded(prev => {
            const next = new Set(prev);
            if (next.has(id)) {
                next.delete(id);
            } else {
                next.add(id);
            }
            return next;
        });
    }

    return(
        <div className="widgetTree"> 
            { filteredSubsystems.map( subsystem => (
                <SubsystemItem
                    key={subsystem.id}
                    name={subsystem.name}
                    parameters={subsystem.parameters}
                    isOpen={expanded.has(subsystem.id)}
                    onToggle = {() => toggle(subsystem.id)}
                    selectedWidgets={arg.selectedWidgets}
                    setSelectedWidgets ={arg.setSelectedWidgets}
                />
            ))}
        </div>
    );
}

export default WidgetTree;