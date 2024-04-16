import React, { useContext } from "react";
import { TbRefresh } from "react-icons/tb";
import { MdWrongLocation } from "react-icons/md";
import { AppContext } from "../../../../contexts/context";

import Button from "../../../../common/components/Button";
import Header from "./components/Header/Header";
import List from "./components/List/List";

const Evaluation = ({ refresh }) => {
  const { drop, evaluate, setTrigger } = useContext(AppContext);

  const button_info = {
    refresh: {
      name: "Refresh",
      icon: <TbRefresh />,
      style: { font: "text-3xl" },
      onClick: () => refresh(drop.item.selected),
    },
    outflow: {
      name: "Outflow",
      icon: <MdWrongLocation />,
      style: { font: "text-3xl" },
      onClick: () =>
        setTrigger((prevTrigger) => ({
          ...prevTrigger,
          outflow: !prevTrigger.outflow,
        })),
    },
  };

  return (
    <div className="flex flex-1 flex-col overflow-auto px-3">
      <div className="flex-between h-16 w-full gap-5 px-3">
        {Object.keys(button_info).map((key) => (
          <Button name={key} button_info={button_info[key]} />
        ))}
      </div>
      <div className="flex h-full w-full overflow-auto rounded-2xl bg-white py-5 pl-5 shadow-lg">
        <div className="max-h-full w-full space-y-2 overflow-y-scroll font-medium 2xl:space-y-3">
          <Header />
          <List actual={evaluate.actual} predict={evaluate.predict} />
        </div>
      </div>
    </div>
  );
};

export default Evaluation;
