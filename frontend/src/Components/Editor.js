import React, { useEffect, useState, useContext } from "react";

import { Button, ButtonGroup, Container, Row, Col } from "react-bootstrap";
import AceEditor from "react-ace";
import Loader from "./Loader"
import { ContextApp } from "../Context/reducer";

import "ace-builds/src-noconflict/mode-java";
import "ace-builds/src-noconflict/theme-github";
import './editor.css'

import 'brace/mode/python'
import 'brace/theme/monokai'

import { getSnippet, saveSnippet, runSample, runAll } from "../Assets/Requests"

import "./description.css"

import { Preloader, ThreeDots } from 'react-preloader-icon';


let Editor = ({ currentTask }) => {

  const { state, dispatch } = useContext(ContextApp);

  const [code, setCode] = useState("")
  const [loading, setLoading] = useState(false)
  const [codeCheck, setCodeCheck] = useState({
    "stdout": "",
    "results": [{ output: "", exit_code: null, correct: 0 }],
    "status": "correct"
  })
  const [finalCheck, setFinalCheck] = useState(null)

  useEffect(() => {
    getSnippet(setCode, state.authToken, state.currentTask)
  }, [state])

  function onSave(newValue) {
    saveSnippet(code, state.authToken, state.currentTask)
  }

  console.log(loading)
  return (
    <>
      <AceEditor
        value={code}
        mode="python"
        theme="monokai"
        fontSize={18}
        width={"100%"}
        name="UNIQUE_ID_OF_DIV"
        editorProps={{ $blockScrolling: true }}
        onChange={(newValue) => setCode(newValue)}
      />
      <Container>
        <Row className="justify-content-md-center" style={{ "margin": 15 }}>

          <Col md="auto" style={{ textAlign: "center" }}>
            <ButtonGroup style={{ textAlign: "center" }}>
              <Button variant="secondary" onClick={() => onSave()}>
                Сохранить код
              </Button>

              <Button
                variant="primary"
                onClick={() => runSample(code, state.authToken, state.currentTask, setCodeCheck, setLoading, setFinalCheck)}
              >
                {
                  loading ?
                    <Preloader
                      use={ThreeDots}
                      size={60}
                      strokeWidth={6}
                      strokeColor="#fff"
                    /> : "Выполнить тесты из примеров"
                }
              </Button>

              <Button
                style={{ backgroundColor: "green" }}
                variant="secondary"
                onClick={() => { runAll(code, state.authToken, state.currentTask, setFinalCheck, setLoading) }}
              >
                Запустить все тесты
              </Button>
            </ButtonGroup>
            {finalCheck === null ?
              null :
              <div style={{marginTop: 10}}>
                {
                  finalCheck.total_tests === finalCheck.right_tests || finalCheck.detail ?
                    <div style={{ color: "green" }}><h5><b>Вы прошли задание. {finalCheck.detail}</b></h5></div> :
                    <div style={{ color: "red" }}>
                      <h5><b>
                        Всего прошло тестов: {finalCheck.total_tests}. Из них успешных: {finalCheck.right_tests}
                        </b></h5>
                    </div>
                }

              </div>
            }
          </Col>
        </Row>
      </Container>
      <div>

      </div>
      <h3>
        Вывод тестов из примеров:
      </h3>
      {
        codeCheck.results.map(
          (elem, ind) => (
            <div key={ind} className="scroll"
              style={{
                backgroundColor: "#2F3129", maxHeight: 150, borderRadius: 5, marginTop: 30,
                padding: 20, color: elem.correct ? "#0ee117" : "#fd001d", lineHeight: 1.3,
              }}
            >
              <b>{elem.output.replace(/ /g, "\u00a0").split("\n").map((item, i) => <p style={{ margin: 3 }} key={i}>{item}</p>)}</b>
              {/* <p style={{ paddingTop: 5, color: "white" }}> {elem.exit_code !== null ? "Exit code" : null} {elem.exit_code}</p> */}
            </div>
          )
        )
      }
    </>
  )
}

export default Editor