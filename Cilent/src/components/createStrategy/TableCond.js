import React, { Component } from "react";
import { DeleteFilled } from "@ant-design/icons";
import { Form, Space, Table, Input } from "antd";
import { EditFilled } from "@ant-design/icons";
import ModalCond from "./ModalCond";
class TableCond extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isModalVisibleCond: false,
      entry: "Dayoftheweek",
      row: undefined,
      originData: [
        {
          key: "1",
          Type: "EntryWhen",

          logics: [],
        },
        {
          key: "2",
          Type: "ExitWhen",
          logics: [],
        },
      ],
    };
  }
  render() {
    console.log(this.props.field, "field");
    const showModalCond = (row) => {
      // console.log(row, "row");

      this.setState({ isModalVisibleCond: true, row: row.Type });
    };
    const handleCancel = () => {
      this.setState({ isModalVisibleCond: false });
    };
    const columns = [
      {
        width: 100,
        dataIndex: "Type",
        key: "Type",
      },
      {
        width: 100,
        dataIndex: "logics",
        key: "logics",
        render: (logics) => {
          let stringShown = "";
          // console.log(logics, "llogics");
          logics.map((logic) => {
            stringShown = stringShown + logic.logic + logic.entry + logic.exit;
          });
          return stringShown;
        },
      },

      {
        key: "operation",
        render: (row) => <EditFilled onClick={() => showModalCond(row)} />,
      },
    ];
    const EditableTable = (props) => {
      // console.log(props.key);
      //   const { originData } = this.state;
      return (
        <Table
          style={{ backgroundColor: "whitesmoke" }}
          showHeader={false}
          pagination={false}
          title={() => "Case ".concat(this.props.field.key)}
          columns={columns}
          dataSource={this.state.originData}
        />
      );
    };
    const onModalFinishCond = (values) => {
      // const { originData } = this.state;s
      // console.log("ModalSuccess:", values);
      let tempData = [...this.state.originData];
      const objIndex = tempData.findIndex((obj) => obj.Type === this.state.row);
      let temp = values.logics ? values.logics : [];
      temp.splice(0, 0, { logic: 0, entry: values.entry, exit: values.exit });
      tempData[objIndex].logics = temp;
      this.setState({ originData: tempData });
      // console.log(tempData,"tempData")
      this.props.formHandle(tempData, this.props.field.key);
      this.setState({ isModalVisibleCond: false });
    };

    const onEntryChange = (val) => {
      let temp= val.split("_");
     
      this.setState({ entry: temp[0] });
    };

    return (
      <>
        <ModalCond
          isModalVisibleCond={this.state.isModalVisibleCond}
          entry={this.state.entry}
          onEntryChange={onEntryChange}
          handleCancel={handleCancel}
          onModalFinishCond={onModalFinishCond}
          conditions={this.props.conditions}
          CondIndicators={this.props.CondIndicators}
        />
        {/* <Space key={this.props.field.key}> */}
        <DeleteFilled
          onClick={() => this.props.remove(this.props.field.name)}
        />
        <Form.Item
          {...this.props.field}
          name={[this.props.field.name, "condition"]}
          fieldKey={[this.props.field.fieldKey, "condition"]}
        >
          <EditableTable />
          {/* <Input/> */}
        </Form.Item>

        {/* </Space> */}
      </>
    );
  }
}

export default TableCond;
