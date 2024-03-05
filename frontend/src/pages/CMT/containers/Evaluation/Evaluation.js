import React, { useContext, useEffect, useState } from "react";
import { TbRefresh } from "react-icons/tb";
import { MdWrongLocation } from "react-icons/md";
import { AppContext } from "../../../../contexts/context";

import ButtonsCont from "../../../../containers/common/ButtonsCont";
import Header from "./components/Header/Header";
import List from "./components/List/List";
import { getEvalFolder } from "../../utils/getFolderName";

const Evaluation = () => {
  const { drop, setTrigger } = useContext(AppContext);
  const [evalFol, setEvalFol] = useState({});
  const [predFol, setPredFol] = useState({});

  useEffect(() => {
    refresh(drop.item.selected);
  }, [drop.item.selected]);

  const refresh = async (item) => {
    const json = await getEvalFolder(item);
    setEvalFol(json.eval);
    setPredFol(json.pred);
  };

  const button_info = {
    Refresh: {
      icon: <TbRefresh />,
      onClick: () => refresh(drop.item.selected),
    },
    Outflow: {
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
        styles={"w-full flex-between h-14 2xl:h-18 gap-[50%]"}
      />
      <div className="flex h-full w-full overflow-auto rounded-2xl bg-white py-5 pl-5 shadow-lg">
        <div className="max-h-full w-full space-y-2 overflow-y-scroll font-medium 2xl:space-y-3">
          <Header />
          <List data={evalFol} preds={predFol} />
        </div>
      </div>
    </div>
  );
};

export default Evaluation;
