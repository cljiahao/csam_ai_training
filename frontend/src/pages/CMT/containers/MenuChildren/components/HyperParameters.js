import React, { useContext } from "react";
import { TbRefresh } from "react-icons/tb";
import { AppContext } from "../../../../../contexts/context";

import Input from "../../../../../containers/common/Input";
import DropBox from "../../../../../containers/common/DropBox";
import Button from "../../../../../containers/common/Button";

const HyperParameters = ({ refresh }) => {
  const { drop, setDrop, parameters, setParameters } = useContext(AppContext);

  const set_parameters = (e) => {
    setDrop((prevDrop) => ({
      ...prevDrop,
      [e.target.name]: { ...prevDrop[e.target.name], selected: e.target.value },
    }));
    if (Object.keys(parameters).includes(e.target.name)) {
      setParameters({ ...parameters, [e.target.name]: e.target.value });
    } else {
      const value =
        e.target.type === "checkbox" ? e.target.checked : e.target.value;
      setParameters({
        ...parameters,
        callbacks: {
          ...parameters.callbacks,
          [e.target.name]: value,
        },
      });
    }
  };

  const button_info = {
    name: "Refresh",
    icon: <TbRefresh />,
    onClick: () => refresh(),
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
      name: "ReduceLROnPlateau",
      type: "checkbox",
      default: true,
      onChange: set_parameters,
    },
  };

  return (
    <div className="m-3 space-y-1 rounded-xl bg-amber-100 py-3 2xl:space-y-2 2xl:py-5">
      <div className="flex-center px-3">
        <DropBox
          folder_name={"model"}
          drop={drop.model.list}
          onChange={set_parameters}
          selected={drop.model.selected}
        />
        <div className="flex-center h-14">
          <Button button_info={button_info} length={4} />
        </div>
      </div>
      <div className="grid w-full grid-cols-2">
        {Object.keys(input_dict).map((key) => (
          <Input key={key} name={key} input_info={input_dict[key]} />
        ))}
      </div>
    </div>
  );
};

export default HyperParameters;
