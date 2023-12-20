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
  }, [random, range, image_hold, canvas_hold]);

  const arrow_size = `${Math.round(250 / random.length)}px`;
  const img_size = `flex w-[${
    random.length <= 4 ? 150 : random.length <= 6 ? 150 : 100
  }px] 2xl:w-[${random.length <= 4 ? 250 : random.length <= 6 ? 250 : 200}px]`;

  return (
    <>
      {random.map((src, i) => {
        return (
          <div
            className="flex h-full w-full justify-between bg-pink-300"
            key={i}
          >
            <div className="flex h-full w-full items-center justify-center bg-green-300">
              <img className={img_size} alt={src} ref={image_hold[i]} />
            </div>
            <div className={`flex h-full items-center bg-blue-300`}>
              <FaArrowRightLong size={arrow_size} className="bg-gray-300" />
            </div>
            <div className="flex h-full w-full items-center justify-center bg-red-300">
              <canvas className={img_size} ref={canvas_hold[i]} />
            </div>
          </div>
        );
      })}
    </>
  );
};

export default ImageCont;
