import React, { Component } from "react";
import { Form, Input, Button, Checkbox, Card } from "antd";
import BuildStrategy from "./BuildStrategy";
class CreateStrategy extends Component {
  constructor(props) {
    super(props);
    this.state = {
      strategyShow: false,
    };
  }
  render() {
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };

    const onFinish = (values) => {
      console.log("Success:", values);
      this.setState({ strategyShow: true });
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };
    const exchangeOptions = ["NSE", "NFO", "MCX", "Nasdaq", "Forex", "Crypto"];
    const segmentOptions = [
      "Cash",
      "Index features",
      "Index Options",
      "Stock futures",
      "StockOptions",
    ];
    function onChange(checkedValues) {
      console.log("checked = ", checkedValues);
    }
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
      },
    };
    const tailFormItemLayout = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0,
        },
        sm: {
          span: 16,
          offset: 8,
        },
      },
    };
    return (
      <>
        {this.state.strategyShow == false ? (
          <Card
            hoverable
            // title="BackTesting"
            style={{ margin: "2rem" }}
          >
            <Form
              // {...layout}
              {...formItemLayout}
              // layout="vertical"
               style={{ justifyContent: "right" }}
              name="basic"
              initialValues={{ remember: true }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
            >
              <Form.Item
                label="Email"
                name="email"
                rules={[
                  { required: true, message: "Please input your username!" },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Your Name"
                name="yourname"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Mobile number"
                name="mobile"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="What name you want to give to ur strategy"
                name="strategyname"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="which exchange"
                name="exchange"
                valuePropName="checked"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Checkbox.Group
                  options={exchangeOptions}
                  // defaultValue={["NSE"]}
                  onChange={onChange}
                />
              </Form.Item>
              <Form.Item
                label="which segment"
                name="segment"
                valuePropName="checked"
                rules={[
                  { required: true, message: "Please input your password!" },
                ]}
              >
                <Checkbox.Group
                  options={segmentOptions}
                  // defaultValue={["Cash"]}
                  onChange={onChange}
                />
              </Form.Item>

              <Form.Item {...tailFormItemLayout}>
                <Button type="primary" htmlType="submit">
                  Submit
                </Button>
              </Form.Item>
            </Form>
          </Card>
        ) : (
          <>
            <BuildStrategy />
          </>
        )}
      </>
    );
  }
}

export default CreateStrategy;
