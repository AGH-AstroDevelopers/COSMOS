import Topbar from "./components/topbar/Topbar";
import SidePanel from "./components/sidebar/SidePanel";
import { useState } from "react";

function App(){
  const[theme,setTheme] =useState("dark");
  return(
    <>
      <Topbar />
      <SidePanel />
    </>
  )
}

export default App;
