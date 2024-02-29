import React, { useContext } from "react";
import { RxCross2 } from "react-icons/rx";
import { AppContext } from "../../../../../../contexts/context";
import Gallery from "./components/Gallery/Gallery";

const Outflow = () => {
  const { outflow, setOutflow } = useContext(AppContext);

  const image_info = {
    A: [
      {
        image_path: "test",
        name: "test",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test1",
        name: "test1",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test3",
        name: "test3",
        label: "NG",
        pred: "G",
      },
    ],
    B: [
      {
        image_path: "test",
        name: "test",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test1",
        name: "test1",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test3",
        name: "test3",
        label: "NG",
        pred: "G",
      },
    ],
    C: [
      {
        image_path: "test",
        name: "test",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test1",
        name: "test1",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test3",
        name: "test3",
        label: "NG",
        pred: "G",
      },
    ],
    D: [
      {
        image_path: "test",
        name: "test",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test1",
        name: "test1",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test3",
        name: "test3",
        label: "NG",
        pred: "G",
      },
    ],
    E: [
      {
        image_path: "test",
        name: "test",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test1",
        name: "test1",
        label: "G",
        pred: "NG",
      },
      {
        image_path: "test3",
        name: "test3",
        label: "NG",
        pred: "G",
      },
    ],
  };

  return (
    <div className="absolute left-1/2 top-1/2 flex h-[95%] w-[95%] -translate-x-1/2 -translate-y-1/2 transform flex-col overflow-auto rounded-3xl bg-white">
      <div className="flex-end w-full p-2">
        <button onClick={() => setOutflow(!outflow)}>
          <RxCross2 size="1.5rem" />
        </button>
      </div>
      <div className="flex w-full flex-1 flex-col space-y-3 overflow-auto px-5 text-2xl">
        {Object.keys(image_info).map((key) => (
          <Gallery key={key} name={key} array={image_info[key]} />
        ))}
      </div>
    </div>
  );
};

export default Outflow;
