import React, { useContext } from "react";
import { TbRefresh } from "react-icons/tb";
import { AppContext } from "../../../../../../contexts/context";

import Button from "../../../../../../common/components/Button";
import DropBox from "../../../../../../common/components/DropBox";
import { getFolderName, getFileCount } from "../../../../utils/api_misc";

const Entry = ({ refresh }) => {
  const { drop, setDrop, parameters, setParameters, setTable } =
    useContext(AppContext);

  const fileCount = async (e) => {
    setDrop((prevDrop) => ({
      ...prevDrop,
      [e.target.name]: { ...prevDrop[e.target.name], selected: e.target.value },
    }));
    if (drop[e.target.name].list.includes(e.target.value)) {
      if (e.target.name === "item") {
        const json = await getFolderName(e.target.value);
        setDrop((prevDrop) => ({
          ...prevDrop,
          folder: { ...prevDrop.folder, list: json },
        }));
        setParameters({ ...parameters, item: e.target.value });
      } else if (e.target.name === "folder" && drop.item.selected) {
        const json = await getFileCount(drop.item.selected, e.target.value);
        setTable(json);
        setParameters({ ...parameters, folder: e.target.value });
      }
    }
  };

  const button_info = {
    name: "Refresh",
    icon: <TbRefresh />,
    style: { font: "text-xl" },
    onClick: () => refresh(),
  };

  return (
    <div className="flex-center h-full w-full flex-col pl-3">
      <div className="flex-center h-full w-full">
        <DropBox
          folder_name={"item"}
          onChange={fileCount}
          drop={drop.item.list}
          selected={drop.item.selected}
        />
      </div>
      <div className="flex-center h-full w-full">
        <DropBox
          folder_name={"folder"}
          onChange={fileCount}
          drop={drop.folder.list}
          selected={drop.folder.selected}
        />
        <div className="flex-center h-14">
          <Button button_info={button_info} />
        </div>
      </div>
    </div>
  );
};

export default Entry;
