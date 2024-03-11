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
  initialEvaluation,
} from "../../core/config";
import Menu from "../../containers/Menu/Menu";
import NavBar from "../../containers/common/NavBar";
import Training from "./containers/Training/Training";
import HyperParameters from "./containers/Training/components/HyperParameters/HyperParameters";
import Evaluation from "./containers/Evaluation/Evaluation";
import Outflow from "./containers/Evaluation/components/Outflow/Outflow";
import startTraining from "./utils/startTraining";
import startEvaluation from "./utils/startEvaluation";
import { getAllModels, getEvalFolder, getItemType } from "./utils/getNames";
import getEpoch from "./utils/getEpoch";

function CMT() {
  const [drop, setDrop] = useState(initialDrop);
  const [evaluate, setEvaluate] = useState(initialEvaluation);
  const [graph, setGraph] = useState(initialGraph);
  const [outflow, setOutflow] = useState(initialOutflow);
  const [parameters, setParameters] = useState(initialParameters);
  const [table, setTable] = useState(initialTable);
  const [trigger, setTrigger] = useState(initialTrigger);

  useEffect(() => {
    item_refresh();
    models_refresh();
  }, []);

  useEffect(() => {
    eval_refresh(drop.item.selected);
  }, [drop.item.selected]);

  useEffect(() => {
    const fetch_epoch_data = async () => {
      if (graph.status !== "complete") {
        const json = await getEpoch();
        const { status, ...graphVal } = json;
        setGraph({
          ...graph,
          status: status,
          graph: [...graph.graph, graphVal],
        });
      }
    };

    const timeout = setTimeout(fetch_epoch_data, 1000);
    return () => {
      clearTimeout(timeout);
    };
  }, [graph]);

  const openMenu = () => {
    setTrigger((prevTrigger) => ({
      ...prevTrigger,
      menu: !prevTrigger.menu,
    }));
  };

  const item_refresh = async () => {
    const json = await getItemType();
    setDrop((prevDrop) => ({
      ...prevDrop,
      item: { list: json, selected: "" },
      folder: { ...prevDrop.folder, selected: "" },
    }));
  };

  const models_refresh = async () => {
    const json = await getAllModels();
    setDrop((prevDrop) => ({
      ...prevDrop,
      model: { list: json, selected: "" },
    }));
  };

  const eval_refresh = async (item) => {
    const json = await getEvalFolder(item);
    setEvaluate({ actual: json.actual, predict: json.predict });
  };

  const startTrain = async () => {
    if (parameters.folder === drop.folder.selected) {
      setGraph({ status: "started", model: "", graph: initialGraph.graph });
      const json = await startTraining(parameters);
      if (json) {
        setGraph({ ...graph, model: json });
      }
    }
  };

  const startEval = async () => {
    if (drop.item.selected && drop.model.selected) {
      setOutflow({ status: "running", res: {} });
      const json = await startEvaluation(
        drop.model.selected,
        drop.item.selected,
      );
      if (json) {
        setOutflow({ status: "complete", res: json });
        setEvaluate((prevEval) => ({ ...prevEval, predict: json }));
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
      onClick: startEval(drop.model.selected),
      disabled: graph.status !== "complete" || outflow.status !== "complete",
    },
  };

  return (
    <AppContext.Provider
      value={{
        drop,
        setDrop,
        evaluate,
        setEvaluate,
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
          <Training refresh={item_refresh} />
        </section>
        <aside
          className={`relative flex w-[60%] flex-col overflow-auto border-l-2 border-slate-400 ${
            trigger.expand ? "h-full" : "h-screen"
          }`}
        >
          <NavBar openMenu={openMenu} button_info={button_info} />
          <Evaluation refresh={eval_refresh} />
          <Menu
            openMenu={openMenu}
            menu={trigger.menu}
            children={<HyperParameters refresh={models_refresh} />}
          />
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
