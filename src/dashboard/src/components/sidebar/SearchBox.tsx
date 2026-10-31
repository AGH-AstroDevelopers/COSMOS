import "./SidePanel.css";

type SearchBoxProps = {
    search:string;
    setSearch: (value:string) => void;
}

function SearchBox(arg: SearchBoxProps){
    return(
        <div className="searchBox">
            <input placeholder="Search widgets..." 
                value={arg.search}
                onChange={(e) => arg.setSearch(e.target.value)}
            />
        </div>
    );
}

export default SearchBox;