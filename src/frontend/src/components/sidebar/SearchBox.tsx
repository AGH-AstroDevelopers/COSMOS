import "./SidePanel.css";
import { useState } from "react";

function SearchBox(){
    const[search,setSearch] = useState("");

    return(
        <div className="searchBox">
            <input placeholder="Search widgets..." 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
        </div>
    );
}

export default SearchBox;