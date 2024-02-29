import React, { useState, useEffect } from "react";
import { AppContext } from "../../contexts/context";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { PiGauge } from "react-icons/pi";

import {
  initialParameters,
  initialTable,
  initialGraph,
} from "../../core/config";
import Menu from "../../containers/Menu/Menu";
import NavBar from "../../containers/common/NavBar";
import startTraining from "./utils/startTraining";
import getEpoch from "./utils/getEpoch";
import Training from "./containers/Training/Training";
import Evaluation from "./containers/Evaluation/Evaluation";
import { getFolderName } from "./utils/getFolderName";
import Outflow from "./containers/Evaluation/components/Outflow/Outflow";
import { Transition } from "@headlessui/react";

function CMT() {
  const [menu, setMenu] = useState(false);
  const [expand, setExpand] = useState(false);
  const [outflow, setOutflow] = useState(false);
  const [drop, setDrop] = useState([]);
  const [graph, setGraph] = useState(initialGraph);
  const [parameters, setParameters] = useState(initialParameters);
  const [table, setTable] = useState(initialTable);

  useEffect(() => {
    const folderName = async () => {
      const json = await getFolderName();
      setDrop(json);
    };
    folderName();
    return;
  }, []);

  useEffect(() => {
    const fetch_epoch_data = async () => {
      if (graph.status && graph.status !== "complete") {
        const json = await getEpoch();
        const { status, ...graphVal } = json;
        setGraph({ status: status, graph: [...graph.graph, graphVal] });
      }
    };
    const timeout = setTimeout(fetch_epoch_data, 1000);
    return () => {
      clearTimeout(timeout);
    };
  }, [graph]);

  const openMenu = () => {
    setMenu(!menu);
  };

  const startTrain = async () => {
    const json = await startTraining(parameters);
    if (json) {
      setGraph({ status: json.status, graph: initialGraph.graph });
    }
  };

  const button_info = {
    Train: {
      icon: <LiaChalkboardTeacherSolid />,
      onClick: startTrain,
      disabled: graph.status !== "complete",
    },
    Evaluate: {
      icon: <PiGauge />,
      onClick: "",
      disabled: graph.status !== "complete",
    },
  };

  return (
    <AppContext.Provider
      value={{
        drop,
        setDrop,
        expand,
        setExpand,
        graph,
        setGraph,
        outflow,
        setOutflow,
        table,
        setTable,
        parameters,
        setParameters,
      }}
    >
      <main className="no-scrollbar relative flex max-h-screen w-screen overflow-auto bg-amber-100 text-sm 2xl:text-lg">
        <section className="w-full">
          <Training />
        </section>
        <aside
          className={`relative flex w-[60%] flex-col overflow-auto border-l-2 border-slate-400 ${
            expand ? "h-full" : "h-screen"
          }`}
        >
          <NavBar openMenu={openMenu} button_info={button_info} />
          <Evaluation />
          <Menu openMenu={openMenu} menu={menu} />
        </aside>
        <Transition
          show={outflow}
          enter="transition-opacity ease-in duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="transition-opacity ease-in duration-300"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <Outflow />
        </Transition>
      </main>
    </AppContext.Provider>
  );
}

export default CMT;
