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

  const input_dict = {
    target: {
      name: "Target",
      type: "text",
      default: entry.target,
      onChange: (e) => setEntry({ ...entry, target: e.target.value }),
    },
    split: {
      name: "Data Split (%)",
      type: "number",
      default: entry.split,
      onChange: (e) => setEntry({ ...entry, split: e.target.value }),
    },
  };

  const button_info = {
    name: "Refresh",
    icon: <TbRefresh />,
    onClick: () => refresh(),
  };

  return (
    <div className="flex">
      <div className="flex-center h-14">
        <DropBox
          folder_name={"item"}
          drop={drop.item.list}
          onChange={dropSelect}
          selected={drop.item.selected}
        />
        <div className="flex-center h-14">
          <Button button_info={button_info} length={4} />
        </div>
      </div>
    </div>
  );
};

export default Entry;
