import React, { Component } from "react";
import { Avatar, Card, Row, Col, Button } from "antd";
import { ArrowRightOutlined, EditOutline, EditFilled } from "@ant-design/icons";
import { Divider } from "antd";
import { Table, Input, InputNumber, Popconfirm, Form, Typography } from "antd";
import { useState } from "react";
import { Select } from "antd";

const { Option } = Select;

function onChange(value) {
  console.log(`selected ${value}`);
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
const children = [];
for (let i = 10; i < 36; i++) {
  children.push(<Option key={i.toString(36) + i}>{i.toString(36) + i}</Option>);
}

const originData = [];
for (let i = 0; i < 4; i++) {
  originData.push({
    key: i.toString(),
    brokername: `TT paperTrading ${i}`,
    exchanges: "MCX",
    info: `Aliceblue expects the user to login ${i}`,
  });
}

const EditableCell = ({
  editing,
  dataIndex,
  title,
  inputType,
  record,
  index,
  children,
  ...restProps
}) => {
  const inputNode = inputType === "number" ? <InputNumber /> : <Input />;
  return (
    <td {...restProps}>
      {editing ? (
        <Form.Item
          name={dataIndex}
          style={{
            margin: 0,
          }}
          rules={[
            {
              required: true,
              message: `Please Input ${title}!`,
            },
          ]}
        >
          {inputNode}
        </Form.Item>
      ) : (
        children
      )}
    </td>
  );
};
const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

const Brokers = () => {
  const [managedata, setmanagedata] = useState(false);
  const [form] = Form.useForm();
  const [data, setData] = useState(originData);
  const [editingKey, setEditingKey] = useState("");

  const isEditing = (record) => record.key === editingKey;

  const edit = (record) => {
    form.setFieldsValue({
      brokername: "",
      exchanges: "",
      info: "",
      ...record,
    });
    setEditingKey(record.key);
  };

  const manage = (att) => {
    setmanagedata(att);
  };

  const cancel = () => {
    setEditingKey("");
  };

  const save = async (key) => {
    try {
      const row = await form.validateFields();
      const newData = [...data];
      const index = newData.findIndex((item) => key === item.key);

      if (index > -1) {
        const item = newData[index];
        newData.splice(index, 1, { ...item, ...row });
        setData(newData);
        setEditingKey("");
      } else {
        newData.push(row);
        setData(newData);
        setEditingKey("");
      }
    } catch (errInfo) {
      console.log("Validate Failed:", errInfo);
    }
  };

  const columns = [
    {
      title: "Brokername",
      dataIndex: "brokername",
      width: "25%",
      editable: true,
    },
    {
      title: "Exchanges",
      dataIndex: "exchanges",
      width: "15%",
      editable: true,
    },
    {
      title: "Info",
      dataIndex: "info",
      width: "40%",
      editable: true,
    },
    {
      title: "operation",
      dataIndex: "operation",
      render: (_, record) => {
        const editable = isEditing(record);
        return editable ? (
          <span>
            <a
              href="javascript:;"
              onClick={() => save(record.key)}
              style={{
                marginRight: 8,
              }}
            >
              Save
            </a>
            <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
              <a>Cancel</a>
            </Popconfirm>
          </span>
        ) : (
          <Typography.Link
            disabled={editingKey !== ""}
            onClick={() => edit(record)}
          >
            <EditFilled />
          </Typography.Link>
        );
      },
    },
  ];
  const mergedColumns = columns.map((col) => {
    if (!col.editable) {
      return col;
    }

    return {
      ...col,
      onCell: (record) => ({
        record,
        inputType: col.dataIndex === "exchanges" ? "number" : "text",
        dataIndex: col.dataIndex,
        title: col.title,
        editing: isEditing(record),
      }),
    };
  });
  const onFinish = (values: any) => {
    console.log("Success:", values);
  };

  const onFinishFailed = (errorInfo: any) => {
    console.log("Failed:", errorInfo);
  };
  return (
    <div>
      <Row gutter={16}>
        <Card style={{ width: 1000 }}>
          <Row>
            <Col span={12}>
              <h3> List of Brokers</h3>
            </Col>
            <Col span={6}>
              <Button
                type="text"
                icon={<ArrowRightOutlined />}
                onClick={() => manage(true)}
              >
                Add Broker
              </Button>
            </Col>
          </Row>
          <Divider />
          <Form form={form} component={false}>
            <Table
              components={{
                body: {
                  cell: EditableCell,
                },
              }}
              bordered
              dataSource={data}
              columns={mergedColumns}
              rowClassName="editable-row"
              pagination={{
                onChange: cancel,
              }}
            />
          </Form>
        </Card>
      </Row>
      <Row gutter={16} justify="center">
        {managedata ? (
          <Card style={{ width: 1000 }} title="Manage Brokers">
            <Form {...layout} name="basic" onFinish={onFinish}>
              <Form.Item label="Select Broker" name="Select Broker">
                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Select a person"
                  optionFilterProp="children"
                  onChange={onChange}
                  onFocus={onFocus}
                  onBlur={onBlur}
                  onSearch={onSearch}
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  <Option value="AliceBlue">Alice Blue</Option>
                  <Option value="Zerodha">Zerodha</Option>
                  <Option value="kite">Kite</Option>
                </Select>
              </Form.Item>
              <Form.Item label="Exchanges" name="Exchanges">
                <Select
                  mode="multiple"
                  allowClear
                  style={{ width: "100%" }}
                  placeholder="Please select"
                  defaultValue={["a10", "c12"]}
                  //   onChange={handleChange}
                >
                  {children}
                </Select>
              </Form.Item>
            </Form>
          </Card>
        ) : (
          <></>
        )}
      </Row>
    </div>
  );
};
export default Brokers;
