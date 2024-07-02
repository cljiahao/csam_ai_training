import React, { useEffect, useRef, useState } from "react";
import { AppContext } from "../../contexts/context";

import { iniHolder, iniRange } from "../../core/conf_settings";
import Header from "./containers/Header/Header";
import Placeholder from "./containers/Placeholder/Placeholder";
import Trackbar from "./containers/Trackbar/Trackbar";
import img_process from "./utils/img_process";
import Selection from "./containers/Selection/Selection";
import Parameters from "./containers/Parameters/Parameters";

const Settings = () => {
  const [holder, setHolder] = useState(iniHolder);
  const [range, setRange] = useState(iniRange);

  const img_ref = useRef(null);

  useEffect(() => {
    const qty = img_process(holder.image, range[holder.radio], img_ref);
    if (holder.radio === "batch" && qty && holder.quantity !== qty) {
      setHolder((prevHolder) => ({ ...prevHolder, quantity: qty }));
    }
  }, [holder, range]);

  const slider_change = (e) => {
    const batch_chip = e.target.parentNode.parentNode.id;
    const slider = e.target.id;
    let value = Number(e.target.value);
    value = 255 <= value ? 255 : value;
    setRange((prevRange) => ({
      ...prevRange,
      [batch_chip]: { ...prevRange[batch_chip], [slider]: value },
    }));
  };

  return (
    <AppContext.Provider value={{ holder, setHolder, range, setRange }}>
      <main className="no-scrollbar flex min-h-screen flex-col space-y-3 bg-amber-100 px-2 text-sm 2xl:text-lg">
        <div className="h-20 2xl:h-28">
          <Header />
        </div>
        <div className="grid h-full w-full flex-1 grid-cols-5 gap-5 py-2">
          <div className="col-span-3">
            <Placeholder image={holder.image} img_ref={img_ref} />
          </div>
          <div className="col-span-2 space-y-5 2xl:space-y-7">
            <Selection />
            <Trackbar
              id={holder.radio}
              range={range}
              onChange={slider_change}
            />
            <Parameters info={range} />
            {/* Dotter button to confirm all chips present */}
          </div>
        </div>
      </main>
    </AppContext.Provider>
  );
};

export default Settings;
