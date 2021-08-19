import React, { Component } from "react";
import FormCond from "./FormCond";
import { MinusCircleOutlined, DeleteFilled } from "@ant-design/icons";
import {
  Form,
  Input,
  Button,
  Checkbox,
  Select,
  Card,
  Row,
  Col,
  Divider,
  TimePicker,
  InputNumber,
  Space,
} from "antd";
import { Radio } from "antd";
import { Modal } from "antd";
import { TreeSelect } from "antd";
import { PlusOutlined, EditFilled } from "@ant-design/icons";
const { TreeNode } = TreeSelect;

const ModalCond = (props) => {
  const [form] = Form.useForm();
  const { Option } = Select;
  console.log(props.entry,"entry")
  return (
    <Modal
      title="Add conditons"
      visible={props.isModalVisibleCond}
      destroyOnClose
      // onOk={this.handleOk}
      width={1000}
      onCancel={props.handleCancel}
      onOk={() => {
        form
          .validateFields()
          .then((values) => {
            form.resetFields();
            props.onModalFinishCond(values);
          })
          .catch((info) => {
            console.log("Validate Failed:", info);
          });
      }}
    >
      <Form form={form} name="basic2" layout="inline" size="large">
        <Row>
          <Col>
            <Form.Item name="entry">
              <Select style={{ width: 200 }} onChange={props.onEntryChange}>
                {props.CondIndicators.map((element) => {
                  return <Option value={element}> {element}</Option>;
                })}
              </Select>
            </Form.Item>
          </Col>

          {props.entry === "Dayoftheweek" && (
            <Col>
              <Form.Item name="exit">
                <Select style={{ width: 200 }}>
                  <Option value="Monday">Monday</Option>
                  <Option value="Tuesday">Tuesday</Option>
                  <Option value="Wednesday">Wednesday</Option>
                  <Option value="Thursday">Thursday</Option>
                  <Option value="Friday">Friday</Option>
                  <Option value="Saturday">Saturday</Option>
                </Select>
              </Form.Item>
            </Col>
          )}
          {props.entry === "TimeOftheDay" && (
            <>
              <Col>
                <Form.Item name="exit">
                  <Select style={{ width: 200 }}>
                    <Option value="equalTo">equalTo</Option>
                    <Option value="isAbove">isAbove</Option>
                    <Option value="isBelow">isBelow</Option>
                    <Option value="crossesAbove">crossesAbove</Option>
                    <Option value="crossesBelow">crossesBelow</Option>
                  </Select>
                </Form.Item>
              </Col>
              <Col>
                <Form.Item name="time">
                  <TimePicker minuteStep={15} secondStep={10} />
                </Form.Item>
              </Col>
            </>
          )}
          {props.entry === "RSI" && (
            <>
              <Col>
                <Form.Item name="exit">
                  <Select style={{ width: 200 }}>
                    <Option value="equalTo">equalTo</Option>
                    <Option value="isAbove">isAbove</Option>
                    <Option value="isBelow">isBelow</Option>
                    <Option value="crossesAbove">crossesAbove</Option>
                    <Option value="crossesBelow">crossesBelow</Option>
                  </Select>
                </Form.Item>
              </Col>
              <Col>
                <Form.Item name="value">
                  <Input placeholder="value" />
                </Form.Item>
              </Col>
            </>
          )}
          {props.entry === "SMA" && (
            <>
              <Col>
                <Form.Item name="exit">
                  <Select style={{ width: 200 }}>
                    <Option value="equalTo">equalTo</Option>
                    <Option value="isAbove">isAbove</Option>
                    <Option value="isBelow">isBelow</Option>
                    <Option value="crossesAbove">crossesAbove</Option>
                    <Option value="crossesBelow">crossesBelow</Option>
                  </Select>
                </Form.Item>
              </Col>
              <Col>
                <Form.Item label="Value" name="value">
                  <Select style={{ width: 200 }}>
                    <Option value="open">Open</Option>
                    <Option value="high">High</Option>
                    <Option value="low">Low</Option>
                    <Option value="close">Close</Option>
                  </Select>
                </Form.Item>
              </Col>
            </>
          )}

          {props.entry === "DaysToExprie" && (
            <>
              <Col>
                <Form.Item name="exit">
                  <Select style={{ width: 200 }}>
                    <Option value="equalTo">equalTo</Option>
                    <Option value="isBelow">isBelow</Option>
                  </Select>
                </Form.Item>
              </Col>
              <Col>
                <Form.Item name="number">
                  <Select style={{ width: 200 }}>
                    <Option value="1">1</Option>
                    <Option value="2">2</Option>
                    <Option value="3">3</Option>
                    <Option value="4">4</Option>
                    <Option value="5">5</Option>
                    <Option value="6">6</Option>
                  </Select>
                </Form.Item>
              </Col>
            </>
          )}
          <Form.List name="logics">
            {(fields, { add, remove }) => (
              <>
                {fields.map((field) => (
                  <FormCond
                    remove={remove}
                    field={field}
                    CondIndicators={props.CondIndicators}
                  />
                ))}

                {/* <Form.Item>
                  <Button
                    style={{ color: "#9ECB35", float: "right" }}
                    icon={<PlusOutlined style={{ color: "white" }} />}
                    size="medium"
                    shape="round"
                    type="primary"
                    // type="dashed"
                    onClick={() => add()}
                    block
                    // icon={<PlusOutlined />}
                  >
                    Add Conditions
                  </Button>
                </Form.Item> */}
                <Form.Item>
                  <Button
                    type="dashed"
                    onClick={() => add()}
                    block
                    icon={<PlusOutlined />}
                  >
                    Add Conditions
                  </Button>
                </Form.Item>
              </>
            )}
          </Form.List>
        </Row>
      </Form>
    </Modal>
  );
};
export default ModalCond;
