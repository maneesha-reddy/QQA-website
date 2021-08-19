import React, { Component, useEffect, useState } from "react";
import { Avatar, Card, Row, Col } from "antd";
import { Form, Input, Button, Checkbox } from "antd";
import axios from "axios";
import Typography from "@material-ui/core/Typography";
import { Statistic } from "antd";

const { Countdown } = Statistic;
const Profile = (props) => {
  const [firstname, setfirstname] = useState("");
  const [ID, setID] = useState("");
  const [lastname, setlastname] = useState("");
  const [datejoined, setdatejoined] = useState("");
  const [form] = Form.useForm();
  useEffect(() => {
    let url = "http://127.0.0.1:8000/website/profile/";
    axios.post(url, { user: props.user }, {}).then((res) => {
      console.log(res, "res");
      form.setFieldsValue({ firstname: res.data["firstname"] });
      form.setFieldsValue({ lastname: res.data["lastname"] });
      form.setFieldsValue({ email: res.data["email"] });
      form.setFieldsValue({ phone: res.data["phonenumber"] });
      form.setFieldsValue({ address: res.data["address"] });
      form.setFieldsValue({ country: res.data["country"] });
      form.setFieldsValue({ state: res.data["state"] });
      form.setFieldsValue({ description: res.data["description"] });
      setfirstname(res.data["firstname"]);
      setlastname(res.data["lastname"]);
      setID(res.data["id"]);
      setdatejoined(res.data["datejoined"]);
    });
  }, []);
  const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
  };
  const tailLayout = {
    wrapperCol: { offset: 8, span: 16 },
  };

  const onFinish = (values) => {
    console.log("Success:", { values, user: props.user });
    let url = "http://127.0.0.1:8000/website/profileUpdate/";
    // let url = "https://quantqalgo.ddns.net/website/signin/";
    axios.post(url, { values, user: props.user }, {}).then((res) => {
      console.warn(res.data["sucessful"], "sc");
    });
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <>
      <Card hoverable title="PROFILE" style={{ width: 1000 }}>
        <Row>
          <Col offset={2} span={8}>
            <Avatar size={80} gap={0} style={{ backgroundColor: "#f56a00" }}>
              {firstname[0] + lastname[0]}
            </Avatar>
            <Row gutter={16}>
              <Col span={12}>
                <Statistic title="ID" value={ID} />
              </Col>
              <Col span={24}>
                <Statistic title="Date Joined" value={datejoined} />
              </Col>
            </Row>
            ,
            {/* <Row>
              <Col span={24}>
                <Typography component="h1" variant="h5" label="ID">
                  {ID}
                </Typography>
              </Col>
              <Col span={12}>
                <Typography component="h1" variant="h5">
                  {datejoined}
                </Typography>
              </Col>
            </Row> */}
          </Col>
          <Col>
            <Form
              form={form}
              // {...layout}
              name="basic"
              layout="vertical"
              // initialValues={{
              //   firstname: this.state.firstname,
              //   lastname: this.state.lastname,
              //   email: this.state.email,
              // }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
            >
              <Row>
                <Col>
                  <Form.Item label="FirstName" name="firstname">
                    <Input disabled />
                  </Form.Item>
                </Col>
                <Col>
                  <Form.Item label="LastName" name="lastname">
                    <Input disabled />
                  </Form.Item>
                </Col>
              </Row>
              <Form.Item label="Email" name="email">
                <Input disabled />
              </Form.Item>
              <Row>
                <Col>
                  <Form.Item label="Phone" name="phone">
                    <Input />
                  </Form.Item>
                </Col>
                <Col>
                  <Form.Item label="Address" name="address">
                    <Input.TextArea />
                  </Form.Item>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Form.Item label="Country" name="country">
                    <Input />
                  </Form.Item>
                </Col>
                <Col>
                  <Form.Item label="State" name="state">
                    <Input />
                  </Form.Item>
                </Col>
              </Row>
              <Form.Item label="Description" name="description">
                <Input.TextArea />
              </Form.Item>
              <Form.Item {...tailLayout}>
                <Button type="primary" htmlType="submit">
                  Save
                </Button>
              </Form.Item>
            </Form>
          </Col>
        </Row>
      </Card>
    </>
  );
};

export default Profile;
