import React, { useEffect, useState } from "react";
import Swal from "sweetalert2";
import { AppContext } from "../../contexts/context";
import { FaRandom } from "react-icons/fa";
import { MdSave } from "react-icons/md";
import { GrPowerReset } from "react-icons/gr";
import { VscRunAll } from "react-icons/vsc";

import {
  initialEntry,
  initialFileCount,
  initialRange,
  initialTrigger,
} from "../../core/config";
import NavBar from "../../containers/common/NavBar";
import Menu from "../../containers/Menu/Menu";
import CountCardCont from "./containers/CountCard/CountCardCont";
import Gallery from "./containers/Gallery/Gallery";
import Trackbars from "./containers/Trackbars/Trackbars";
import getTrackbar from "./utils/getTrackbar";
import getCountRand from "./utils/getCountRand";
import getRandom from "./utils/getRandom";
import setTrackbar from "./utils/setTrackbar";
import process from "./utils/process";
import Entry from "./containers/Entry/Entry";

function CDA() {
  const [random, setRandom] = useState([]);
  const [state, setState] = useState("");
  const [entry, setEntry] = useState(initialEntry);
  const [fileCount, setFileCount] = useState(initialFileCount);
  const [range, setRange] = useState(initialRange);
  const [trigger, setTrigger] = useState(initialTrigger);

  useEffect(() => {
    const getTrack = async () => {
      const json = await getTrackbar();
      setRange({ input: json.trackbar, slider: json.trackbar });
    };
    getTrack();
  }, []);

  const reset = async () => {
    const json = await getTrackbar();
    setRange({ input: json.trackbar, slider: json.trackbar });
  };

  const getRandomFiles = async () => {
    const json = await getRandom(8);
    setRandom(json.file_list);
  };

  const updateRange = async () => {
    const alert = await setTrackbar(range.slider);

    Swal.fire({
      title: alert.title,
      text: alert.text,
      icon: alert.icon,
      confirmButtonText: alert.confirmButtonText,
    });
    return;
  };

  const process_img = async () => {
    setState("started");
    const alert = await process(range.slider, entry);
    setState("complete");

    Swal.fire({
      title: alert.title,
      text: alert.text,
      icon: alert.icon,
      confirmButtonText: alert.confirmButtonText,
    });
    return;
  };

  const button_info = {
    Random: {
      icon: <FaRandom />,
      onClick: getRandomFiles,
    },
    Save: {
      icon: <MdSave />,
      onClick: updateRange,
    },
    Reset: {
      icon: <GrPowerReset />,
      onClick: reset,
    },
    Process: {
      icon: <VscRunAll />,
      onClick: process_img,
      disabled: state === "started",
    },
  };

  const openMenu = async () => {
    if (!trigger.menu) {
      const json = await getCountRand();
      setFileCount(json.file_count);
    }
    setTrigger((prevTrig) => ({ ...prevTrig, menu: !prevTrig.menu }));
  };

  return (
    <AppContext.Provider
      value={{
        entry,
        setEntry,
        fileCount,
        setFileCount,
        random,
        setRandom,
        range,
        setRange,
        trigger,
        setTrigger,
      }}
    >
      <main className="flex h-screen w-screen bg-amber-100">
        <section className="w-full">
          <Gallery />
        </section>
        <aside className="relative w-[60%] border-l-2 border-slate-400">
          <NavBar openMenu={openMenu} button_info={button_info} />
          <Entry />
          <Trackbars />
          <Menu
            openMenu={openMenu}
            menu={trigger.menu}
            children={<CountCardCont />}
          />
        </aside>
      </main>
    </AppContext.Provider>
  );
}

export default CDA;
