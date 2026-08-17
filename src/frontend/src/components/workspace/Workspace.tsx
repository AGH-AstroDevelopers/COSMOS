import "./Workspace.css";
import WidgetFrame from "./WidgetFrame";
import ReactGridLayout, { WidthProvider } from "react-grid-layout/legacy";

type WorkspaceProps = {
    sidebarOpen: boolean;
    selectedWidgets: Set<string>;
};

const GridLayout = WidthProvider(ReactGridLayout);

function Workspace(arg: WorkspaceProps){
    
    return(
        <main className={`workspace ${arg.sidebarOpen ? "open" : ""}`}>
            {arg.selectedWidgets.size ===0 ? (
                <div className="emptyWorkspaceText">
                    Open the menu (+) on the left and select a parameter to display.
                </div>) : (
                    <GridLayout>
                        {/* widgets will go here, add them by checkbox*/}
                    </GridLayout>   
            )}
        </main>
    );
}

export default Workspace;