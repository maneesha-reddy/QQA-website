import React, { Component } from "react";
import { Card } from "antd";
import { LockTwoTone } from "@ant-design/icons";
// import Button from "@material-ui/core/Button";
// import CssBaseline from "@material-ui/core/CssBaseline";
// import TextField from "@material-ui/core/TextField";
// import FormControlLabel from "@material-ui/core/FormControlLabel";
// import Checkbox from "@material-ui/core/Checkbox";
// import Link from "@material-ui/core/Link";
import Typography from "@material-ui/core/Typography";
// import { Typography, Space } from 'antd';


import { Form, Input } from "antd";
import axios from "axios";
import { NavLink, withRouter } from "react-router-dom";
import { notification, Space } from "antd";
// import Snackbar from "@material-ui/core/Snackbar";
// import MuiAlert from "@material-ui/lab/Alert";
import { Layout, Menu, Breadcrumb, Button } from "antd";
// import LoginTopBar from "../logintopbar/loginTopbar";
import design4 from "../topbar/Design1.png";
import logo1 from "./QA-MainWhite.png";
import logo2 from "./qa-whitebackground.jpg";
const { Header, Content } = Layout;
class SignIn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      log: false,
      open: true,
     
    };
  }

  render() {
    // const { Text, Link } = Typography;
    const validateMessages = {
      required: "${label} is required!",
      types: {
        email: "${label} is not a valid email!",
        number: "${label} is not a valid number!",
      },
      number: {
        range: "${label} must be between ${min} and ${max}",
      },
    };
    // function Alert(props) {
    //   return <MuiAlert elevation={6} variant="filled" {...props} />;
    // }
    const handleClose = (event, reason) => {
      if (reason === "clickaway") {
        return;
      }
      this.setState({ open: false });
    };
   
    const onFinish = (values) => {
      console.log("Success:", values);
      let url = "http://127.0.0.1:8000/website/signin/";
      // let url = "https://quantqalgo.ddns.net/website/signin/";
      axios.post(url, values, {}).then((res) => {
        console.warn(res.data["sucessful"], "sc");
        this.props.auth(res.data["sucessful"]);
        this.setState({ log: res.data["sucessful"] });
        this.props.usernameChange(res.data["id"],res.data["firstname"])
        if (res.data["sucessful"] === true) {
          notification["success"]({
            message: "Sucessfully loggedin",
            duration: 3,
          });
          history.push("/dashboard");
        } else {
          notification["error"]({
            message: "Error", 
            duration: 3,
          });
        }
      });
     
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };
    const { location, history } = this.props;
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };
    return (
      <>
        {/* <LoginTopBar
          toogleTheme={this.toogleTheme}
          darkmode={this.state.darkmode}
        /> */}
        <Layout className="site-layout">
          <Header
            className="site-layout-background"
            style={{
              padding: 0,
              // background: "linear-gradient(to right, #ff4600 0%, #ffa833 100%)",
              background: "linear-gradient(to right, #e48005 0%, #082b6b 100%)"
            }}
          />
          <Content style={{ margin: "0 16px" }}>
            <Card style={{ width: 500 }} hoverable={true} bordered={false}>
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                {/* <CssBaseline /> */}
                <img
                  src={logo1}
                  style={{ height: "auto", width: "150px" }}
                  className="img-responsive"
                  alt=""
                />{" "}
                <br />
                <LockTwoTone
                  twoToneColor="#eb2f96"
                  size="large"
                  style={{ alignContent: "center" }}
                />
                <Typography component="h1" variant="h5">
                  Sign in
                </Typography>
                <br />
                <Form
                  {...layout}
                  name="basic"
                  initialValues={{ remember: true }}
                  onFinish={onFinish}
                  onFinishFailed={onFinishFailed}
                  validateMessages={validateMessages}
                >
                  <Form.Item
                    label="Email"
                    name="email"
                    rules={[
                      {
                        type: "email",
                        message: "The input is not valid E-mail!",
                      },
                      {
                        required: true,
                        message: "Please input your E-mail!",
                      },
                    ]}
                  >
                    <Input style={{ width: 200 }} />
                  </Form.Item>
                  <Form.Item
                    label="Password"
                    name="password"
                    rules={[
                      {
                        required: true,
                        message: "Please input your password!",
                      },
                    ]}
                    hasFeedback
                  >
                    <Input.Password style={{ width: 200 }} />
                  </Form.Item>

                  {/* <FormControlLabel
                    control={<Checkbox value="remember" color="primary" />}
                    label="Remember me"
                  /> */}
                  <Form.Item {...tailLayout}>
                    <Button type="primary" htmlType="submit" style={{backgroundColor:"#082b6b"}}>
                      Sign In
                    </Button>
                  </Form.Item>
                  <NavLink to="/SignUp">Don't have an account? Sign Up</NavLink>
                </Form>
              </div>
            </Card>
          </Content>
        </Layout>
      </>
    );
  }
}

export default withRouter(SignIn);
