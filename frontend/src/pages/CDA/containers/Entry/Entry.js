import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";

import InputCont from "../../../../common/components/InputCont";
import DropBox from "../../../../common/components/DropBox";
import Button from "../../../../common/components/Button";
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

  const input_info = {
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
    style: { font: "text-xl" },
    onClick: () => refresh(),
  };

  return (
    <div className="mx-1 flex flex-col 2xl:my-2 2xl:gap-2">
      <div className="flex-center text-md h-14 2xl:text-xl">
        <DropBox
          folder_name={"item"}
          drop={drop.item.list}
          onChange={dropSelect}
          selected={drop.item.selected}
        />
        <div className="flex-center h-full">
          <Button button_info={button_info} />
        </div>
      </div>
      <div className="flex-center text-md 2xl:text-xl">
        <InputCont input_info={input_info} />
      </div>
    </div>
  );
};

export default Entry;
