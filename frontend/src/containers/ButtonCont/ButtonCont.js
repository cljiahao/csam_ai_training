import React, { useContext } from "react";
import Swal from "sweetalert2";
import { IoMenu } from "react-icons/io5";
import { FaRandom } from "react-icons/fa";
import { MdSave } from "react-icons/md";
import { GrPowerReset } from "react-icons/gr";
import { VscRunAll } from "react-icons/vsc";
import { AppContext } from "../../contexts/context";

import Button from "../common/Button";
import getRandom from "../../utils/getRandom";
import getTrackbar from "../../utils/getTrackbar";
import setTrackbar from "../../utils/setTrackbar";
import process from "../../utils/process";

const ButtonCont = ({ openMenu }) => {
  const { range, setRandom, setRange, setInText } = useContext(AppContext);

  const getRandomFiles = async () => {
    const json = await getRandom(8);
    setRandom(json.file_list);
  };

  const reset = async () => {
    const json = await getTrackbar();
    setRange(json.trackbar);
    setInText(json.trackbar);
  };

  const updateRange = async () => {
    const alert = await setTrackbar(range);

    Swal.fire({
      title: alert.title,
      text: alert.text,
      icon: alert.icon,
      confirmButtonText: alert.confirmButtonText,
    });
    return;
  };

  const process_img = async () => {
    const alert = await process(range);

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
    },
  };

  return (
    <div className="flex h-[11%] w-full items-center border-b-2 border-gray-300 2xl:h-[8%]">
      <div className="mx-1 flex h-full items-center justify-center 2xl:mx-2">
        <IoMenu className="cursor-pointer" size="1.5rem" onClick={openMenu} />
      </div>
      <div className="group flex h-full w-full items-center gap-3 pr-3 font-bold 2xl:gap-8">
        {Object.keys(button_info).map((key) => {
          return (
            <Button
              key={key}
              but_class="flex h-[75%] w-full items-center justify-center gap-1 2xl:gap-2 rounded-lg bg-blue-300 group/items text-2xl hover:text-base 2xl:text-3xl 2xl:hover:text-2xl"
              span_class="hidden group-hover/items:block text-sm 2xl:text-xl"
              icon={button_info[key].icon}
              text={key}
              onClick={button_info[key].onClick}
            />
          );
        })}
      </div>
    </div>
  );
};

export default ButtonCont;
