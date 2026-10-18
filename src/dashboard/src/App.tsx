import { useState, useEffect } from "react";

import Topbar from "./components/topbar/Topbar";
import SidePanel from "./components/sidebar/SidePanel";
import Workspace from "./components/workspace/Workspace";


type ColorTheme = "light" | "dark"

function App(){
  const[theme,setTheme] =useState<ColorTheme>("dark");
  const [sidebarOpen, setSidebarOpen]=useState(false);
  const [selectedWidgets, setSelectedWidgets] = useState<Set<string>>(new Set());

  useEffect(() => {
      document.documentElement.dataset.theme = theme;
      localStorage.setItem("theme",theme);
      },[theme]);


  const toggleTheme = () => {
    setTheme((currentTheme) =>
      currentTheme === "light" ? "dark" : "light",
    );
  };


  return(
    <>
      <Topbar
        theme={theme}
        onToggleTheme={toggleTheme}
      />
      <SidePanel 
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        selectedWidgets={selectedWidgets}
        setSelectedWidgets={setSelectedWidgets}
      />
      <Workspace
        sidebarOpen={sidebarOpen}
        selectedWidgets={selectedWidgets}
        setSelectedWidgets={setSelectedWidgets}
      />
    </>
  )
}

export default App;
