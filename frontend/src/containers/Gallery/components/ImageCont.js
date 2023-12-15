import React, { useContext, useMemo, createRef, useEffect } from "react";
import { FaArrowRightLong } from "react-icons/fa6";
import { AppContext } from "../../../contexts/context";

import imageFilter from "../../../utils/imagefilter";

const ImageCont = () => {
  const { random, range } = useContext(AppContext);
  const canvas_hold = useMemo(() => random.map(() => createRef()), [random]);
  const image_hold = useMemo(() => random.map(() => createRef()), [random]);

  useEffect(() => {
    imageFilter(random, range, image_hold, canvas_hold);
  }, [random, range]);

  const arrow_size = `${Math.round(250 / random.length)}px`;
  const scale = `scale-[${Math.round(120 / random.length) / 10}]`;

  return (
    <>
      {random.map((src, i) => {
        return (
          <div
            className="flex h-full w-full justify-between bg-pink-300"
            key={i}
          >
            <div className="flex h-full w-full items-center justify-center bg-green-300">
              <img className={scale} alt={src} ref={image_hold[i]} />
            </div>
            <div className={`flex h-full items-center bg-blue-300`}>
              <FaArrowRightLong size={arrow_size} className="bg-gray-300" />
            </div>
            <div className="flex h-full w-full items-center justify-center bg-red-300">
              <canvas className={scale} ref={canvas_hold[i]} />
            </div>
          </div>
        );
      })}
    </>
  );
};

export default ImageCont;
