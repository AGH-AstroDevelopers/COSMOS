import { useState, type ReactNode } from "react";
import "./SidePanel.css";

type ToggleListProps = {
    title: string;
    children: ReactNode;
};

function ToggleList(arg: ToggleListProps){
    const [isOpen, setIsOpen] = useState(false);

    return(
        <div className="toggleList"> 
            <button className="toggleListButton"
                onClick={() => setIsOpen(!isOpen)}>
                
                <span className={`arrow ${isOpen ? "open" : ""}`}> ▶ </span> 
                {arg.title}
            </button>
            {isOpen && (
                <div className="toggleListContent">
                    {arg.children}
                </div>
            )}
        </div>
    );
}

export default ToggleList;