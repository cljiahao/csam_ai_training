import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";

import Input from "../../../../containers/common/Input";
import DropBox from "../../../../containers/common/DropBox";
import Button from "../../../../containers/common/Button";
import { TbRefresh } from "react-icons/tb";
import { getRandomness } from "../../utils/api_misc";

const Entry = ({ refresh }) => {
  const { drop, setDrop, entry, setEntry } = useContext(AppContext);

  const dropSelect = async (e) => {
    setDrop((prevDrop) => ({
      ...prevDrop,
      [e.target.name]: { ...prevDrop[e.target.name], selected: e.target.value },
    }));
    if (e.target.value) {
      const json = await getRandomness(e.target.value);
      setEntry({ ...entry, random: json });
    } else {
      setEntry({ ...entry, random: "0" });
    }
  };

  const checkEntry = (e) => {
    const { name, type, value } = e.target;

    if (type === "text") {
      if (value.trim() === "") {
        setEntry({ ...entry, [name]: value }); //empty
      } else {
        setEntry({ ...entry, [name]: value.trim() }); // Not empty
      }
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
    random: {
      name: "Random (%)",
      type: "text",
      default: entry.random,
      disabled: true,
      bg_color:
        Number(entry.random) === 0
          ? ""
          : Number(entry.random) < 100
            ? "bg-red-300"
            : "bg-green-300",
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
    <div className="mx-1 flex flex-col 2xl:my-2 2xl:gap-2">
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
