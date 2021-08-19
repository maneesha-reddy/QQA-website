import React, { Component } from "react";
import { useState } from "react";
import TableCond from "./TableCond";
import { Table, Popconfirm, Typography } from "antd";
import { Space } from "antd";
import { MinusCircleOutlined, DeleteFilled } from "@ant-design/icons";
import ModalInd from "./ModalInd";
import axios from "axios";
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
} from "antd";
import { Radio } from "antd";
import { Modal } from "antd";
import { Switch, notification } from "antd";
import { TreeSelect } from "antd";
import { PlusOutlined, EditFilled } from "@ant-design/icons";
const { TreeNode } = TreeSelect;
class BuildStrategy extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // indTitles: ["Indicator", "Ind"],
      titles: [],
      indTitles: [],
      indi: [],
      IndicatorChange: "CPR",
      CondIndicators: ["Dayoftheweek", "TimeOftheDay", "DaysToExprie"],
      isModalVisibleInd: false,
      isModalVisibleCond: false,
      conditions: [],
      switchChange: "live",

      originData: [
        {
          key: "1",
          Type: "EntryWhen",
          Condition: "None",
        },
        {
          key: "2",
          Type: "ExitWhen",
          Condition: "None",
        },
      ],
    };
  }
  formRef = React.createRef();
  showModalInd = () => {
    this.setState({ isModalVisibleInd: true });
  };
  onhandleCancelInd = () => {
    this.setState({ isModalVisibleInd: false });
  };

  render() {
    const { SHOW_PARENT } = TreeSelect;
    const { Option } = Select;
    const indicators = [
      "MACD",
      "ADX",
      "EMA",
      "SMA",
      "RSI",
      "SuperTrend",
      "CPR",
      "ATR",
    ];
    const onFormChange = (form, value) => {
      console.log(value[0].title);
      console.log(this.state[`${form}`], value);
      // this.setState({ [form]: value }, function () {
      //   // console.log(formdata);
      // });
    };

    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };
    const onFinish = (values) => {
      console.log("Success:", values);
      let url = "http://127.0.0.1:8000/website/strategyBuild/";
      axios.post(url, values, {}).then((res) => {
        console.warn(res.data);
      });
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };

    function onChange(e) {
      console.log(`radio checked:${e.target.value}`);
      // this.setState({ switchChange: e.target.value})
    }
    const onSwitchChange=(val)=> {
      console.log(val);

      this.setState({ switchChange: val.target.value });
    }
    function onBlur() {
      console.log("blur");
    }

    function onFocus() {
      console.log("focus");
    }

    function onSearch(val) {
      console.log("search:", val);
    }

    const onModalFinish = (values) => {
      console.log("ModalSuccess:", values);
      this.setState({ isModalVisible: false });
    };
    const onModalFinishInd = (values) => {
      console.log("ModalSuccess:", values);
      let temp = "";
      if (values.indicator === "MACD") {
        temp = values.indicator.concat(
          "_",
          values.period1,
          "_",
          values.period2,
          "_",
          values.interval
        );
      }
      if ((values.indicator === "ADX") | (values.indicator === "ATR")) {
        temp = values.indicator.concat(
          "_",
          values.period,
          "_",
          values.interval
        );
      }
      if (
        (values.indicator === "RSI") |
        (values.indicator === "EMA") |
        (values.indicator === "SMA")
      ) {
        temp = values.indicator.concat(
          "_",
          values.period,
          "_",
          values.value,
          "_",
          values.interval
        );
      }
      if (values.indicator === "SuperTrend") {
        temp = values.indicator.concat(
          "_",
          values.period,
          "_",
          values.factor,
          "_",
          values.interval
        );
      }
      if (values.indicator === "CPR") {
        temp = values.indicator.concat("-", values.interval);
      }

      this.setState(
        {
          titles: [...this.state.titles, temp],
          indTitles: [...this.state.indTitles, values.indicator],
          indi: [...this.state.indi, [values.period, values.interval]],
          conditions: [...this.state.conditions, values.indicator],
          CondIndicators: [...this.state.CondIndicators, temp],
        },
        () => {
          console.log("Indi", this.state.indi);
          console.log("IndTitles", this.state.indTitles);
        }
      );
      this.formRef.current.setFieldsValue({
        Indicator: this.state.titles,
      });
      this.setState({ isModalVisibleInd: false });
    };

    const { indTitles, indi } = this.state;
    const tProps = {
      value: this.state.indTitles,
    };
    const onIndicatorChange = (val) => {
      console.log(val);
      this.setState({ IndicatorChange: val });
    };

    const formHandle = (tempData, k) => {
      // console.log(tempData, "diwjefij");
      let temp = this.formRef.current.getFieldValue("sights")
        ? this.formRef.current.getFieldValue("sights")
        : {};
      // console.log(temp, "temp");
      temp[k] = tempData;
      this.formRef.current.setFieldsValue({
        sights: temp,
      });
    };
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

    return (
      <Card
        hoverable
        // title="BackTesting"
        style={{ width: 900 }}
      >
        <Form
          ref={this.formRef}
          name="mainbasic"
          // labelCol={{ span: 2 }}
          // wrapperCol={{ span: 14 }}
          layout="vertical"
          // layout="inline"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
        >
          <Form.Item name="live">
            <Radio.Group onChange={onSwitchChange}>
              <Radio.Button value="live">Live</Radio.Button>
              <Radio.Button value="backtest">BackTest</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="Chart" name="chart">
            <Radio.Group onChange={onChange}>
              <Radio.Button value="candle">Candle</Radio.Button>
              <Radio.Button value="Heikinashi">Heikinashi</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Button
            style={{ float: "right",backgroundColor:"#082b6b" }}
            icon={<PlusOutlined style={{ color: "white" }} />}
            size="medium"
            shape="round"
            type="primary"
            onClick={this.showModalInd}
          >
            Add Indicator
          </Button>
          <ModalInd
            onModalFinishInd={onModalFinishInd}
            isModalVisibleInd={this.state.isModalVisibleInd}
            onhandleCancelInd={this.onhandleCancelInd}
            indicators={indicators}
            onIndicatorChange={onIndicatorChange}
            IndicatorChange={this.state.IndicatorChange}
          />

          <Form.Item label="Indicator" name="Indicator">
            <Select
              showSearch
              mode="multiple"
              style={{ width: 200 }}
              placeholder="Select Indicator"
              optionFilterProp="children"
              value={this.state.titles}
            >
              {this.state.titles.map((element) => {
                return <Option value={element}> {element}</Option>;
              })}
            </Select>
          </Form.Item>

          <h5>Conditions</h5>

          <Form.List name="sights">
            {(fields, { add, remove }) => (
              <>
                {fields.map((field) => (
                  <TableCond
                    formHandle={formHandle}
                    conditions={this.state.conditions}
                    CondIndicators={this.state.CondIndicators}
                    field={field}
                    remove={remove}
                  />
                ))}

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

          <h5>Profit/Order</h5>
          <Row>
            <Col>
              <Form.Item name="stopGain">
                <Input addonBefore="Stop Gain" suffix="%" />
              </Form.Item>
            </Col>
            <Col offset={6}>
              <Form.Item name="stopLoss">
                <Input addonBefore="Stop Loss" suffix="%" />
              </Form.Item>
            </Col>
          </Row>
          <Divider />
          <Form.Item label="Strategy Type" name="Strategy Type">
            <Radio.Group onChange={onChange}>
              <Radio.Button value="intraday">Intraday</Radio.Button>
              <Radio.Button value="positional">Positional</Radio.Button>
            </Radio.Group>
          </Form.Item>
          {this.state.switchChange === "live" ? (
            <Form.Item label="Trade during" name="TradeDuring">
              <Input.Group compact>
                <TimePicker.RangePicker style={{ width: "70%" }} />
              </Input.Group>
            </Form.Item>
          ) : (
            <Form.Item label="TradePeriod" name="tradeperiod">
              <Select style={{ width: 200 }}>
                <Option value="1">1month</Option>
                <Option value="3">3months</Option>
                <Option value="6">6months</Option>
                <Option value="12">1 year</Option>
                <Option value="24">2 years</Option>
                <Option value="36">3 years</Option>
              </Select>
            </Form.Item>
          )}

          <Form.Item label="Max Transactions" name="maxTransactions">
            <InputNumber min={1} max={10} />
          </Form.Item>
          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Card>
    );
  }
}
export default BuildStrategy;
