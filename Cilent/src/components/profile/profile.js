import React, { Component, useEffect, useState } from "react";
import { Avatar, Card, Row, Col } from "antd";
import { Form, Input, Button, Checkbox } from "antd";
import axios from "axios";
const Profile = () => {
  const [firstname, setfirstname] = useState("");
  const [ID, setID] = useState("");
  const [datejoined, setdatejoined] = useState("");
  const [form] = Form.useForm();
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/website/profile/").then((res) => {
      form.setFieldsValue({ firstname: res.data["firstname"] });
      form.setFieldsValue({ lastname: res.data["lastname"] });
      form.setFieldsValue({ email: res.data["email"] });
      setfirstname(res.data["firstname"]);
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
    console.log("Success:", values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <>
      <Card hoverable title="PROFILE" style={{ width: 1000 }}>
        <Row>
          <Col span={8}>
            <Avatar size={80} gap={4} style={{ backgroundColor: "#f56a00" }}>
              {firstname}
            </Avatar>
            <h3> {ID}</h3>
            <h3> {datejoined}</h3>
          </Col>
          <Col>
            <Form
              form={form}
              {...layout}
              name="basic"
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
                    <Input />
                  </Form.Item>
                </Col>
                <Col>
                  <Form.Item label="LastName" name="lastname">
                    <Input />
                  </Form.Item>
                </Col>
              </Row>
              <Form.Item label="Email" name="email">
                <Input />
              </Form.Item>
              <Row>
                <Col>
                  <Form.Item label="Phone" name="phone">
                    <Input />
                  </Form.Item>
                </Col>
                <Col>
                  <Form.Item label="Address" name="address">
                    <Input />
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
              <Form.Item label="Description">
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
