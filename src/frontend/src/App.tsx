import Topbar from "./components/topbar/Topbar";
import { useState } from "react";

function App(){
  const[theme,setTheme] =useState("dark");
  return(
    <>
      <Topbar />
    </>
  )
}

export default App;
