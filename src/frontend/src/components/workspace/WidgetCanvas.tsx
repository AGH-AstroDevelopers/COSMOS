import "./Workspace.css";

type WorkspaceProps = {
    sidebarOpen:boolean;
};

function Workspace(arg: WorkspaceProps){
    return(
        <main className={`workspace ${arg.sidebarOpen ? "open" : ""}`}>
        </main>
    );
}

export default Workspace;