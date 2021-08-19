import React from "react";
// import logo from "./logo.png";
import { Layout } from "antd";
import { NavLink } from "react-router-dom";
import { Avatar } from "antd";
import {
  UserOutlined,
  BellOutlined,
  BellFilled,
  DownOutlined,
} from "@ant-design/icons";
import "./TopBar.css";
import { Select, Button } from "antd";
import design4 from "./Design1.png";
import design6 from "./Design6.png";
import logo from "./Design5.png";
import { Menu } from "antd";
import { Card, Row, Col, Dropdown } from "antd";
import logo1 from "./QA-MainWhite.png";

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
    const menu = (
      <Menu mode="inline">
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
      </Menu>
    );

    return (
      <Header
        className="header"
        style={{ position: "fixed", zIndex: 1, width: "100%", height: "68px" }}
      >
        <Row align="middle" justify="center">
          <Col span={20} pull={1}>
            <NavLink to="">
              <img
                src={logo1}
                style={{ height: "auto", width: "200px" }}
                className="img-responsive"
                alt="logo"
              />
            </NavLink>
          </Col>
          <Col span={1} push={2} style={{ display: "flex" }}>
            <Badge
              className="site-badge-count-109"
              count={1}
              style={{
                backgroundColor: "#f50",
              }}
            >
              <BellFilled
                style={{
                  fontSize: "25px",
                  color: "#082b6b",
                }}
              />
            </Badge>
          </Col>
          <Col span={3} push={2}>
            <Dropdown overlay={menu} trigger={["click"]}>
              <Avatar
                size={80}
                style={{
                  backgroundColor: "#082b6b",
                }}
                size="large"
              >
                {this.props.firstname[0]}
              </Avatar>
            </Dropdown>
          </Col>
        </Row>
        {/* <div> */}
        {/* <div> */}

        {/* <div className="select">
           
          </div> */}

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
        {/* </div> */}
      </Header>
    );
  }
}

// return (

//   );
// }

export default TopBar;
