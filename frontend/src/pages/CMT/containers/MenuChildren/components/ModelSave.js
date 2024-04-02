import React, { useContext } from "react";
import { TbRefresh, TbCloudDownload } from "react-icons/tb";
import { AppContext } from "../../../../../contexts/context";
import zipModel from "../../../utils/zipModel";
import Swal from "sweetalert2";

import DropBox from "../../../../../containers/common/DropBox";
import Button from "../../../../../containers/common/Button";

const ModelSave = ({ refresh }) => {
  const { drop, setDrop, parameters, setParameters } = useContext(AppContext);

  const set_parameters = (e) => {
    setDrop((prevDrop) => ({
      ...prevDrop,
      [e.target.name]: { ...prevDrop[e.target.name], selected: e.target.value },
    }));

    setParameters({ ...parameters, [e.target.name]: e.target.value });
  };

  const saveModel = async () => {
    console.log("Model selected for saving:", drop.model.selected);
    if (!drop.model.selected) {
      console.log("No model selected for zipping");
      Swal.fire({
        title: "No Model Selected",
        text: "Please select a model before saving.",
        icon: "warning",
        confirmButtonText: "OK",
      });
      return;
    }

    const modelName = drop.model.selected.replace(/^temp\//, "");

    const blob = await zipModel(modelName);
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${modelName}.zip`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const button_info = [
    {
      name: "Refresh",
      icon: <TbRefresh />,
      onClick: () => refresh(),
    },
    {
      name: "Save",
      icon: <TbCloudDownload />,
      onClick: saveModel,
    },
  ];

  return (
    <div className="flex h-full flex-col justify-end">
      <div className="m-3 flex flex-col justify-end rounded-xl bg-amber-100 py-3 2xl:space-y-2 2xl:py-5">
        <p className="text text-center">Model Zip</p>
        <div className="flex-center px-3">
          <DropBox
            folder_name={"model"}
            drop={drop.model.list}
            onChange={set_parameters}
            selected={drop.model.selected}
          />
          <div className="flex-center h-14 space-x-2">
            {button_info.map((button, index) => (
              <Button key={index} button_info={button} length={4} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelSave;
