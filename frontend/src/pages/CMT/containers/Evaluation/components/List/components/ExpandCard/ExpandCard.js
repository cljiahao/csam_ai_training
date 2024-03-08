import React, { useState } from "react";
import { MdExpandMore, MdExpandLess } from "react-icons/md";

import List from "../../List";

const ExpandCard = ({ name, values, preds }) => {
  const [exCard, setExCard] = useState(false);
  return (
    <div className="w-full rounded-lg border border-slate-400 py-1 pl-3 2xl:py-2">
      <div className="flex-between w-full">
        <div>{name}</div>
        <button
          className="flex-center mr-1 w-6 2xl:mr-3"
          onClick={() => setExCard(!exCard)}
        >
          {exCard ? (
            <MdExpandLess size="1.5rem" />
          ) : (
            <MdExpandMore size="1.5rem" />
          )}
        </button>
      </div>
      <div
        className={`flex w-full flex-col space-y-2 2xl:space-y-3 ${
          exCard && "pt-2"
        }`}
      >
        {exCard ? <List actual={values} predict={preds} /> : ""}
      </div>
    </div>
  );
};

export default ExpandCard;
