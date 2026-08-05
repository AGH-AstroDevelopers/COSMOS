import "./Topbar.css";

function Topbar(){
    return(
        <header className="topbar">
            <div className="leftTopbar">
                COSMOS Mission Control
            </div>
            <div className="rightTopbar">
                <span className="AstroDevelopers">AstroDevelopers</span>
                <div className="topbarButtons">
                    <button>☀</button>
                    <button>Save</button>
                    <button>Layouts ▾</button>
                </div>
            </div>
        </header>
    );
}

export default Topbar;