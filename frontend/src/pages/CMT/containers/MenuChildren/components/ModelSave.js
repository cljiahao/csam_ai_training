import React, { useContext } from "react";
import { TbRefresh, TbCloudDownload } from "react-icons/tb";
import { AppContext } from "../../../../../contexts/context";

import DropBox from "../../../../../common/components/DropBox";
import Button from "../../../../../common/components/Button";

const ModelSave = ({ refresh }) => {
  const { drop, setDrop, parameters, setParameters } = useContext(AppContext);

  const set_parameters = (e) => {
    setDrop((prevZip) => ({
      ...prevZip,
      [e.target.name]: {
        ...prevZip[e.target.name],
        selected: e.target.value,
      },
    }));

    setParameters({ ...parameters, [e.target.name]: e.target.value });
  };
  const handleDownload = async () => {
    const modelFolder = drop.zip.selected; // Assuming this is the model name

    try {
      const response = await fetch("/zip_model/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ modelname: modelFolder }), // Ensure this matches backend expectation
      });

      if (!response.ok) {
        throw new Error("Failed to download the model");
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.setAttribute("download", `${modelFolder}.zip`); // Name the download file
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error("Error downloading the file:", error);
    }
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
      onClick: handleDownload,
    },
  ];

  return (
    <div className="flex h-full flex-col justify-end">
      <div className="m-3 flex flex-col justify-end rounded-xl bg-amber-100 py-3 2xl:space-y-2 2xl:py-5">
        <p className="text text-center">Model Zip</p>
        <div className="flex-center px-3">
          <DropBox
            folder_name={"model"}
            drop={drop.zip.list}
            onChange={set_parameters}
            selected={drop.zip.selected}
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
