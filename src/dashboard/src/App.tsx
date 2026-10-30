import { useState, useEffect } from "react";

import Topbar from "./components/topbar/Topbar";
import SidePanel from "./components/sidebar/SidePanel";
import Workspace from "./components/workspace/Workspace";
import UtcClock from "./components/topbar/UtcClock";
import { usePersistentState, setToArray, arrayToSet } from "./hooks/usePersistentState";

type ColorTheme = "light" | "dark"

function App(){
  const[theme,setTheme] =useState<ColorTheme>("dark");
  const [sidebarOpen, setSidebarOpen]=useState(false);
  
  // Saves which widgets are currently selected in this browser's localStorage, so they survive a page refresh
  const [selectedWidgets, setSelectedWidgets] = usePersistentState<Set<string>>("cosmos.selectedWidgets", new Set(), setToArray, arrayToSet);

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
      <UtcClock />
      <Workspace
        sidebarOpen={sidebarOpen}
        selectedWidgets={selectedWidgets}
        setSelectedWidgets={setSelectedWidgets}
      />
    </>
  )
}

export default App;
