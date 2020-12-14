import React from 'react';

import Sidebar from "../Components/Sidebar"
import Editor from "../Components/Editor"

import 'bootstrap/dist/css/bootstrap.min.css';
import Description from "../Components/Description";

import "./description.css"

function App({currentTask, setCurrentTask, setAuthToken }) {

  return (
    <div style={{ display: "flex", height: "100%", width: "100vw" }}>
      <Sidebar style={{ height: "100%", display: "flex", flexDirection: "column" }}/>
      <div className="scroll" style={{ display: "flex", height: "100%", width: "100vw" }}>
       
          <Description/>
    
        <div className="scroll" style={{ margin: 20, width: "100%" }}>
          <Editor/>
        </div>
      </div>
    </div>

  );
}

export default App;
