import React, { useContext, useMemo, createRef, useEffect } from "react";
import { FaArrowRightLong } from "react-icons/fa6";
import { AppContext } from "../../../../contexts/context";

import imageFilter from "./utils/imagefilter";

const Gallery = () => {
  const { random, range } = useContext(AppContext);
  const canvas_hold = useMemo(() => random.map(() => createRef()), [random]);
  const image_hold = useMemo(() => random.map(() => createRef()), [random]);

  useEffect(() => {
    imageFilter(random, range.slider, image_hold, canvas_hold);
  }, [random, range, image_hold, canvas_hold]);

  const arrow_size = `${Math.round(250 / random.length)}px`;
  const img_size = `${
    random.length <= 6
      ? "flex w-[150px] 2xl:w-[250px]"
      : "flex w-[100px] 2xl:w-[200px]"
  }`;

  return (
    <div className="grid h-full w-full grid-cols-2 items-center gap-x-10 gap-y-5">
      {random.map((src, i) => {
        return (
          <div
            className="flex h-full w-full justify-between rounded-3xl bg-slate-200"
            key={i}
          >
            <div className="flex h-full w-full items-center justify-center">
              <img className={img_size} alt={src} ref={image_hold[i]} />
            </div>
            <div className={`flex h-full items-center`}>
              <FaArrowRightLong size={arrow_size} className="" />
            </div>
            <div className="flex h-full w-full items-center justify-center">
              <canvas className={img_size} ref={canvas_hold[i]} />
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default Gallery;
