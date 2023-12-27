import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";
import { API } from "../../../core/config";
import CountCard from "./CountCard";

const CountCardCont = () => {
  const { settings } = useContext(AppContext);
  return (
    <div className="grid grid-flow-row grid-cols-3 gap-10 px-7">
      {Object.keys(settings.file_count).map((fol) => {
        return settings.file_count[fol] != null ? (
          <CountCard
            key={fol}
            src={`${API}/CDA/images/${settings.file_count[fol].file_path}`}
            title={fol}
            count={settings.file_count[fol].count}
          />
        ) : null;
      })}
    </div>
  );
};

export default CountCardCont;
