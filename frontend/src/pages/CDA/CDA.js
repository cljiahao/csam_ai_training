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
  initialAugRange,
  initialTrigger,
} from "../../core/config";
import Menu from "../../common/containers/Menu/Menu";
import NavBar from "../../common/containers/NavBar/NavBar";
import Entry from "./containers/Entry/Entry";
import CountCardCont from "./containers/CountCard/CountCardCont";
import Gallery from "./containers/Gallery/Gallery";
import Trackbars from "./containers/Trackbars/Trackbars";
import { getTrackbar, setTrackbar } from "./utils/api_trackbar";
import { getItemType } from "../../utils/api_misc";
import { getRandomImg, getRandomCount } from "./utils/api_misc";
import process from "./utils/api_process";

function CDA() {
  const [state, setState] = useState("");
  const [drop, setDrop] = useState(initialDrop);
  const [entry, setEntry] = useState(initialEntry);
  const [random, setRandom] = useState(initialRandom);
  const [range, setRange] = useState(initialAugRange);
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
    const json = await getItemType("CDA");
    setDrop((prevDrop) => ({
      ...prevDrop,
      item: { list: json, selected: "" },
      folder: { ...prevDrop.folder, selected: "" },
    }));
    setEntry(initialEntry);
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
    Swal.fire({
      title: "Do you want to bypass augment?",
      text: "Click Yes to bypass and No to proceed with augment",
      icon: "question",
      showCancelButton: true,
      confirmButtonText: "Yes",
      cancelButtonText: "No",
    }).then(async (result) => {
      setState("started");
      const alert = await process(
        range.slider,
        drop.item.selected,
        entry,
        result.isConfirmed,
      );
      setState("complete");

      Swal.fire({
        title: alert.title,
        text: alert.text,
        icon: alert.icon,
        confirmButtonText: alert.confirmButtonText,
      });
      return;
    });
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
      style: { font: "text-2xl", width: "w-full" },
      onClick: get_random_files,
    },
    save: {
      name: "Save",
      icon: <MdSave />,
      style: { font: "text-2xl", width: "w-full" },
      onClick: update_range,
    },
    reset: {
      name: "Reset",
      icon: <GrPowerReset />,
      style: { font: "text-2xl", width: "w-full" },
      onClick: get_trackbar,
    },
    process: {
      name: "Process",
      icon: <VscRunAll />,
      onClick: process_img,
      style: { font: "text-2xl", width: "w-full" },
      disabled: state === "started" || Number(entry.random) < 100,
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
      <main className="flex h-screen w-screen overflow-hidden bg-amber-100">
        <section className="w-full">
          <Gallery />
        </section>
        <aside className="relative w-[60%] border-l-2 border-slate-400">
          <div className="w-full border-b-2 border-slate-400">
            <NavBar openMenu={openMenu} button_info={button_info} />
          </div>
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
