import React, {useContext} from "react";

import {ContextApp} from "../Context/reducer";


import {Route, Redirect} from 'react-router-dom';

export default ({ children, ...rest }) => {
    const {state, dispatch} = useContext(ContextApp);

    return (
      <Route
        {...rest}
        render={({ location }) =>
          state.authToken ? (
            children
          ) : (
            <Redirect
              to={{
                pathname: "/login",
                state: { from: location }
              }}
            />
          )
        }
      />
    );
  }