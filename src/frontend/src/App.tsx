import Topbar from "./components/topbar/Topbar";
import SidePanel from "./components/sidebar/SidePanel";
import Workspace from "./components/workspace/WidgetCanvas";
import { useState } from "react";

function App(){
  const[theme,setTheme] =useState("dark");
  const [sidebarOpen, setSidebarOpen]=useState(false);

  return(
    <>
      <Topbar />
      <SidePanel 
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />
      <Workspace sidebarOpen={sidebarOpen}/>
    </>
  )
}

export default App;
