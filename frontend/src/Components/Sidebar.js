import React, { useEffect, useState, useContext } from 'react';

import { ProSidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import 'react-pro-sidebar/dist/css/styles.css';

import { ContextApp } from "../Context/reducer";
import { logout, getTasks } from "../Assets/Requests"


import { BiLogOut, BiHide } from 'react-icons/bi';
import { BsListTask } from 'react-icons/bs';
import { CURRENT_TASK_UPDATE } from '../Context/actions'



function Sidebar() {
  const { state, dispatch } = useContext(ContextApp);

  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    getTasks(dispatch, state.authToken)
    console.log(state.tasks)
  }, [])

  function setTask(task_uuid) {
    console.log(task_uuid)
    dispatch({
      type: CURRENT_TASK_UPDATE,
      payload: {
        currentTask: task_uuid,
      }
    })
  }


  function createMenu() {
    return state.tasks.map(
      (section, i) => (
        <SubMenu icon={<BsListTask />} key={i} title={section["_id"]}>
          {
            
            section.tasks.map(
              (item, ind) => (
                <MenuItem onClick={() => setTask(item['task_uuid'])} key={ind}>{item.short_title}</MenuItem>
              )
            )
          }
        </SubMenu>
      )
    )
  }


  return (
    <ProSidebar collapsed={collapsed}>
      <Menu iconShape="circle"  >
        <MenuItem icon={<BiLogOut />} onClick={() => logout(state.authToken, dispatch)}>
          Выйти
        </MenuItem>
        <MenuItem icon={<BiHide />} onClick={() => setCollapsed(!collapsed)}>
          Спрятать меню
        </MenuItem >

        {state.tasks.length === 0 ? <></> : createMenu()}

      </Menu>
    </ProSidebar>
  );
}

export default Sidebar;
