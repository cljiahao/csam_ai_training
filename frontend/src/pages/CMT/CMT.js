import React, { useState, useEffect } from "react";
import { AppContext } from "../../contexts/context";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { PiGauge } from "react-icons/pi";
import { Transition } from "@headlessui/react";

import {
  initialParameters,
  initialTable,
  initialGraph,
  initialTrigger,
  initialDrop,
  initialOutflow,
} from "../../core/config";
import Menu from "../../containers/Menu/Menu";
import NavBar from "../../containers/common/NavBar";
import Training from "./containers/Training/Training";
import Evaluation from "./containers/Evaluation/Evaluation";
import Outflow from "./containers/Evaluation/components/Outflow/Outflow";
import startTraining from "./utils/startTraining";
import startEvaluation from "./utils/startEvaluation";
import { getItemType } from "./utils/getFolderName";
import getEpoch from "./utils/getEpoch";

function CMT() {
  const [drop, setDrop] = useState(initialDrop);
  const [graph, setGraph] = useState(initialGraph);
  const [outflow, setOutflow] = useState(initialOutflow);
  const [parameters, setParameters] = useState(initialParameters);
  const [table, setTable] = useState(initialTable);
  const [trigger, setTrigger] = useState(initialTrigger);

  useEffect(() => {
    const get_item_type = async () => {
      const json = await getItemType();
      setDrop((prevDrop) => ({
        ...prevDrop,
        item: { ...prevDrop.item, list: json },
      }));
    };
    get_item_type();
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
    console.log(outflow);
    setTrigger((prevTrigger) => ({
      ...prevTrigger,
      menu: !prevTrigger.menu,
    }));
  };

  const startTrain = async () => {
    if (parameters.folder === drop.folder.selected) {
      const json = await startTraining(parameters);
      if (json) {
        setGraph({ status: json.status, graph: initialGraph.graph });
      }
    }
  };

  const startEval = async () => {
    if (drop.item.selected) {
      setOutflow({ status: "running", res: {} });
      const json = await startEvaluation("test", drop.item.selected);
      if (json) {
        setOutflow({ status: "complete", res: json });
      }
    }
  };

  const button_info = {
    train: {
      name: "Train",
      icon: <LiaChalkboardTeacherSolid />,
      onClick: startTrain,
      disabled: graph.status !== "complete" || outflow.status !== "complete",
    },
    evaluate: {
      name: "Evaluate",
      icon: <PiGauge />,
      onClick: startEval,
      disabled: graph.status !== "complete" || outflow.status !== "complete",
    },
  };

  return (
    <AppContext.Provider
      value={{
        drop,
        setDrop,
        graph,
        setGraph,
        outflow,
        setOutflow,
        parameters,
        setParameters,
        table,
        setTable,
        trigger,
        setTrigger,
      }}
    >
      <main className="no-scrollbar relative flex max-h-screen w-screen overflow-auto bg-amber-100 text-sm 2xl:text-lg">
        <section className="w-full">
          <Training />
        </section>
        <aside
          className={`relative flex w-[60%] flex-col overflow-auto border-l-2 border-slate-400 ${
            trigger.expand ? "h-full" : "h-screen"
          }`}
        >
          <NavBar openMenu={openMenu} button_info={button_info} />
          <Evaluation />
          <Menu openMenu={openMenu} menu={trigger.menu} />
        </aside>
        <Transition
          show={trigger.outflow}
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
