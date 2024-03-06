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
import Entry from "./containers/Entry/Entry";
import CountCardCont from "./containers/CountCard/CountCardCont";
import Gallery from "./containers/Gallery/Gallery";
import Trackbars from "./containers/Trackbars/Trackbars";
import { getTrackbar, setTrackbar } from "./utils/trackbar";
import getCountRand from "./utils/getCountRand";
import getRandom from "./utils/getRandom";
import process from "./utils/process";

function CDA() {
  const [random, setRandom] = useState([]);
  const [state, setState] = useState("");
  const [entry, setEntry] = useState(initialEntry);
  const [fileCount, setFileCount] = useState(initialFileCount);
  const [range, setRange] = useState(initialRange);
  const [trigger, setTrigger] = useState(initialTrigger);

  useEffect(() => {
    get_trackbar();
  }, []);

  const get_trackbar = async () => {
    const json = await getTrackbar();
    setRange({ input: json.trackbar, slider: json.trackbar });
  };

  const get_random_files = async () => {
    const json = await getRandom(8);
    setRandom(json.file_list);
  };

  const update_range = async () => {
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

  const openMenu = async () => {
    if (!trigger.menu) {
      const json = await getCountRand();
      setFileCount(json.file_count);
    }
    setTrigger((prevTrig) => ({ ...prevTrig, menu: !prevTrig.menu }));
  };

  const button_info = {
    random: {
      name: "Random",
      icon: <FaRandom />,
      onClick: get_random_files,
    },
    save: {
      name: "Save",
      icon: <MdSave />,
      onClick: update_range,
    },
    reset: {
      name: "Reset",
      icon: <GrPowerReset />,
      onClick: get_trackbar,
    },
    process: {
      name: "Process",
      icon: <VscRunAll />,
      onClick: process_img,
      disabled: state === "started",
    },
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
