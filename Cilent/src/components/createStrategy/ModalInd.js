import React from "react";
// import { MinusCircleOutlined, DeleteFilled } from "@ant-design/icons";
import { Form, Input, Select, Card, InputNumber } from "antd";
import { Modal } from "antd";
// import { PlusOutlined, EditFilled } from "@ant-design/icons";
const ModalInd = (props) => {
  const [form] = Form.useForm();
  const { Option } = Select;

  return (
    <Modal
      title="Add Indicator"
      destroyOnClose
      visible={props.isModalVisibleInd}
      onCancel={props.onhandleCancelInd}
      width={1000}
      onOk={() => {
        form
          .validateFields()
          .then((values) => {
            form.resetFields();
            props.onModalFinishInd(values);
          })
          .catch((info) => {
            console.log("Validate Failed:", info);
          });
      }}
    >
      <Form form={form} name="basic2" layout="inline" size="large">
        <Form.Item label="Indicator" name="indicator">
          <Select
            showSearch
            // mode="multiple"
            style={{ width: 200 }}
            placeholder="Select Indicator"
            optionFilterProp="children"
            onChange={props.onIndicatorChange}
            // onFocus={onFocus}
            // onBlur={onBlur}
            // onSearch={onSearch}
          >
            {props.indicators.map((element) => {
              return <Option value={element}> {element}</Option>;
            })}
          </Select>
        </Form.Item>
        {props.IndicatorChange === "RSI" && (
          <>
            <Form.Item label="Period" name="period">
              <Input placeholder="Enter the period" />
            </Form.Item>
            <Form.Item label="Value" name="value">
              <Select style={{ width: 200 }}>
                <Option value="open">Open</Option>
                <Option value="high">High</Option>
                <Option value="low">Low</Option>
                <Option value="close">Close</Option>
              </Select>
            </Form.Item>
          </>
        )}
        {props.IndicatorChange === "ATR" && (
          <>
            <Form.Item label="Period" name="period">
              <Input placeholder="Enter the period" />
            </Form.Item>
          </>
        )}
        {props.IndicatorChange === "SuperTrend" && (
          <>
            <Form.Item label="Period" name="period">
              <Input placeholder="Enter the period" />
            </Form.Item>
            <Form.Item label="Factor" name="factor">
              <InputNumber placeholder="Enter the factor" />
            </Form.Item>
          </>
        )}
        {props.IndicatorChange === "MACD" && (
          <>
            <Form.Item label="Period1" name="period1">
              <Input placeholder="Enter the period1" />
            </Form.Item>
            <Form.Item label="Period2" name="period2">
              <Input placeholder="Enter the period2" />
            </Form.Item>
          </>
        )}
        {props.IndicatorChange === "SMA" && (
          <>
            <Form.Item label="Period" name="period">
              <Input placeholder="Enter the period" />
            </Form.Item>
            <Form.Item label="Value" name="value">
              <Select style={{ width: 200 }}>
                <Option value="open">Open</Option>
                <Option value="high">High</Option>
                <Option value="low">Low</Option>
                <Option value="close">Close</Option>
              </Select>
            </Form.Item>
          </>
        )}
        {props.IndicatorChange === "EMA" && (
          <>
            <Form.Item label="Period" name="period">
              <Input placeholder="Enter the period" />
            </Form.Item>
            <Form.Item label="Value" name="value">
              <Select style={{ width: 200 }}>
                <Option value="open">Open</Option>
                <Option value="high">High</Option>
                <Option value="low">Low</Option>
                <Option value="close">Close</Option>
              </Select>
            </Form.Item>
          </>
        )}
        {props.IndicatorChange === "ADX" && (
          <>
            <Form.Item label="Period" name="period">
              <Input placeholder="Enter the period" />
            </Form.Item>
          </>
        )}
        <Form.Item label="Candle Interval" name="interval">
          <Select style={{ width: 200 }}>
            <Option value="5min">5min</Option>
            <Option value="15min">15min</Option>
            <Option value="30min">30min</Option>
            <Option value="1hr">1hr</Option>
            <Option value="2hr">2hr</Option>
          </Select>
        </Form.Item>
      </Form>
    </Modal>
  );
};
export default ModalInd;
