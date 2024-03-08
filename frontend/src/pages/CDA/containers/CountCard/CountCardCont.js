import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";
import { API } from "../../../../core/config";
import CountCard from "./components/CountCard";

const CountCardCont = () => {
  const { random } = useContext(AppContext);
  return (
    <div className="grid grid-flow-row grid-cols-3 gap-10 px-7 pt-2 2xl:pt-4">
      {Object.keys(random.count).map((fol) => {
        return random.count[fol] != null ? (
          <CountCard
            key={fol}
            src={`${API}/get_image/${random.count[fol].file_path}`}
            title={fol}
            count={random.count[fol].count}
          />
        ) : null;
      })}
    </div>
  );
};

export default CountCardCont;
