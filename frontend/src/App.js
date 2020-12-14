import React, { useReducer } from 'react';

import './Assets/App.css';
import './Assets/Dashboard.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { ContextApp, initialState, testReducer } from "./Context/reducer";

import Login from "./Views/login"
import Tests from "./Views/tests"
import PrivateRoute from "./Assets/PrivateRoute"


function App() {
  const [state, dispatch] = useReducer(testReducer, initialState);

  return (
    <ContextApp.Provider value={{ dispatch, state }}>
      <Router>
        <Switch>
          <Route exact path="/login">
            <Login />
          </Route>
          <PrivateRoute exact path="/">
            <Tests />
          </PrivateRoute>
        </Switch>
      </Router>
    </ContextApp.Provider>
  );
}

export default App;
