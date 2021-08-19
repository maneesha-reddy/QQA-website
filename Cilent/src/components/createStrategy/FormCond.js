import React, { Component } from "react";
import { MinusCircleOutlined, DeleteFilled } from "@ant-design/icons";
import {
  Form,
  Select,
  Card,
  Row,
  Col,
  Divider,
  TimePicker,
  InputNumber,
  Space,
  Input,
} from "antd";
import { Radio } from "antd";

class FormCond extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entry: "Dayoftheweek",
    };
  }
  render() {
    console.log(this.props.field,"formcodfield")
    const { Option } = Select;
    const onEntryChange = (val) => {
      let temp= val.split("_");
      this.setState({ entry: temp[0] });
    };
    return (
      <Space key={this.props.field.key} align="baseline">
      {/* <Form.Item> */}
     
        <Row>
          <Form.Item
            {...this.props.field}
            name={[this.props.field.name, "logic"]}
            fieldKey={[this.props.field.fieldKey, "logic"]}
          >
            <Radio.Group>
              <Radio value={0}>Or</Radio>
              <Radio value={1}>And</Radio>
            </Radio.Group>
          </Form.Item>
        </Row>
        
        <Row>
          <Col>
            <Form.Item
              {...this.props.field}
              name={[this.props.field.name, "entry"]}
              fieldKey={[this.props.field.fieldKey, "entry"]}
            >
              {/* <Select style={{ width: 200 }} onChange={onEntryChange}>
                <Option value="Dayoftheweek">Day of the week</Option>
                <Option value="TimeOftheDay">Time of the Day</Option>
                <Option value="DaysToExprie">DaysToExprie</Option>
              </Select> */}
              <Select style={{ width: 200 }} onChange={onEntryChange}>
                {this.props.CondIndicators.map((element) => {
                  return <Option value={element}> {element}</Option>;
                })}
              </Select>
            </Form.Item>
          </Col>
          {this.state.entry === "Dayoftheweek" && (
            <Col>
              <Form.Item
                {...this.props.field}
                name={[this.props.field.name, "exit"]}
                fieldKey={[this.props.field.fieldKey, "exit"]}
              >
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
          {this.state.entry === "TimeOftheDay" && (
            <>
              <Col>
                <Form.Item
                  {...this.props.field}
                  name={[this.props.field.name, "exit"]}
                  fieldKey={[this.props.field.fieldKey, "exit"]}
                >
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
                <Form.Item
                  {...this.props.field}
                  name={[this.props.field.name, "time"]}
                  fieldKey={[this.props.field.fieldKey, "time"]}
                >
                  <TimePicker minuteStep={15} secondStep={10} />
                </Form.Item>
              </Col>
            </>
          )}
           {(this.state.entry === "RSI")|| (this.state.entry === "SuperTrend")||(this.state.entry === "CPR")&& (
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
          {(this.state.entry === "SMA")|| (this.state.entry === "ATR")|| (this.state.entry === "ADX")|| (this.state.entry === "EMA")&& (
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

          {this.state.entry === "DaysToExprie" && (
            <>
              <Col>
                <Form.Item
                  {...this.props.field}
                  name={[this.props.field.name, "exit"]}
                  fieldKey={[this.props.field.fieldKey, "exit"]}
                >
                  <Select style={{ width: 200 }}>
                    <Option value="equalTo">equalTo</Option>
                    <Option value="isBelow">isBelow</Option>
                  </Select>
                </Form.Item>
              </Col>
              <Col>
                <Form.Item
                  {...this.props.field}
                  name={[this.props.field.name, "number"]}
                  fieldKey={[this.props.field.fieldKey, "number"]}
                >
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

          <DeleteFilled
            onClick={() => this.props.remove(this.props.field.name)}
          />
        </Row>
      </Space>
     
     
    );
  }
}

export default FormCond;
