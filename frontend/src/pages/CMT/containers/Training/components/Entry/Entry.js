import React, { useContext } from "react";
import { AppContext } from "../../../../../../contexts/context";

import DropBox from "../../../../../../containers/common/DropBox";
import getFileCount from "../../../../utils/getFileCount";
import Input from "../../../../../../containers/common/Input";

const Entry = () => {
  const { drop, parameters, setParameters, setTable } = useContext(AppContext);

  const set_parameters = (e) => {
    if (Object.keys(parameters).includes(e.target.name)) {
      setParameters({ ...parameters, [e.target.name]: e.target.value });
    } else {
      const value =
        e.target.type === "checkbox" ? e.target.checked : e.target.value;
      setParameters({
        ...parameters,
        callbacks: {
          ...parameters["callbacks"],
          [e.target.name]: value,
        },
      });
    }
  };

  const input_dict = {
    epochs: {
      name: "Epochs",
      type: "text",
      default: parameters.epochs,
      onChange: set_parameters,
    },
    early: {
      name: "Early Stopping",
      type: "checkbox",
      default: true,
      onChange: set_parameters,
    },
    reducelr: {
      name: "ReduceLR OnPlateau",
      type: "checkbox",
      default: true,
      onChange: set_parameters,
    },
  };

  const fileCount = async (e) => {
    if (drop.includes(e.target.value)) {
      const json = await getFileCount(e.target.value);
      setTable(json);
      setParameters({ ...parameters, folder: e.target.value });
    }
  };

  return (
    <div className="grid w-full grid-cols-2 gap-x-3 gap-y-3 pl-3">
      <DropBox drop={drop} onChange={fileCount} />
      {Object.keys(input_dict).map((key) => (
        <Input key={key} name={key} input_info={input_dict[key]} />
      ))}
    </div>
  );
};

export default Entry;
