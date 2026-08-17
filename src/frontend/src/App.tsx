import Topbar from "./components/topbar/Topbar";
import SidePanel from "./components/sidebar/SidePanel";
import Workspace from "./components/workspace/Workspace";
import { useState } from "react";

function App(){
  const[theme,setTheme] =useState("dark");
  const [sidebarOpen, setSidebarOpen]=useState(false);
  const [selectedWidgets, setSelectedWidgets]= useState<Set<string>>(new Set());

  console.log(selectedWidgets);
  return(
    <>
      <Topbar />
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
