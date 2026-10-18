import "./Topbar.css";

type TopbarProps = {
    theme: ColorTheme;
    onToggleTheme: () => void;
    };

function Topbar({ theme, onToggleTheme }: TopbarProps){

    const isDark = theme === "dark";

    return(
        <header className="topbar">
            <div className="leftTopbar">
                COSMOS Mission Control
            </div>
            <div className="rightTopbar">
                <span className="AstroDevelopers">AstroDevelopers</span>
                <div className="topbarButtons">
                    <button
                    type="button"
                    onClick={onToggleTheme}
                    aria-label={isDark ? "light theme" : "dark theme"}
                    aria-pressed={isDark}
                    >
                    {isDark?"☀":"☾"}</button>
                    <button>Save</button>
                    <button>Layouts ▾</button>
                </div>
            </div>
        </header>
    );
}

export default Topbar;