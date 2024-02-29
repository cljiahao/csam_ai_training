import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";

import Input from "../../../../containers/common/Input";

const Entry = () => {
  const { entry, setEntry } = useContext(AppContext);

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

  return (
    <div className="grid w-full grid-cols-2 items-center gap-x-3 gap-y-3 p-1 2xl:h-20 2xl:text-xl">
      {Object.keys(input_dict).map((key) => (
        <Input key={key} name={key} input_info={input_dict[key]} />
      ))}
    </div>
  );
};

export default Entry;
