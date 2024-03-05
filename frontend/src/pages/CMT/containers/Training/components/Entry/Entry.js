import React, { useContext } from "react";
import { AppContext } from "../../../../../../contexts/context";

import DropBox from "../../../../../../containers/common/DropBox";
import getFileCount from "../../../../utils/getFileCount";
import { getFolderName } from "../../../../utils/getFolderName";

const Entry = () => {
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

  return (
    <div className="flex w-full flex-col gap-x-3 gap-y-3 pl-3">
      {Object.keys(drop)
        .reverse()
        .map((key) => (
          <DropBox
            key={key}
            folder_name={key}
            onChange={fileCount}
            drop={drop[key].list}
          />
        ))}
    </div>
  );
};

export default Entry;
