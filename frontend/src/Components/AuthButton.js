import React, { useContext } from "react"
import {ContextApp} from "../Context/reducer";

import {Button} from "react-bootstrap";
import {login} from '../Assets/Requests'

import {BrowserRouter as Router, Redirect} from 'react-router-dom';

export default function AuthButton({setValidation, credentials}) {

  const { state, dispatch } = useContext(ContextApp);

  function handleLogin(event) {
    event.preventDefault()
    login(dispatch, setValidation, credentials)
  }

  return !state.authToken ? (
    <Button
      className="mt-4" size="lg"
      variant="primary" block type="submit"
      onClick={handleLogin.bind(this)}
    >
      Войти
    </Button>

  ) : (
      <Redirect to={{
          pathname: "/",
          state: { from: "/login" }
        }} />
    )
}