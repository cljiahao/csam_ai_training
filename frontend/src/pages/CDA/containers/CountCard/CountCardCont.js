import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";
import { API } from "../../../../core/config";
import CountCard from "./components/CountCard";

const CountCardCont = () => {
  const { fileCount } = useContext(AppContext);
  return (
    <div className="grid grid-flow-row grid-cols-3 gap-10 px-7 pt-2 2xl:pt-4">
      {Object.keys(fileCount).map((fol) => {
        return fileCount[fol] != null ? (
          <CountCard
            key={fol}
            src={`${API}/CDA/get_image/${fileCount[fol].file_path}`}
            title={fol}
            count={fileCount[fol].count}
          />
        ) : null;
      })}
    </div>
  );
};

export default CountCardCont;
