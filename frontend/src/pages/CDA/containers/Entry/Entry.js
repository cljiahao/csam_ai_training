import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";

import Input from "../../../../containers/common/Input";
import DropBox from "../../../../containers/common/DropBox";
import Button from "../../../../containers/common/Button";
import { TbRefresh } from "react-icons/tb";

const Entry = ({ refresh }) => {
  const { drop, setDrop, entry, setEntry } = useContext(AppContext);

  const dropSelect = (e) => {
    setDrop((prevDrop) => ({
      ...prevDrop,
      [e.target.name]: { ...prevDrop[e.target.name], selected: e.target.value },
    }));
  };

  const checkEntry = (e) => {
    const { name, type, value } = e.target;
    console.log(type, value);

    if (type === "text") {
      if (value.trim() === "") {
        setEntry({ ...entry, [name]: value }); //empty
      } else {
        setEntry({ ...entry, [name]: value.trim() }); // Not empty
      }
      console.log(type, value);
    } else if (type === "number") {
      if (
        !isNaN(value) &&
        !isNaN(parseInt(value)) &&
        parseInt(value) <= 100 &&
        parseInt(value) > 0
      ) {
        setEntry({ ...entry, [name]: value });
      }
    }
  };

  const input_dict = {
    target: {
      name: "Target",
      type: "text",
      default: entry.target,
      onChange: checkEntry,
    },
    split: {
      name: "Data Split (%)",
      type: "number",
      default: entry.split,
      onChange: checkEntry,
    },
  };

  const button_info = {
    name: "Refresh",
    icon: <TbRefresh />,
    onClick: () => refresh(),
  };

  return (
    <div className="flex flex-col">
      <div className="flex-center h-14">
        <DropBox
          folder_name={"item"}
          drop={drop.item.list}
          onChange={dropSelect}
          selected={drop.item.selected}
        />
        <div className="flex-center h-full">
          <Button button_info={button_info} length={4} />
        </div>
      </div>
      <div className="flex-center">
        {Object.keys(input_dict).map((key) => (
          <Input key={key} name={key} input_info={input_dict[key]} />
        ))}
      </div>
    </div>
  );
};

export default Entry;
