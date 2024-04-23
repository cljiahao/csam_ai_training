import React, { useEffect, useRef, useState } from "react";
import { AppContext } from "../../contexts/context";

import { initialSetRange, initialTrigger } from "../../core/config";
import Header from "./containers/Header/Header";
import img_process from "./utils/img_process";

const Settings = () => {
  const [name, setName] = useState("");
  const [trigger, setTrigger] = useState(initialTrigger);
  const [range, setRange] = useState(initialSetRange);

  const batch_chip_ref = useRef({
    batch: useRef(null),
    chip: useRef(null),
  });

  useEffect(() => {
    const qty = img_process(
      trigger.image,
      range["slider"]["batch"],
      batch_chip_ref.current["batch"],
    );
    console.log(qty);
  }, [trigger, range]);

  return (
    <AppContext.Provider value={{ name, setName, trigger, setTrigger }}>
      <main className="no-scrollbar flex h-screen max-h-screen w-screen flex-col overflow-auto bg-amber-100 px-2 text-sm 2xl:text-lg">
        <Header />
        <section className="flex h-full w-full">
          {Object.keys(batch_chip_ref.current).map((key) => (
            <div
              key={key}
              className={`flex h-full flex-col py-3 ${key === "batch" ? "w-full" : "w-[60%]"}`}
            >
              <div className="h-full w-full">
                {trigger.image ? (
                  <div className="h-80 2xl:h-[550px]">
                    <canvas
                      className="h-full w-full object-contain"
                      ref={batch_chip_ref.current[key]}
                    ></canvas>
                  </div>
                ) : (
                  <div className="m-auto mx-5 h-full rounded-xl border-4 border-dashed border-gray-400 bg-gray-100" />
                )}
              </div>
              <aside className="flex-center h-full w-full">
                Work In Progress
              </aside>
            </div>
          ))}
        </section>
      </main>
    </AppContext.Provider>
  );
};

export default Settings;
