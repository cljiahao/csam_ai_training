import React, { useEffect, useState } from "react";
import { Transition } from "@headlessui/react";
import { AppContext } from "../../contexts/context";

import { initialSettings } from "../../core/config";
import Gallery from "../../containers/Gallery/Gallery";
import ButtonCont from "../../containers/ButtonCont/ButtonCont";
import getTrackbar from "../../utils/getTrackbar";
import Trackbars from "../../containers/Trackbars/Trackbars";
import Menu from "../../containers/Menu/Menu";
import getCountRand from "../../utils/getCountRand";
import InputCont from "../../containers/InputCont/InputCont";

function CDA() {
  const [random, setRandom] = useState([]);
  const [range, setRange] = useState({});
  const [inText, setInText] = useState({});
  const [settings, setSettings] = useState(initialSettings);

  useEffect(() => {
    const getTrack = async () => {
      const json = await getTrackbar();
      setRange(json.trackbar);
      setInText(json.trackbar);
    };
    getTrack();
  }, []);

  const openMenu = async () => {
    if (settings.menu) {
      setSettings({
        ...settings,
        menu: !settings.menu,
      });
    } else {
      const json = await getCountRand();
      setSettings({
        ...settings,
        menu: !settings.menu,
        file_count: json.file_count,
      });
    }
  };

  return (
    <AppContext.Provider
      value={{
        random,
        setRandom,
        range,
        setRange,
        inText,
        setInText,
        settings,
        setSettings,
      }}
    >
      <div className="flex h-screen max-h-screen w-screen bg-amber-50">
        <section className="h-full w-[67%]">
          <Gallery />
        </section>
        <aside className="relative flex h-full w-[33%] flex-col border-l-2 border-gray-300">
          <ButtonCont openMenu={openMenu} />
          <InputCont />
          <Trackbars />
          <Transition
            show={settings.menu}
            enter="transition-opacity ease-in duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity ease-in duration-300"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <Menu openMenu={openMenu} />
          </Transition>
        </aside>
      </div>
    </AppContext.Provider>
  );
}

export default CDA;
