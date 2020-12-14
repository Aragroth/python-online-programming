import React, { useState, useContext } from 'react';
import Cookies from 'universal-cookie';

import { Form, Container } from "react-bootstrap";

import AuthButton from "../Components/AuthButton"

const cookies = new Cookies();


function Login() {

  const [validation, setValidation] = useState({ valid: 1, details: "" });
  const [credentials, setCredentials] = useState(
    { username: "", password: "" }
  );

  function handleChange(event) {
    setCredentials({
      ...credentials,
      [event.target.name]: event.target.value
    })
  }

  console.log(credentials)

  return (
    <Container style={{ paddingTop: "12%" }} className="text-center d-flex align-items-center">

      <Form style={{ width: 300, margin: "auto" }}>
        {/* <img className="mb-4" src="https://getbootstrap.com/docs/4.5/assets/brand/bootstrap-solid.svg" alt="" width="72"
          height="72" /> */}
        <h3 className="mb-4">Войти в систему</h3>
        <Form.Group>
          <Form.Control size="lg" onChange={handleChange.bind(this)}
            name="username" placeholder="Username" className="form-control login-top"
            type="text" />

          <Form.Control size="lg" className="form-control login-bottom" onChange={handleChange.bind(this)} required
            name="password" placeholder="Password"
            type="password" />

          {
            validation.valid ? null :
              <Form.Text className="small mt-1" style={{ color: "red" }}>
                {validation.details}
              </Form.Text>
          }

          <AuthButton
            setValidation={setValidation}
            credentials={credentials}
          />

        </Form.Group>
      </Form>
    </Container>

  );
}



export default Login;
