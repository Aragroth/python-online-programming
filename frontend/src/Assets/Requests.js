import Cookies from 'universal-cookie';

import { AUTH_TOKEN_UPDATE, TASKS_ALL_UPDATE,CURRENT_TASK_UPDATE } from '../Context/actions';


const api_url = process.env.REACT_APP_BASE_URL + "/api"
const cookies = new Cookies();


export function login(dispatch, setValidation, { password, username }) {

  fetch(`${api_url}/login`, {
    method: 'post',
    headers: new Headers({
      'Authorization': 'Basic Og==',
      'Content-Type': 'application/x-www-form-urlencoded'
    }),
    body: `grant_type=password&username=${username}&password=${password}`
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => {
      if (obj.status !== 200) {
        setValidation({ valid: 0, details: obj.body.detail })
      }

      else {
        cookies.set('auth_token', obj.body['access_token'], { path: '/', sameSite: "Strict" })
        dispatch({
          type: AUTH_TOKEN_UPDATE,
          payload: {
            token: obj.body['access_token'],
          }
        })
      }
    });
}



export function logout(authToken, dispatch) {
  fetch(`${api_url}/logout`, {
    headers: new Headers({
      'Authorization': `Bearer ${authToken}`,
    }),
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => {
      if (obj.status !== 200) console.log(obj)
      else {
        cookies.remove('auth_token', { path: '/', sameSite: "Strict" });
        dispatch({
          type: AUTH_TOKEN_UPDATE,
          payload: {
            token: null,
          }
        })
      }
    });
}



export function getSnippet(setCode, authToken, test_uuid) {
  if (test_uuid === null) {
    return null
  }
  fetch(`${api_url}/snippets/${test_uuid}`, {
    headers: new Headers({
      'Authorization': `Bearer ${authToken}`,
    }),
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => {
      console.log(obj.body['code_snippet'])
      if (obj.status !== 200) console.log(obj)
      else {
        setCode(obj.body['code_snippet'])
      }
    });
}



export function saveSnippet(code, authToken, test_uuid) {
  fetch(`${api_url}/snippets/${test_uuid}`, {
    method: "post",
    headers: new Headers({
      'Authorization': `Bearer ${authToken}`,
    }),
    body: JSON.stringify({ code })
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => { if (obj.status !== 200) console.log(obj) });
}



export function runSample(code, authToken, test_uuid, setCodeCheck, setLoading, setFinalCheck) {
  setLoading(1)
  fetch(`${api_url}/check/test/${test_uuid}/sample`, {
    method: "post",
    headers: new Headers({
      'Authorization': `Bearer ${authToken}`,
    }),
    body: JSON.stringify({ code })
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => {
      if (obj.status !== 200) {
        setLoading(0) 
        setFinalCheck({detail: obj.body.detail})
      }
      else { 
        setCodeCheck(obj.body)
        setLoading(0)
      }
    });

}



export function runAll(code, authToken, test_uuid, setFinalCheck, setLoading) {
  setLoading(1)
  fetch(`${api_url}/check/test/${test_uuid}/all`, {
    method: "post",
    headers: new Headers({
      'Authorization': `Bearer ${authToken}`,
    }),
    body: JSON.stringify({ code })
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => {
      if (obj.status !== 200) {
        setFinalCheck({detail: obj.body.detail})
        setLoading(0)
        return
      }

      setFinalCheck({
        total_tests: obj.body.total_tests,
        right_tests:  obj.body.right_tests
      })
      setLoading(0)
    });
}



export function getTasks(dispatch, authToken) {

  fetch(`${api_url}/tasks`, {
    headers: new Headers({
      'Authorization': `Bearer ${authToken}`,
    }),
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => {

      if (obj.status === 200) {
        dispatch({
          type: TASKS_ALL_UPDATE,
          payload: {
            tasks: obj.body.response,
          }
        })
        console.log(obj.body.response[0].tasks[0]['task_uuid'])
        dispatch({
          type: CURRENT_TASK_UPDATE,
          payload: {
            currentTask: obj.body.response[0].tasks[0]['task_uuid'],
          }
        })
      }
    });
}



export function getDescription(setDescription, currentTask, authToken) {
  console.log(currentTask)
  fetch(`${api_url}/tasks/${currentTask}/description`, {
    headers: new Headers({
      'Authorization': `Bearer ${authToken}`,
    }),
  })
    .then(r => r.json().then(data => ({ status: r.status, body: data })))
    .then(obj => {
      if (obj.status !== 200) console.log(obj)
      else {
        console.log(obj.body.response)
        setDescription(obj.body.response)
      }
    });
}
