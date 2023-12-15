import React, { useEffect, useState } from "react";
import { Transition } from "@headlessui/react";
import { AppContext } from "../../contexts/context";

import Gallery from "../../containers/Gallery/Gallery";
import ButtonCont from "../../containers/ButtonCont/ButtonCont";
import getTrackbar from "../../utils/getTrackbar";
import Trackbars from "../../containers/Trackbars/Trackbars";

function CDA() {
  const [random, setRandom] = useState([]);
  const [range, setRange] = useState({});
  const [inText, setInText] = useState({});

  useEffect(() => {
    const getTrack = async () => {
      const json = await getTrackbar();
      setRange(json.trackbar);
      setInText(json.trackbar);
    };
    getTrack();
  }, []);

  return (
    <AppContext.Provider
      value={{ random, setRandom, range, setRange, inText, setInText }}
    >
      <div className="flex h-screen max-h-screen w-screen bg-amber-50">
        <section className="h-full w-[67%]">
          <Gallery />
        </section>
        <aside className="h-full w-[33%]">
          <ButtonCont />
          <Trackbars />
        </aside>
      </div>
    </AppContext.Provider>
  );
}

export default CDA;
