import React, { useContext } from "react";
import Swal from "sweetalert2";
import { TbRefresh, TbCloudDownload } from "react-icons/tb";
import { AppContext } from "../../../../../contexts/context";
import { saveAs } from "file-saver";

import DropBox from "../../../../../common/components/DropBox";
import Button from "../../../../../common/components/Button";
import { zipModel } from "../../../../../utils/api_misc";

const ModelSave = ({ refresh }) => {
  const { drop, setDrop } = useContext(AppContext);

  const set_parameters = (e) => {
    setDrop((prevZip) => ({
      ...prevZip,
      [e.target.name]: {
        ...prevZip[e.target.name],
        selected: e.target.value,
      },
    }));
  };
  const saveModel = async () => {
    const [, model_name] = drop.zip.selected.split("/");
    const resp = await zipModel(drop.zip.selected);
    if (resp.ok) {
      const blob = await resp.blob();
      saveAs(blob, `${model_name}.zip`);
    } else {
      Swal.fire({
        title: "Error",
        text: "An error occurred while saving the model. Please try again.",
        icon: "error",
        confirmButtonText: "OK",
      });
    }
  };

  const button_info = [
    {
      name: "Refresh",
      icon: <TbRefresh />,
      style: { font: "text-xl" },
      onClick: () => refresh(),
    },
    {
      name: "Save",
      icon: <TbCloudDownload />,
      style: { font: "text-xl" },
      onClick: saveModel,
    },
  ];

  return (
    <div className="flex h-full flex-col justify-end">
      <div className="m-3 flex flex-col justify-end rounded-xl bg-amber-100 py-3 2xl:space-y-2 2xl:py-5">
        <p className="text text-center">Model Zip</p>
        <div className="flex-center px-3">
          <DropBox
            folder_name={"zip"}
            drop={drop.zip.list}
            onChange={set_parameters}
            selected={drop.zip.selected}
          />
          <div className="flex-center h-14 space-x-2">
            {button_info.map((button, index) => (
              <Button key={index} button_info={button} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelSave;
