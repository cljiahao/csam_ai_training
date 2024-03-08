import React, { useContext } from "react";
import { TbRefresh } from "react-icons/tb";
import { MdWrongLocation } from "react-icons/md";
import { AppContext } from "../../../../contexts/context";

import ButtonsCont from "../../../../containers/common/ButtonsCont";
import Header from "./components/Header/Header";
import List from "./components/List/List";

const Evaluation = ({ refresh }) => {
  const { drop, evaluate, setTrigger } = useContext(AppContext);

  const button_info = {
    refresh: {
      name: "Refresh",
      icon: <TbRefresh />,
      onClick: () => refresh(drop.item.selected),
    },
    outflow: {
      name: "Outflow",
      icon: <MdWrongLocation />,
      onClick: () =>
        setTrigger((prevTrigger) => ({
          ...prevTrigger,
          outflow: !prevTrigger.outflow,
        })),
    },
  };

  return (
    <div className="flex flex-1 flex-col overflow-auto px-3">
      <ButtonsCont
        button_info={button_info}
        styles={"w-full flex-between h-14 2xl:h-24 gap-[50%]"}
      />
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
