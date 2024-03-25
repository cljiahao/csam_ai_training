import React, { useEffect, useState } from "react";
import Swal from "sweetalert2";
import { AppContext } from "../../contexts/context";
import { FaRandom } from "react-icons/fa";
import { MdSave } from "react-icons/md";
import { GrPowerReset } from "react-icons/gr";
import { VscRunAll } from "react-icons/vsc";

import {
  initialDrop,
  initialEntry,
  initialRandom,
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
import { getItemType, getRandomImg, getRandomCount } from "./utils/getNames";
import process from "./utils/process";

function CDA() {
  const [state, setState] = useState("");
  const [drop, setDrop] = useState(initialDrop);
  const [entry, setEntry] = useState(initialEntry);
  const [random, setRandom] = useState(initialRandom);
  const [range, setRange] = useState(initialRange);
  const [trigger, setTrigger] = useState(initialTrigger);

  useEffect(() => {
    get_trackbar();
    item_refresh();
  }, []);

  const get_trackbar = async () => {
    const json = await getTrackbar();
    setRange({ input: json, slider: json });
  };

  const item_refresh = async () => {
    const json = await getItemType();
    setDrop((prevDrop) => ({
      ...prevDrop,
      item: { list: json, selected: "" },
      folder: { ...prevDrop.folder, selected: "" },
    }));
  };

  const get_random_files = async () => {
    if (drop.item.selected) {
      const json = await getRandomImg(drop.item.selected, 8);
      setRandom((prevRandom) => ({ ...prevRandom, gallery: json }));
    }
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
    const alert = await process(range.slider, drop.item.selected, entry);
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
    if (!trigger.menu && drop.item.selected) {
      const json = await getRandomCount(drop.item.selected);
      setRandom((prevRandom) => ({ ...prevRandom, count: json }));
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
      disabled: state === "started" || Object.values(entry).includes(""),
    },
  };

  return (
    <AppContext.Provider
      value={{
        drop,
        setDrop,
        entry,
        setEntry,
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
          <Entry refresh={item_refresh} />
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
