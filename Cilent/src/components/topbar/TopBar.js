import React from "react";
// import logo from "./logo.png";
import { Layout } from "antd";
import { NavLink } from "react-router-dom";
import { Avatar } from "antd";
import { UserOutlined, BellOutlined, BellFilled } from "@ant-design/icons";
import "./TopBar.css";
import { Select, Button } from "antd";
import design4 from "./Design1.png";
import design6 from "./Design6.png";
import logo from "./Design5.png";
import { Menu } from "antd";
import { Card } from "antd";

// import { Select } from 'antd';
// import InputLabel from '@material-ui/core/InputLabel';
// import MenuItem from '@material-ui/core/MenuItem';
// import FormControl from '@material-ui/core/FormControl';
// import Select from "@material-ui/core/Select";

import { Badge } from "antd";
const { SubMenu } = Menu;

const { Option } = Select;

const { Header } = Layout;

function handleChange(value) {
  console.log(`selected ${value}`);
}

// function TopBar(props) {
class TopBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collapsed: false,
    };
  }
  toggleCollapsed = () => {
    this.setState({
      collapsed: !this.state.collapsed,
    });
  };

  render() {
    return (
      <Header
        className="header"
        style={{ position: "fixed", zIndex: 1, width: "100%" }}
      >
        <div>
          <NavLink to="">
            {/* <img className="logo" src={logo} alt="logo"></img> */}
            <img
              src={design6}
              style={{ height: "auto", width: "200px" }}
              className="img-responsive"
              alt=""
            />{" "}
          </NavLink>

          <Badge
            className="site-badge-count-109"
            count={1}
            style={{
              backgroundColor: "#f50",
              position: "absolute",
              right: "4vh",
              // top: "2vh",
            }}
          >
            <BellFilled
              style={{
                fontSize: "25px",
                color: "#52c41a",
                position: "absolute",
                right: "4vh",
                // top: "2vh",
              }}
            />
          </Badge>
          {/* <div> */}
          <Avatar
            style={{
              backgroundColor: "#87d068",
              position: "absolute",
              right: "2vh",
              top: "2vh",
            }}
            size="large"
            icon={<UserOutlined />}
          />

          <div className="select">
            <Menu
              // defaultSelectedKeys={["1"]}
              // defaultOpenKeys={["sub1"]}
              mode="inline"
              style={{ width: 100 }}
              // theme="dark"
              // inlineCollapsed={this.state.collapsed}
            >
              <SubMenu
                key="sub1"
                title="My Account"
                style={{
                  width: 150,
                  position: "absolute",
                  top: "2.5vh",
                  right: "6vh",
                  backgroundColor: "transparent",
                  border: "transparent",
                  color: "white",
                }}
              >
                <Menu.Item key="1">
                  <NavLink to="/profile">MY PROFILE </NavLink>
                </Menu.Item>

                <Menu.Item key="2">
                  <NavLink to="/subcribe">SUBSCRIPTIONS</NavLink>
                </Menu.Item>

                <Menu.Item key="3">
                  <NavLink to="/brokers">BROKERS AND EXCHANGES </NavLink>
                </Menu.Item>

                <Menu.Item key="4">
                  <NavLink to="/invoice">INVOICE</NavLink>
                </Menu.Item>

                <Menu.Item key="5">
                  <NavLink to="/settings">SETTINGS</NavLink>
                </Menu.Item>

                <Menu.Item key="6">
                  <NavLink to="/logout">LOGOUT</NavLink>
                </Menu.Item>
              </SubMenu>
            </Menu>
          </div>

          {/* <div className="select">
          <Select
            className="dropdownbutton"
            defaultValue="My Account"
            style={{
              position: "absolute",
              top: "2.5vh",
              right: "6vh",
              backgroundColor: "transparent",
              border: "transparent",
              color: "white",
            }}
            onChange={handleChange}
          >
            <Option value="My Profile">
              {" "}
              <NavLink to="/profile">My Profile </NavLink>
            </Option>

            <NavLink to="/subscribe">
              <Option value="Subscriptions">Subscriptions</Option>
            </NavLink>
            <NavLink to="/brokers">
              <Option value="Brokersandexchanges" style={{ color: "black" }}>
                Brokers and exchanges
              </Option>
            </NavLink>
            <NavLink to="/invoice">
              <Option value="Invoice">Invoice</Option>
            </NavLink>
            <NavLink to="/settings">
              <Option value="Settings">Settings</Option>
            </NavLink>
            <Option value="Logout">Logout</Option>
          </Select>
        </div> */}
          {/* <Button
          type={props.darkmode ? "dashed" : "primary"}
          onClick={props.toogleTheme}
          style={{ position: "absolute", top: "2.5vh" }}
        >
          Dark
        </Button> */}
          {/* </div> */}
          {/* <Button onClick = {toogleTheme}>Dark mode</Button> */}
        </div>
      </Header>
    );
  }
}

// return (

//   );
// }

export default TopBar;
