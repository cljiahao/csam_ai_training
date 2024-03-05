import React, { useContext } from "react";
import { RxCross2 } from "react-icons/rx";
import { AppContext } from "../../../../../../contexts/context";
import Gallery from "./components/Gallery/Gallery";

const Outflow = () => {
  const { outflow, setTrigger } = useContext(AppContext);

  return (
    <div className="absolute left-1/2 top-1/2 flex h-[95%] w-[95%] -translate-x-1/2 -translate-y-1/2 transform flex-col overflow-auto rounded-3xl bg-white">
      <div className="flex-end w-full p-2">
        <button
          onClick={() =>
            setTrigger((prevTrigger) => ({
              ...prevTrigger,
              outflow: !prevTrigger.outflow,
            }))
          }
        >
          <RxCross2 size="1.5rem" />
        </button>
      </div>
      <div className="flex w-full flex-1 flex-col space-y-3 overflow-y-scroll px-5 text-lg font-semibold">
        <Gallery data={outflow.res} />
      </div>
    </div>
  );
};

export default Outflow;
