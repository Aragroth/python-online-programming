import React, { useEffect, useState, useContext } from 'react';
import { ContextApp } from "../Context/reducer";

import "./description.css"

let images_url = process.env.REACT_APP_BASE_URL + "/images/"

function Description() {
  let [description, setDescription] = useState({ title: "", photo: null, description: "", examples: [{ input: "", output: "" }] })

  const { state, dispatch } = useContext(ContextApp);

  useEffect(() => {
    for (let section of state.tasks) {
      for (let task of section.tasks) {
        if (task.task_uuid == state.currentTask) {
          setDescription(task)
          break
        }
      }
    }
  }, [state.currentTask])





  return (
    <div className="scroll" style={{ marginRight: 25, maxWidth: "35%", width: "100%", minWidth: 350 }}>
      <h3>{description.title}</h3>
      <hr
        style={{
          backgroundColor: "black",
          height: 0.5,
          opacity: 0.4,
          borderRadius: 10
        }}
      />

      {description.photo ? <img style={{ width: "100%", borderRadius: 7 }} src={images_url + description.photo} /> : null}
      <p style={{ lineHeight: 1.5, marginTop: 15 }}>
        {description.description.split("\n").map((item, i) => <p style={{ margin: 3 }} key={i}>{item}</p>)}
      </p>

      {description.examples.map((elem, ind) => (
        <div key={ind} style={{ paddingTop: 30 }}>
          <b>Входные данные </b>
          <div
            style={{
              backgroundColor: "#2F3129", borderRadius: 15,
              padding: 20, color: "white", lineHeight: 1.3
            }}> {elem.input.split("\n").map((item, i) => <p style={{ margin: 3 }} key={i}>{item}</p>)}
          </div>
          <b>Выходные данные</b>
          <div
            style={{
              backgroundColor: "#2F3129", borderRadius: 15,
              padding: 20, color: "white", lineHeight: 1.3
            }}>
            {elem.output.split("\n").map((item, i) => <p style={{ margin: 3 }} key={i}>{item}</p>)}
          </div>
        </div>
      ))}

    </div>

  );
}

export default Description;
