import React from "react";
import { Layout, Menu, Breadcrumb } from "antd";
import "./App.css";

import SideBar from "./components/sidebar/sidebar";
import TopBar from "./components/topbar/TopBar";
// import { Route, Switch } from "react-router-dom";
import { HashRouter, BrowserRouter, Route, Switch } from "react-router-dom";
import DashBoard from "./components/dashboard/Dashboard";
import HomeFilled from "@ant-design/icons";
import Backlist from "./components/backlist/Backlist";
import PaperTrade from "./components/paperTrade/PaperTrade";
import { Socket } from "socket.io-client";
import SignIn from "./components/authenticate/signIn";
import SignUp from "./components/authenticate/signUp";
import LiveTrade from "./components/Livetrade/LiveTrade";
import LoginTopBar from "./components/logintopbar/loginTopbar";
import CreateStrategy from "./components/createStrategy/CreateStrategy";
import Homepage from "./components/homepage/homepage";
import Profile from "./components/profile/profile";
import Brokers from "./components/brokers/Broker";
const { Header, Content } = Layout;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collapsed: false,
      authen: false,
      darkmode: "darkmode",
      username:undefined,
      firstname:'',
    };
    // this.onAuthenticate = this.onAuthenticate.bind(this);
  }

  onCollapse = (collapsed) => {
    console.log(collapsed);
    this.setState({ collapsed });
  };

  onAuthenticate = (value) => {
    console.log(value, "value");
    this.setState({ authen: value });
  };

  toogleTheme = () => {
    console.log("Toogling theme!");
    this.setState(
      (prevState) => {
        return {
          darkmode:
            prevState.darkmode === "darkmode" ? "lightmode" : "darkmode",
        };
      },
      function () {
        console.log(this.state.darkmode);
      }
    );
  };

  render() {
    // console.log(this.state.authen, "hello");
    const usernameChange=(val1,val2)=>{
      console.log(val1,val2)
      this.setState({ username: val1,firstname:val2 });
    }
    return (
      <>
        {this.state.authen ? (
          <>
            {/* <Layout className={this.state.darkmode}> */}
            {/* <Layout className='dashboard'> */}
            <Layout>
              <TopBar
                style={{ padding: 100 }}
                toogleTheme={this.toogleTheme}
                darkmode={this.state.darkmode}
                firstname={this.state.firstname}
              />
              <Layout
              // style={{ minHeight: "100vh" }}
              >
                <SideBar />
                <Layout className="site-layout">
                  {/* style={{backgroundColor: "#cff6cf" } */}
                  <Header
                    className="site-layout-background"
                    style={{ padding: 0 }}
                  />
                  <Content
                    style={{ marginLeft: 200, padding: "3rem" }}

                    // style={{ margin: "0 16px" }}
                  >
                    <Switch>
                      <Route
                        path={["/dashboard"]}
                        component={DashBoard}
                      ></Route>
                      <Route path="/backtest" component={Backlist}></Route>
                      <Route path="/paperTrade" component={PaperTrade}></Route>
                      <Route path="/liveTrade" component={LiveTrade}></Route>
                      <Route path="/profile" render={(props) => <Profile {...props}  user={this.state.username} />}></Route>
                      <Route path="/brokers" component={Brokers}></Route>
                      <Route
                        path="/createTrade"
                        component={CreateStrategy}
                      ></Route>
                      <Route path="/SignUp" component={SignUp}></Route>
                      <Route
                        path="/SignIn"
                        render={(props) => <SignIn {...props} auth={this.onAuthenticate}  usernameChange={usernameChange} />}
                      />

                      <Route path="/" component={DashBoard}></Route>
                    </Switch>
                  </Content>
                </Layout>
              </Layout>
            </Layout>
          </>
        ) : (
          <>
            <Layout className={this.state.darkmode}>
              {/* <Content > */}
                <Switch>
                  <Route path="/SignUp" component={SignUp}></Route>
                  <Route
                    path="/SignIn"
                    render={(props) => (
                      <SignIn {...props} auth={this.onAuthenticate}  usernameChange={usernameChange} />
                    )}
                  />
                  <Route
                    path="/"
                    render={(props) => (
                      <SignIn {...props} auth={this.onAuthenticate} usernameChange={usernameChange}  />
                    )}
                  ></Route>
                </Switch>
              {/* </Content> */}
            </Layout>
          </>
        )}
      </>
    );
  }
}

export default App;
