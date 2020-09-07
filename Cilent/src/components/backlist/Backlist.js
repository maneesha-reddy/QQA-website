import React, { Component } from "react";
// import Select from '@material-ui/core/Select';
import TextField from "@material-ui/core/TextField";
import "./Backlist.css";
import { DatePicker, Radio, Space } from "antd";
import { Select } from "antd";
import { Row, Col } from "antd";
import { Modal, Button } from "antd";
import { PlusOutlined, EditOutlined } from "@ant-design/icons";
// import FirstModel from "./FirstModel";
import SecondModel from "./SecondModel";
import Result from "./Result";
// import Edit from "./Edit";
import axios from "axios";
import { Input, Form } from "antd";
import { Card } from "antd";
// import TextField from "@material-ui/core/TextField";

const { Option } = Select;
class Backlist extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stocks: {},
      results: {},
      size: "default",
      operation: undefined,
      Date: undefined,
      modal2Visible: false,
      activeName: null,
      spinner: true,
      table: false,
    };
    this.handleModalValues = this.handleModalValues.bind(this);
    this.setModal2Visible = this.setModal2Visible.bind(this);
    // this.onFinish = this.onFinish(this);
  }

  setModal2Visible(isVisible, op) {
    this.setState({ modal2Visible: isVisible, operation: op });
  }

  handleDateChange = (event) => {
    console.log("hi");
    console.log(event);
    this.setState({ Date: event });
  };
  handleModalValues(values) {
    console.log(values);
    this.setState(
      (prevState) => {
        return {
          ...prevState,
          stocks: {
            ...prevState.stocks,
            [values.name]: {
              name: values.name,
              exchange: values.exchange,
              symbols: values.symbols,
              StrikePrice: values.StrikePrice,
              segment: values.segment,
              // Strategy: values.Strategy,
            },
          },
        };
      },
      function () {
        console.log(this.state.stocks);
      }
    );
  }
  handleName = (e) => {
    console.log(e);
    this.setState({ activeName: e });
  };
  onFinish = async (values) => {
    console.log("hiiiiiiii");
    this.setState({ table: true });
    console.log(values);
    console.log(this.state.stocks[this.state.activeName]);
    console.log(this.state.activeName);
    const data = new FormData();
    data.append("symbol", this.state.stocks[this.state.activeName]["symbols"]);
    data.append("from_date", values.FromDate);
    data.append("to_date", values.ToDate);
    for (var key of data.entries()) {
      console.log(key[0] + ", " + key[1]);
    }
    let url = "http://127.0.0.1:8000/create/";
    await axios.post(url, data, {
      // receive two parameter endpoint url ,form data
    });
    // .then((res) => {
    //   // then print response status
    //   console.warn(this.state);
    // });
    axios.get("http://127.0.0.1:8000/create/").then((res) => {
      console.warn(res.data);
      this.setState({ spinner: false });
      this.setState((prevState) => {
        return {
          ...prevState,
          results: {
            ...prevState.results,
            hello: {
              Trade_start_date: res.data["Trade start date"],
              Trade_end_date: res.data["Trade end date"],
              Initial_Capital: res.data["Initial_Capital"],
              Ending_Capital: res.data["Ending_Capital"],
              Total_no_trades: res.data["Total no trades"],
              Positive_trades: res.data["Positive_trades"],
              Negative_trades: res.data["Negative_trades"],
              Total_loss: res.data["Total_loss"],
              Net_Profit: res.data["Net Profit"],
              Sharpe_ratio: res.data["Sharpe ratio"],
              CAGR: res.data["CAGR (%)"],
              Maximum_Drawdown: res.data["Maximum Drawdown (%)"],
            },
          },
        };
      });

      console.log(this.state.spinner);
    });
    // axios.get("http://127.0.0.1:8000/create/").then((res) => {
    //   console.log(res.data);
    // });
  };

  render() {
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };
    const { size } = this.state.size;
    return (
      // <div id="border" style={{ backgroundColor: "white", paddingLeft: 100 }}>
      <Row justify={"center"}>
        <Col>
          <Card
            hoverable
            // title="BackTesting"
            style={{ width: 500 }}
          >
            <Form {...layout} onFinish={this.onFinish}>
              {/* <Col span={12}> */}
              <Row>
                <Col span={20}>
                  <Form.Item
                    name="name"
                    rules={[{ required: true }]}
                    label="Name"
                  >
                    {/* <Row gutter={8}>
                  <Col span={15}> */}

                    <Select
                      showSearch
                      bordered={false}
                      style={{ width: 200 }}
                      placeholder="Name"
                      optionFilterProp="children"
                      onChange={this.handleName}
                      filterOption={(input, option) =>
                        option.children
                          .toLowerCase()
                          .indexOf(input.toLowerCase()) >= 0
                      }
                    >
                      {Object.entries(this.state.stocks).map(([key, item]) => {
                        console.log(item.name, "eorkgj");
                        return (
                          <Option key={item.name} value={item.name}>
                            {item.name}
                          </Option>
                        );
                      })}
                    </Select>
                  </Form.Item>
                </Col>

                <Col span={4}>
                  <Button
                    style={{ color: "#9ECB35" }}
                    icon={<PlusOutlined style={{ color: "white" }} />}
                    type="primary"
                    // style={{ marginLeft: 20 }}
                    onClick={() => this.setModal2Visible(true, "add")}
                  ></Button>
                  <Button
                    icon={<EditOutlined />}
                    disabled={
                      Object.keys(this.state.stocks).length >= 1 &&
                      this.state.activeName != null
                        ? false
                        : true
                    }
                    type="primary"
                    onClick={() => {
                      this.setModal2Visible(true, "edit");
                    }}
                  ></Button>
                </Col>
              </Row>

              <SecondModel
                autofill={
                  this.state.operation === "edit"
                    ? this.state.stocks[this.state.activeName]
                    : null
                }
                operation={this.state.operation}
                handleModalValues={this.handleModalValues}
                isVisible={this.state.modal2Visible}
                setModal2Visible={this.setModal2Visible}
              />

              <Form.Item
                style={{ fontWeight: "bolder" }}
                name="Strategy"
                label="Strategy"
                rules={[{ required: true, message: "" }]}
              >
                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Strategy"
                  optionFilterProp="children"
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  {["1", "2", "3"].map((element) => {
                    return <Option value={element}> {element}</Option>;
                  })}
                </Select>
              </Form.Item>

              <Form.Item
                name="Quantity"
                rules={[{ required: true }]}
                label="Quantity"
              >
                <TextField
                  id="outlined-basic"
                  label="Enter Quantity"
                  variant="outlined"
                />
              </Form.Item>
              {/* </Col> */}
              {/* <Col span={12}> */}
              <Form.Item
                name="Initial Capital"
                rules={[{ required: true }]}
                label="Initial Capital"
              >
                <TextField
                  id="outlined-basic"
                  label="Initial Capital"
                  variant="outlined"
                />
              </Form.Item>
              <Form.Item
                style={{ fontWeight: "bolder" }}
                name="Time_frame"
                label="Time_frame"
                rules={[{ required: true, message: "" }]}
              >
                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Time_frame"
                  optionFilterProp="children"
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  {[
                    "1min",
                    "5min",
                    "10min",
                    "15min",
                    "30min",
                    "1hour",
                    "4hours",
                    "1day",
                    "1 week",
                  ].map((element) => {
                    return <Option value={element}> {element}</Option>;
                  })}
                </Select>
              </Form.Item>
              <Form.Item
                name="FromDate"
                rules={[{ required: true }]}
                label="From"
              >
                <TextField
                  id="datetime-local"
                  type="datetime-local"
                  defaultValue=""
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Form.Item>
              <Form.Item name="ToDate" rules={[{ required: true }]} label="To">
                <TextField
                  id="datetime-local-2"
                  type="datetime-local"
                  defaultValue=""
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Form.Item>
              <Form.Item {...tailLayout}>
                <Button type="primary" htmlType="submit" ghost="true">
                  BackTest
                </Button>
              </Form.Item>
              {/* </Col> */}
            </Form>
          </Card>

          {this.state.table == true && (
            <Result
              results={this.state.results["hello"]}
              props={this.state.spinner}
            />
          )}
        </Col>
        <br />
        <br />
      </Row>
    );
  }
}

export default Backlist;